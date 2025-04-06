from logging import getLogger
from typing import Any, Dict

import requests
from core.authentication.auth_middleware import get_current_token
from core.config import session_store, settings
from core.microsoft_auth_client import get_account, msal_client, refresh_cache
from fastapi import APIRouter, Body, Depends, HTTPException
from schemas.token import TokenData

router = APIRouter()


@router.get("/auth/microsoft-login", response_model=Dict[str, str])
def microsoft_login(
    token_data: TokenData = Depends(get_current_token),
):
    """Redirect users to Microsoft's login page"""
    auth_url = msal_client.get_authorization_request_url(
        settings.AZURE_SCOPE, redirect_uri=settings.AZURE_REDIRECT_URI
    )
    res = {"login_url": auth_url}
    return res


@router.post("/auth/microsoft-get-token", response_model=Dict[str, str])
def microsoft_auth_callback(
    code: str = Body(embed=True),
    token_data: TokenData = Depends(get_current_token),
):
    """Exchange code from Microsoft for Auth Token"""
    logger = getLogger(__name__ + ".microsoft_auth_callback")
    try:
        token_response = msal_client.acquire_token_by_authorization_code(
            code=code,
            scopes=settings.AZURE_SCOPE,
            redirect_uri=settings.AZURE_REDIRECT_URI,
        )

        if "access_token" in token_response:
            session_store[token_data.id] = token_response["id_token_claims"][
                "oid"
            ]
            # logger.info(token_response)
            # logger.info(msal_client.get_accounts())
            res = {"message": "Login successful"}
            return res
        else:
            logger.error(token_response)
            raise HTTPException(
                status_code=400, detail="Unable to complete authentication"
            )
    except HTTPException as ex:
        logger.exception(ex)
        raise ex
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(
            status_code=500,
            detail="Unable to connect account",
        )
    finally:
        refresh_cache()


@router.get("/auth/logout", response_model=Dict[str, str])
def logout(
    token_data: TokenData = Depends(get_current_token),
):
    """Logout user by clearing session"""
    logger = getLogger(__name__ + ".logout")
    try:
        if token_data.id not in session_store:
            raise HTTPException(
                status_code=400, detail="Outlook not connected"
            )
        oid = session_store[token_data.id]
        del session_store[token_data.id]
        msal_client.token_cache.remove_account(get_account(oid))
        return {"message": "Logged out"}
    except HTTPException as ex:
        logger.exception(ex)
        raise ex
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(
            status_code=500,
            detail="Unable to remove connection",
        )
    finally:
        refresh_cache()


@router.get("/user/profile", response_model=Dict[str, Any])
def get_user_profile(
    token_data: TokenData = Depends(get_current_token),
):
    """Retrieve user profile using Microsoft Graph API"""
    oid = session_store[token_data.id]
    token = msal_client.acquire_token_silent(
        scopes=settings.AZURE_SCOPE, account=get_account(oid)
    ).get("access_token")
    if not token:
        return HTTPException(status_code=400, detail="User not authenticated")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me", headers=headers
    )

    return response.json()
