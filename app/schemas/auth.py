from typing import Optional

from pydantic import AliasChoices, BaseModel, Field
from schemas.base import PyObjectID


class PlatformConnections(BaseModel):
    id: PyObjectID = Field(validation_alias=AliasChoices("_id", "id"))
    user_id: str
    microsoft_oid: Optional[str] = None
