from datetime import UTC, datetime
from typing import Dict, Generic, List, Optional, Type, TypeVar

import gridfs
from bson.objectid import ObjectId
from core.config import settings
from fastapi import HTTPException, status
from pydantic import BaseModel
from pymongo import MongoClient
from schemas import auth as s_auth
from schemas import power_automate_user_flows as s_user_flows
from schemas.page import Page

T = TypeVar("T", bound=BaseModel)


class MongoStorage(Generic[T]):
    """Generic Storage class for interfacing with mongo db"""

    client = MongoClient(settings.MONGODB_URI)

    def __init__(
        self,
        collection_name: str,
        model: Type[T],
        db_name: str = settings.DATABSE_NAME,
        update_ban: List[str] = ["_id"],
    ):
        """
        Storage object with methods to Create, Read, Update,
        Delete (CRUD) objects in the mongo database.
        """

        self.db = self.client[db_name]
        self.fs = gridfs.GridFS(self.db)
        self.model = model
        self.collection_name = collection_name
        self.collection = self.db[collection_name]
        self.update_ban = update_ban

    def create(
        self,
        data: dict,
    ) -> str:
        """Creates a db record and returns the id"""

        date = datetime.now(UTC)
        data["date_created"] = date
        data["date_modified"] = date

        id = str(self.collection.insert_one(data).inserted_id)

        return id

    def get(self, filter: Dict) -> Optional[T]:
        """Gets a record from the db using the supplied filter"""

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        res = self.collection.find_one(filter)

        if res:
            res = self.model(**res)

        return res

    def get_all(
        self, filter: Dict, limit: int = 0, sort: dict = {"_id": 1}
    ) -> List[T]:
        """Gets all records from the db using the supplied filter"""

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        res_list = self.collection.find(filter).sort(sort).limit(limit=limit)
        res_out = [self.model(**item) for item in res_list]

        return res_out

    def get_page(
        self,
        filter: Dict,
        limit: int = 0,
        cursor: Optional[str] = None,
        sort: dict = {"_id": 1},
    ) -> Page[T]:
        """Gets a page of res"""

        if cursor:
            filter["_id"] = {"$gt": ObjectId(cursor)}

        res = self.get_all(filter, limit=limit, sort=sort)

        item_count = len(res)
        next_cursor = None

        if item_count > 0:
            count_query = filter.copy()
            count_query["_id"] = {"$gt": ObjectId(res[-1].id)}
            last_item = self.get(count_query)
            if last_item and last_item.id != res[-1].id:
                next_cursor = res[-1].id

        res_page = Page(
            items=res,
            item_count=item_count,
            next_cursor=next_cursor,
        )

        return res_page

    def verify(self, filter: Dict) -> T:
        """
        Gets a record using the filter
        and raises an error if a matching record is not found
        """

        res = self.get(filter)

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.collection_name} Item not found",
            )

        return res

    def update(self, filter: Dict, update: Dict):
        """Updates a record"""
        self.verify(filter)

        for key in self.update_ban:
            if key in update:
                raise KeyError(f"Invalid Key. KEY {key} cannot be changed")
        update["date_modified"] = datetime.now(UTC)

        return self.collection.update_one(filter, {"$set": update})

    def advanced_update(self, filter: Dict, update: Dict):
        """Updates a record with more complex parameters"""
        self.verify(filter)

        if "$set" in update:
            update["$set"]["date_modified"] = datetime.now(UTC)
        else:
            update["$set"] = {"date_modified": datetime.now(UTC)}

        return self.collection.update_one(filter, update)

    def delete(self, filter: Dict):
        """Deletes a component record"""
        self.verify(filter)

        self.collection.delete_one(filter)


# platform_connections = MongoStorage(
#     collection_name="platform_connections",
#     model=s_auth.PlatformConnections,
#     update_ban=["_id", "user_id"],
# )


power_automate_user_flows = MongoStorage(
    collection_name="power_automate_user_flows",
    model=s_user_flows.PAUserFlow,
    update_ban=["_id", "user_id"],
)
