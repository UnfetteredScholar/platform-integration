from enum import StrEnum
from typing import Optional

from pydantic import AliasChoices, BaseModel, Field
from schemas.base import PyObjectID


class FlowStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class PAUserFlow(BaseModel):
    id: PyObjectID = Field(validation_alias=AliasChoices("_id", "id"))
    user_id: str = Field(..., description="User Id")
    flow_id: str = Field(..., description="Unique identifier for the flow")
    flow_url: str = Field(..., description="Production URL of the flow")
    status: FlowStatus


class PAFlowIn(BaseModel):
    flow_id: str = Field(..., description="Unique identifier for the flow")
    flow_url: str = Field(..., description="Production URL of the flow")


class PAUserFlowUpdate(BaseModel):
    # flow_id: Optional[str] = None
    flow_url: Optional[str] = None
    status: Optional[FlowStatus] = None
