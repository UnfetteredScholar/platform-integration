import copy
from logging import getLogger

url_collection_flow_template = {
    "properties": {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
        "displayName": "Send Flow URL",
        "definition": {
            "metadata": {
                "workflowEntityId": "None",
                "processAdvisorMetadata": "None",
                "flowChargedByPaygo": "None",
                "flowclientsuspensionreason": "None",
                "flowclientsuspensiontime": "None",
                "flowclientsuspensionreasondetails": "None",
                "creator": {
                    "id": "67c7ec85-5ebf-41db-85f2-238260635b73",
                    "type": "User",
                    "tenantId": "7e1c5bc5-e201-4917-8255-619176a3e046",
                },
                "provisioningMethod": "FromDefinition",
                "failureAlertSubscription": True,
                "clientLastModifiedTime": "2025-04-07T15:31:09.8649178Z",
                "connectionKeySavedTimeKey": "2025-04-07T15:31:09.8649178Z",
                "creationSource": "Portal",
                "modifiedSources": "Portal",
            },
            "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "$authentication": {
                    "defaultValue": {},
                    "type": "SecureObject",
                },
                "$connections": {"defaultValue": {}, "type": "Object"},
            },
            "triggers": {
                "Recurrence": {
                    "recurrence": {
                        "interval": 60,
                        "frequency": "Second",
                        "timeZone": "UTC",
                    },
                    "type": "Recurrence",
                }
            },
            "actions": {
                "List_Callback_URL": {
                    "runAfter": {},
                    "type": "OpenApiConnection",
                    "inputs": {
                        "parameters": {
                            "environmentName": "Default-7e1c5bc5-e201-4917-8255-619176a3e046",
                            "flowName": "5cc25a6f-830a-42ac-a5fb-49a43ea99a4f",
                        },
                        "host": {
                            "apiId": "/providers/Microsoft.PowerApps/apis/shared_flowmanagement",
                            "connectionName": "shared_flowmanagement",
                            "operationId": "ListCallbackUrl",
                        },
                        "authentication": "@parameters('$authentication')",
                    },
                },
                "HTTP": {
                    "runAfter": {"Get_Flow": ["Succeeded"]},
                    "type": "Http",
                    "inputs": {
                        "uri": "https://platform-integration.onrender.com/api/v1/power_automate/flows",
                        "method": "PUT",
                        "headers": {"Authorization": "auth_key"},
                        "body": {
                            "flow_id": "@outputs('Get_Flow')?['body/properties/displayName']",
                            "flow_url": "@outputs('List_Callback_URL')?['body/response/value']",
                        },
                    },
                    "runtimeConfiguration": {
                        "contentTransfer": {"transferMode": "Chunked"}
                    },
                },
                "Get_Flow": {
                    "runAfter": {"List_Callback_URL": ["Succeeded"]},
                    "type": "OpenApiConnection",
                    "inputs": {
                        "parameters": {
                            "environmentName": "Default-7e1c5bc5-e201-4917-8255-619176a3e046",
                            "flowName": "5cc25a6f-830a-42ac-a5fb-49a43ea99a4f",
                        },
                        "host": {
                            "apiId": "/providers/Microsoft.PowerApps/apis/shared_flowmanagement",
                            "connectionName": "shared_flowmanagement",
                            "operationId": "GetFlow",
                        },
                        "authentication": "@parameters('$authentication')",
                    },
                },
            },
            "outputs": {},
        },
        "connectionReferences": {
            "shared_flowmanagement": {
                "connectionName": "shared-flowmanagemen-eeadf6eb-1c04-410b-9391-cc66b5807873",
                "source": "Embedded",
                "id": "/providers/Microsoft.PowerApps/apis/shared_flowmanagement",
                "tier": "NotSpecified",
                "apiName": "flowmanagement",
            }
        },
        "flowFailureAlertSubscribed": False,
        "isManaged": False,
    }
}


def update_flow_properties(environment_id, flow_name, auth_header: str):
    """
    Updates the environmentName and flowName within a flow template structure
    and returns it in the specified format {"properties": updated_properties}.

    Args:
      flow_template_list (list): A list containing one dictionary,
                                 representing the flow template structure.
                                 Assumes the structure matches the provided example.
      environment_id (str): The new environment ID to set.
      flow_name (str): The new flow name to set.

    Returns:
      dict: A new dictionary in the format {"properties": updated_properties}
            containing the modified flow properties, or None if the input
            structure is invalid or keys are missing.
    """
    logger = getLogger(__name__ + ".update_flow_properties")
    # Use deepcopy to avoid modifying the original template object
    try:
        template_copy = copy.deepcopy(url_collection_flow_template)
    except (TypeError, IndexError):
        print("Error: Could not copy input template structure.")
        return None

    # Navigate through the nested structure and update the values
    # Using .get() for safer access in case keys are missing
    try:
        properties_data = template_copy.get("properties")
        if properties_data is None:
            raise KeyError("'properties' key not found")

        # Update List_Callback_URL parameters
        list_callback_params = (
            properties_data.get("definition", {})
            .get("actions", {})
            .get("List_Callback_URL", {})
            .get("inputs", {})
            .get("parameters")
        )

        if list_callback_params is None:
            raise KeyError(
                "Nested path to List_Callback_URL parameters not found or incomplete"
            )

        list_callback_params["environmentName"] = environment_id
        list_callback_params["flowName"] = flow_name

        # Update Get_Flow parameters
        get_flow_params = (
            properties_data.get("definition", {})
            .get("actions", {})
            .get("Get_Flow", {})
            .get("inputs", {})
            .get("headers")
        )

        if get_flow_params is None:
            raise KeyError(
                "Nested path to Get_Flow parameters not found or incomplete"
            )

        get_flow_params["environmentName"] = environment_id
        get_flow_params["flowName"] = flow_name

        # Update HTTP parameters
        http_params = (
            properties_data.get("definition", {})
            .get("actions", {})
            .get("HTTP", {})
            .get("inputs", {})
            .get("parameters")
        )

        if http_params is None:
            raise KeyError(
                "Nested path to Get_Flow parameters not found or incomplete"
            )

        http_params["Authorization"] = auth_header

    except KeyError as e:
        logger.error(f"Error: Missing key in template structure - {e}")
        logger.exception(e)
        return None
    except AttributeError as e:
        logger.error(
            f"Error: Problem accessing attribute, structure might differ - {e}"
        )
        logger.exception
        return None

    # Construct the final output object in the desired format
    output_object = {"properties": properties_data}

    return output_object
