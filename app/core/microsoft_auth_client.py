from core.config import settings
from msal import ConfidentialClientApplication

AUTHORITY = f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}"
SCOPE = [
    "https://management.azure.com/user_impersonation",
]  # ["User.Read"]


msal_client = ConfidentialClientApplication(
    settings.AZURE_CLIENT_ID,
    authority=AUTHORITY,
    client_credential=settings.AZURE_CLIENT_SECRET,
)
