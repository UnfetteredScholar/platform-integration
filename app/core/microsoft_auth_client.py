import os
from typing import Generator

from core.authentication.auth_middleware import get_current_token
from core.config import settings
from fastapi import Depends
from msal import ConfidentialClientApplication, SerializableTokenCache
from pymongo import MongoClient
from schemas.token import TokenData

AUTHORITY = f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}"


class MongoTokenCache(SerializableTokenCache):

    _client = MongoClient(settings.MONGODB_URI)
    _collection = _client[settings.DATABSE_NAME]["microsoft_connections"]

    def __init__(
        self,
        user_id: str,
    ):
        super().__init__()

        self.user_id = user_id
        self._load_cache()

    def _load_cache(self):
        record = MongoTokenCache._collection.find_one(
            {"user_id": self.user_id}
        )
        if record and "token_cache" in record:
            self.deserialize(record["token_cache"])

    def persist(self):
        if self.has_state_changed:
            serialized = self.serialize()
            MongoTokenCache._collection.update_one(
                {"user_id": self.user_id},
                {"$set": {"token_cache": serialized}},
                upsert=True,
            )
            self.has_state_changed = False

    def clear_cache(self):
        if MongoTokenCache._collection.find_one({"user_id": self.user_id}):
            MongoTokenCache._collection.delete_one({"user_id": self.user_id})


def get_token_cache(
    token_data: TokenData = Depends(get_current_token),
) -> Generator[MongoTokenCache, None, None]:
    """
    Gets the microsoft tokens for a user
    """
    cache = MongoTokenCache(user_id=token_data.id)
    try:
        yield cache
    finally:
        print("persistng cache")
        cache.persist()


def get_msal_client(
    cache: MongoTokenCache = Depends(get_token_cache),
) -> ConfidentialClientApplication:
    msal_client = ConfidentialClientApplication(
        client_id=settings.AZURE_CLIENT_ID,
        authority=AUTHORITY,
        client_credential=settings.AZURE_CLIENT_SECRET,
        token_cache=cache,
    )

    return msal_client
