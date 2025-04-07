from logging import getLogger
from typing import Any, Dict

import requests
from core import storage
from core.authentication.auth_middleware import get_current_token
from core.config import settings
from core.get_flow_url import update_flow_properties
from core.marketplace import quest_flows
from core.microsoft_auth_client import get_msal_client
from fastapi import APIRouter, Body, Depends, HTTPException, status
from msal import ConfidentialClientApplication
from schemas.token import TokenData

# FastAPI router
router = APIRouter(prefix="/power_automate")

BASE_URL = "https://api.flow.microsoft.com"


@router.get("/get_environments")
def get_environments(
    token_data: TokenData = Depends(get_current_token),
    msal_client: ConfidentialClientApplication = Depends(get_msal_client),
):
    """Fetch available Power Automate environments."""
    logger = getLogger(__name__ + ".get_environments")
    try:
        # conn_data = storage.platform_connections.get(
        #     {"user_id": token_data.id}
        # )
        # oid = conn_data.microsoft_oid

        if len(msal_client.get_accounts()) == 0:
            raise HTTPException(
                status_code=400, detail="Outlook not connected"
            )

        token = msal_client.acquire_token_silent(
            scopes=settings.AZURE_SCOPE, account=msal_client.get_accounts()[0]
        ).get("access_token")
        # if not token:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Microsoft Auth not completed",
        #     )

        URL = f"{BASE_URL}/providers/Microsoft.ProcessSimple/environments?api-version=2016-11-01"

        api_result = requests.get(
            URL,
            headers={"Authorization": "Bearer " + token},
            timeout=30,
        ).json()
        return api_result
    except HTTPException as ex:
        logger.exception(ex)
        raise ex
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to get environments",
        )


@router.post("/upload_flow")
def upload_flow(
    environment_id: str = Body(embed=True),
    token_data: TokenData = Depends(get_current_token),
    msal_client: ConfidentialClientApplication = Depends(get_msal_client),
):
    """Upload a Power Automate flow from a zip file."""
    logger = getLogger(__name__ + ".upload_flow")
    try:
        # conn_data = storage.platform_connections.get(
        #     {"user_id": token_data.id}
        # )
        # oid = conn_data.microsoft_oid
        if len(msal_client.get_accounts()) == 0:
            raise HTTPException(
                status_code=400, detail="Outlook not connected"
            )
        token = msal_client.acquire_token_silent(
            scopes=settings.AZURE_SCOPE, account=msal_client.get_accounts()[0]
        ).get("access_token")
        # if not token:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Microsoft Auth not completed",
        #     )

        # Get connections flow
        URL = f"{BASE_URL}/providers/Microsoft.ProcessSimple/environments/{environment_id}/flows?api-version=2016-11-01"

        api_result = requests.get(
            URL,
            headers={"Authorization": "Bearer " + token},
            timeout=30,
        ).json()
        logger.info(api_result)
        # Filter the flow with displayName 'Quest Aut[[h'
        filtered_flows = [
            flow
            for flow in api_result["value"]
            if flow["properties"]["displayName"] == "Quest AI Connections"
        ]

        # If the filtered_flows is empty, the flow with 'Quest Auth' display name doesn't exist
        if filtered_flows:
            logger.info(filtered_flows)
            flow_properties = filtered_flows[0]["properties"][
                "connectionReferences"
            ]
        else:
            logger.info(
                "Quest AI Connections flow not found. Import flow and try again."
            )

        ########################################################
        # Get the connections name from the filtered_flows

        Microsoft_Teams_connection = flow_properties.get(
            "shared_teams", None
        ).get("connectionName", None)
        SharePoint_connection = flow_properties.get(
            "shared_sharepointonline", None
        ).get("connectionName", None)
        Office_365_Outlook_connection = flow_properties.get(
            "shared_office365", None
        ).get("connectionName", None)
        Office_365_Users_connection = flow_properties.get(
            "shared_office365users", None
        ).get("connectionName", None)
        Flow_Management_connection = flow_properties.get(
            "shared_flowmanagement", None
        ).get("connectionName", None)

        # Print the connection names to verify
        logger.info(
            f"Microsoft Teams Connection Name: {Microsoft_Teams_connection}"
        )
        logger.info(f"SharePoint Connection Name: {SharePoint_connection}")
        logger.info(
            f"Office 365 Outlook Connection Name: {Office_365_Outlook_connection}"
        )
        logger.info(
            f"Office 365 Users Connection Name: {Office_365_Users_connection}"
        )
        logger.info(
            f"Flow Management Connection Name: {Flow_Management_connection}"
        )
        ########################################################
        # Replace the connections name in the quest_flows

        def update_connection_if_exists(
            flow, connection_key, new_connection_name
        ):
            logger = getLogger(__name__ + ".update_connection_if_exists")
            try:
                # Check if the connection exists in the flow
                if (
                    connection_key
                    in flow["properties"]["connectionReferences"]
                ):
                    # Update the connection name
                    flow["properties"]["connectionReferences"][connection_key][
                        "connectionName"
                    ] = new_connection_name
                    logger.info(
                        f"Updated {connection_key} connection name to: {new_connection_name}"
                    )
                else:
                    logger.info(
                        f"{connection_key} connection does not exist in this flow. No changes made."
                    )
            except Exception as ex:
                logger.exception(ex)
                raise ex

        for flow in quest_flows:
            # Update each connection if it exists
            update_connection_if_exists(
                flow, "shared_office365", Office_365_Outlook_connection
            )
            update_connection_if_exists(
                flow, "shared_office365users", Office_365_Users_connection
            )
            update_connection_if_exists(
                flow, "shared_sharepointonline", SharePoint_connection
            )
            update_connection_if_exists(
                flow, "shared_teams", Microsoft_Teams_connection
            )
            update_connection_if_exists(
                flow, "shared_flowmanagement", Flow_Management_connection
            )

        ########################################################
        # Upload the flows

        URL = f"{BASE_URL}/providers/Microsoft.ProcessSimple/environments/{environment_id}/flows?api-version=2016-11-01"
        primary_flows_responses = []
        for item in quest_flows:
            api_result = requests.post(
                URL,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json=item,
                timeout=30,
            ).json()
            logger.info(api_result)
            primary_flows_responses.append(
                {
                    "flowID": api_result.get("name"),
                    "flowName": api_result.get("properties", {}).get(
                        "displayName"
                    ),
                }
            )

        ########################################################
        # Upload the url collection flows
        url_collection_responses = []
        for response in primary_flows_responses:
            flow_id = response.get("flowID")
            # First update environment and flow IDs
            updated_flow_object = update_flow_properties(
                environment_id, flow_id
            )
            logger.info(updated_flow_object)
            update_connection_if_exists(
                updated_flow_object,
                "shared_office365",
                Office_365_Outlook_connection,
            )
            update_connection_if_exists(
                updated_flow_object,
                "shared_office365users",
                Office_365_Users_connection,
            )
            update_connection_if_exists(
                updated_flow_object,
                "shared_sharepointonline",
                SharePoint_connection,
            )
            update_connection_if_exists(
                updated_flow_object, "shared_teams", Microsoft_Teams_connection
            )
            update_connection_if_exists(
                updated_flow_object,
                "shared_flowmanagement",
                Flow_Management_connection,
            )

            URL = f"{BASE_URL}/providers/Microsoft.ProcessSimple/environments/{environment_id}/flows?api-version=2016-11-01"

            api_result = requests.post(
                URL,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json=updated_flow_object,
                timeout=30,
            ).json()
            logger.info(api_result)
            url_collection_responses.append(
                {
                    "flowID": api_result.get("name"),
                    "flowName": api_result.get("properties", {}).get(
                        "displayName"
                    ),
                }
            )
        message = {
            "primary_flows_responses": primary_flows_responses,
            "url_collection_responses": url_collection_responses,
        }
        return message
    except HTTPException as ex:
        logger.exception(ex)
        raise ex
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to upload flows",
        )
