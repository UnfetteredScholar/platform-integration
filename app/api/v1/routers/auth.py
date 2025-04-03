from typing import Any, Dict

import requests
from core.config import session_store, settings
from core.microsoft_auth_client import msal_client
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/auth/microsoft-login")
def microsoft_login():
    """Redirect users to Microsoft's login page"""
    auth_url = msal_client.get_authorization_request_url(
        settings.AZURE_SCOPE, redirect_uri=settings.AZURE_REDIRECT_URI
    )
    return RedirectResponse(auth_url)


@router.get("/getAToken", response_model=Dict[str, Any])
def auth_callback(request: Request):
    """Handle the authentication response from Microsoft"""
    params = dict(request.query_params)
    if "code" not in params:
        return {"error": "Authorization failed"}

    token_response = msal_client.acquire_token_by_authorization_code(
        params["code"], settings.AZURE_SCOPE, redirect_uri=settings.AZURE_REDIRECT_URI
    )

    if "access_token" in token_response:
        session_store["token"] = token_response  # Store session
        res = {"message": "Login successful", "token": token_response}
        # print(res)
        return res

    return {"error": "Failed to retrieve token", "details": token_response}


@router.get("/auth/logout", response_model=Dict[str, str])
def logout():
    """Logout user by clearing session"""
    session_store.clear()
    return {"message": "Logged out"}


@router.get("/user/profile", response_model=Dict[str, Any])
def get_user_profile():
    """Retrieve user profile using Microsoft Graph API"""
    token = session_store.get("token", {}).get("access_token")
    if not token:
        return {"error": "User not authenticated"}

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)

    return response.json()
