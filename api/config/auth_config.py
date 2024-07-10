from fastapi import HTTPException, status
from fastapi import Header

from api.service.auth_service import AuthService

auth_service = AuthService()


def get_current_task(authorization: str = Header(alias='Authorization')):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token scheme")
    auth_service.validate_token(authorization)
