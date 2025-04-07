from logging import getLogger
from typing import Dict, Optional

from bson.objectid import ObjectId
from core import storage
from core.authentication.auth_middleware import get_current_token
from fastapi import APIRouter, Depends, HTTPException, Path
from schemas.page import Page
from schemas.power_automate_user_flows import (
    FlowStatus,
    PAFlowIn,
    PAUserFlow,
    PAUserFlowUpdate,
)
from schemas.token import TokenData

router = APIRouter()


@router.put("/power_automate/flows", response_model=PAUserFlow)
async def add_user_flow(
    flow_data: PAFlowIn,
    token_data: TokenData = Depends(get_current_token),
) -> PAUserFlow:
    """
    Updates or adds flow information for a specific user.

    Args:
        flows_data: power automate flow data to store
    """
    logger = getLogger(__name__ + ".add_user_flow")
    try:
        if storage.power_automate_user_flows.get(
            {"flow_id": flow_data.flow_id, "user_id": token_data.id}
        ):
            storage.power_automate_user_flows.update(
                filter={
                    "flow_id": flow_data.flow_id,
                    "user_id": token_data.id,
                },
                update=flow_data.model_dump(),
            )

        else:
            data = flow_data.model_dump()
            data["user_id"] = token_data.id
            data["status"] = FlowStatus.ACTIVE
            storage.power_automate_user_flows.create(data=data)

        return storage.power_automate_user_flows.verify(
            {"flow_id": flow_data.flow_id, "user_id": token_data.id}
        )

    except HTTPException as ex:
        logger.exception(ex)
        raise ex
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(
            status_code=500,
            detail="Unable to add flow",
        )


@router.get("/power_automate/flows", response_model=Page[PAUserFlow])
async def get_user_flows(
    cursor: Optional[str] = None,
    limit: int = 10,
    flow_status: Optional[FlowStatus] = None,
    token_data: TokenData = Depends(get_current_token),
):
    """
    Retrieves all flow information for a specific user.

    Returns:
        List of power automate user flows
    """
    logger = getLogger(__name__ + ".get_user_flows")
    try:
        filter = {"user_id": token_data.id}
        if flow_status is not None:
            filter["status"] = flow_status
        flows = storage.power_automate_user_flows.get_page(
            filter=filter, limit=limit, cursor=cursor
        )

        return flows
    except HTTPException as ex:
        logger.exception(ex)
        raise ex
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(
            status_code=500,
            detail="Unable to get flows",
        )


@router.get("/power_automate/flows/{flow_id}", response_model=PAUserFlow)
async def get_user_flow(
    flow_id: str = Path(description="Field ID or Object Id of Field record"),
    token_data: TokenData = Depends(get_current_token),
):
    """
    Retrieves a user flow

    Returns:
        The user flow
    """
    logger = getLogger(__name__ + ".get_user_flow")
    try:
        filter = {"user_id": token_data.id}
        try:
            filter["_id"] = ObjectId(flow_id)
        except Exception:
            filter["flow_id"] = flow_id
        flow = storage.power_automate_user_flows.verify(filter=filter)

        return flow
    except HTTPException as ex:
        logger.exception(ex)
        raise ex
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(
            status_code=500,
            detail="Unable to get flow",
        )


@router.patch("/power_automate/flows/{flow_id}", response_model=PAUserFlow)
async def update_user_flow(
    data: PAUserFlowUpdate,
    flow_id: str = Path(description="Field ID or Object Id of Field record"),
    token_data: TokenData = Depends(get_current_token),
):
    """
    Updates a user flow

    Returns:
        The user flow
    """
    logger = getLogger(__name__ + ".update_user_flow")
    try:
        update = data.model_dump(exclude_none=True, exclude_unset=True)
        filter = {"user_id": token_data.id}
        try:
            filter["_id"] = ObjectId(flow_id)
        except Exception:
            filter["flow_id"] = flow_id
        storage.power_automate_user_flows.update(filter=filter, update=update)
        flow = storage.power_automate_user_flows.verify(filter=filter)

        return flow
    except HTTPException as ex:
        logger.exception(ex)
        raise ex
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(
            status_code=500,
            detail="Unable to update flow",
        )


@router.delete(
    "/power_automate/flows/{flow_id}", response_model=Dict[str, str]
)
async def delete_user_flow(
    flow_id: str = Path(description="Field ID or Object Id of Field record"),
    token_data: TokenData = Depends(get_current_token),
):
    """
    Removes a user flow

    Returns:
        The user flow
    """
    logger = getLogger(__name__ + ".delete_user_flow")
    try:
        filter = {"user_id": token_data.id}
        try:
            filter["_id"] = ObjectId(flow_id)
        except Exception:
            filter["flow_id"] = flow_id
        storage.power_automate_user_flows.delete(filter=filter)

        message = {"message": "User flow removed"}

        return message
    except HTTPException as ex:
        logger.exception(ex)
        raise ex
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(
            status_code=500,
            detail="Unable to remove flow",
        )
