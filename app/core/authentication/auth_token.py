from datetime import UTC, datetime, timedelta
from typing import Any, Dict, Optional

from core.config import settings
from fastapi import HTTPException, status
from jose import JWTError, jwt
from schemas.token import ClientIdentifier, TokenData

ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_DAYS = settings.ACCESS_TOKEN_EXPIRE_DAYS

KEYS = {
    ClientIdentifier.QUEST_AI.value: settings.QUEST_AI_SECRET_KEY,
}

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
    client_id: ClientIdentifier = ClientIdentifier.QUEST_AI,
) -> str:
    """
    Creates a jwt access token using the data provided

    Args:
        data: data to be encoded into the token
        expires_delta: period of time which the token will be valid

    Returns:
        encoded jwt string
    """
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            days=int(ACCESS_TOKEN_EXPIRE_DAYS)
        )

    to_encode.update({"exp": expire, "client_id": client_id})
    encoded_jwt = jwt.encode(to_encode, KEYS[client_id], algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> TokenData:
    """
    Verifies an access token

    Args:
        token: the jwt token string

    Returns:
        TokenData object containing the data in the token
    """
    try:
        client_id = jwt.get_unverified_claims(token).get("client_id")
        payload = jwt.decode(token, KEYS[client_id], algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        id: str = payload.get("id")
        token_type: str = payload.get("type")
        role: str = payload.get("role")

        if email is None or id is None:
            raise credentials_exception

        return TokenData(
            email=email, id=id, type=token_type, role=role, client_id=client_id
        )
    except JWTError:
        raise credentials_exception
