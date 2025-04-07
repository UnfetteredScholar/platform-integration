from typing import Annotated

from bson.errors import InvalidId
from bson.objectid import ObjectId
from pydantic import AfterValidator, BeforeValidator

PyObjectID = Annotated[str, BeforeValidator(str)]


def is_valid_obj_id(value: str) -> str:
    try:
        ObjectId(value)
    except Exception as ex:
        raise ValueError(f"{value} is not a valid object ID")

    return value


ValidIdStr = Annotated[str, AfterValidator(is_valid_obj_id)]
