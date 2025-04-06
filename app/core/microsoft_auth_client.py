import os

from core.config import settings
from msal import ConfidentialClientApplication, SerializableTokenCache

cache = SerializableTokenCache()
if os.path.exists("token_cache.bin"):
    cache.deserialize(open("token_cache.bin", "r").read())

AUTHORITY = f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}"
SCOPE = [
    "https://management.azure.com/user_impersonation",
]  # ["User.Read"]


msal_client = ConfidentialClientApplication(
    client_id=settings.AZURE_CLIENT_ID,
    authority=AUTHORITY,
    client_credential=settings.AZURE_CLIENT_SECRET,
    token_cache=cache,
)


def refresh_cache():
    if cache.has_state_changed:
        with open("token_cache.bin", "w") as f:
            f.write(cache.serialize())


def get_account(oid: str) -> dict:
    """Gets the account object using the oid"""
    accounts = msal_client.get_accounts()

    for account in accounts:
        if account["local_account_id"] == oid:
            return account

    raise Exception("Microsoft credentials not found")
