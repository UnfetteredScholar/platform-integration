import os

import requests
from core.config import settings
from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from flows import quest_flows
from msal import ConfidentialClientApplication

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# MS Identity Credentials
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = os.getenv("AZURE_REDIRECT_URI")
SCOPE = [
    "https://management.azure.com/user_impersonation",
    "User.Read",
]  # ["User.Read"]

# MSAL Client
msal_client = ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)
print(REDIRECT_URI)

# In-memory session (Replace with Redis/Database for production)
session_store = {}


@app.get("/auth/login")
def login():
    """Redirect users to Microsoft's login page"""
    auth_url = msal_client.get_authorization_request_url(
        SCOPE, redirect_uri=REDIRECT_URI
    )
    return RedirectResponse(auth_url)


@app.get("/getAToken")
def auth_callback(request: Request):
    """Handle the authentication response from Microsoft"""
    params = dict(request.query_params)
    if "code" not in params:
        return {"error": "Authorization failed"}

    token_response = msal_client.acquire_token_by_authorization_code(
        params["code"], SCOPE, redirect_uri=REDIRECT_URI
    )

    if "access_token" in token_response:
        session_store["token"] = token_response  # Store session
        res = {"message": "Login successful", "token": token_response}
        print(res)
        return res

    return {"error": "Failed to retrieve token", "details": token_response}


@app.get("/auth/logout")
def logout():
    """Logout user by clearing session"""
    session_store.clear()
    return {"message": "Logged out"}


@app.get("/user/profile")
def get_user_profile():
    """Retrieve user profile using Microsoft Graph API"""
    token = session_store.get("token", {}).get("access_token")
    if not token:
        return {"error": "User not authenticated"}

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)

    return response.json()


################################################################################################
BASE_URL = "https://api.flow.microsoft.com"


@app.get("/get_environments")
def get_environments():
    """Fetch available Power Automate environments."""
    token = session_store.get("token", {}).get("access_token")
    # if "error" in token:
    #     return redirect(url_for("login"))

    URL = f"{BASE_URL}/providers/Microsoft.ProcessSimple/environments?api-version=2016-11-01"

    api_result = requests.get(
        URL,
        headers={"Authorization": "Bearer " + token},
        timeout=30,
    ).json()
    return api_result


@app.post("/upload_flow")
def upload_flow(environment_id: str = Body(embed=True)):
    """Upload a Power Automate flow from a zip file."""
    token = session_store.get("token", {}).get("access_token")
    # if "error" in token:
    #     return redirect(url_for("login"))

    # Get environment ID from request

    URL = f"{BASE_URL}/providers/Microsoft.ProcessSimple/environments/{environment_id}/flows?api-version=2016-11-01"
    responses = []
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

        responses.append(
            {
                "flowID": api_result.get("name"),
                "flowName": api_result.get("properties", {}).get("displayName"),
            }
        )
        # responses.append(api_result)
    return responses
