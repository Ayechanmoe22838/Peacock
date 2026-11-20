from typing import Optional
from fastapi import Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
import app.models as models

def extract_token_from_request(request: Request) -> Optional[str]:
    # 1. Check HTTP-only cookie
    token = request.cookies.get("access_token")
    if token:
        if token.startswith("Bearer "):
            token = token[7:]
        return token
    # 2. Check Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]
    return None

def get_current_user_optional(request: Request, db: Session = Depends(get_db)) -> Optional["models.User"]:
    token = extract_token_from_request(request)
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    user = db.query(models.User).filter(models.User.user_id == int(user_id), models.User.is_active == True).first()
    return user

def get_current_user(request: Request, db: Session = Depends(get_db)) -> "models.User":
    user = get_current_user_optional(request, db)
    if not user:
        if "text/html" in request.headers.get("Accept", ""):
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                headers={"Location": f"/login?next={request.url.path}"}
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

def get_current_admin(user: "models.User" = Depends(get_current_user)) -> "models.User":
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden. Admin role required."
        )
    return user

def get_current_customer(user: "models.User" = Depends(get_current_user)) -> "models.User":
    if user.role != "customer" and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden. Customer role required."
        )
    return user
