from datetime import timedelta
from fastapi import APIRouter, Request, Depends, Form, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.encryption import encrypt_data
from app.core.permissions import get_current_user_optional
from app.core.templates import render_template
import app.models as models

router = APIRouter(tags=["Authentication"])

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, next: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    if current_user:
        if current_user.role == "admin":
            return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        return RedirectResponse(url="/customer/dashboard", status_code=status.HTTP_303_SEE_OTHER)

    return render_template(
        request=request,
        name="public/login.html",
        context={"current_user": None, "next_url": next, "error": None}
    )

@router.post("/login", response_class=HTMLResponse)
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    next: str = Form(None),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email.strip().lower()).first()
    if not user or not verify_password(password, user.password_hash):
        return render_template(
            request=request,
            name="public/login.html",
            context={"current_user": None, "next_url": next, "error": "Invalid email address or password."},
            status_code=200
        )

    if not user.is_active:
        return render_template(
            request=request,
            name="public/login.html",
            context={"current_user": None, "next_url": next, "error": "Your account has been deactivated. Please contact support."},
            status_code=200
        )

    # Issue access token
    access_token = create_access_token(
        data={"sub": str(user.user_id), "role": user.role, "email": user.email}
    )

    dest = next if (next and next.startswith("/")) else ("/admin/dashboard" if user.role == "admin" else "/customer/dashboard")
    
    response = RedirectResponse(url=dest, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False
    )

    db.add(models.AuditLog(
        user_id=user.user_id,
        action="USER_LOGIN",
        entity_type="User",
        entity_id=user.user_id,
        details=f"User {user.email} logged in successfully."
    ))
    db.commit()

    return response

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    if current_user:
        return RedirectResponse(url="/customer/dashboard", status_code=status.HTTP_303_SEE_OTHER)

    return render_template(
        request=request,
        name="public/register.html",
        context={"current_user": None, "error": None, "form_data": {}}
    )

@router.post("/register", response_class=HTMLResponse)
def register_submit(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    address: str = Form(None),
    db: Session = Depends(get_db)
):
    form_data = {"full_name": full_name, "email": email, "phone": phone, "address": address}

    if password != confirm_password:
        return render_template(
            request=request,
            name="public/register.html",
            context={"current_user": None, "error": "Passwords do not match.", "form_data": form_data},
            status_code=200
        )

    if len(password) < 6:
        return render_template(
            request=request,
            name="public/register.html",
            context={"current_user": None, "error": "Password must be at least 6 characters long.", "form_data": form_data},
            status_code=200
        )

    clean_email = email.strip().lower()
    existing = db.query(models.User).filter(models.User.email == clean_email).first()
    if existing:
        return render_template(
            request=request,
            name="public/register.html",
            context={"current_user": None, "error": "An account with this email already exists. Please log in.", "form_data": form_data},
            status_code=200
        )

    new_user = models.User(
        full_name=full_name.strip(),
        email=clean_email,
        phone=encrypt_data(phone.strip()),
        password_hash=get_password_hash(password),
        address=address.strip() if address else None,
        role="customer",
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(
        data={"sub": str(new_user.user_id), "role": new_user.role, "email": new_user.email}
    )

    response = RedirectResponse(url="/customer/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False
    )

    db.add(models.Notification(
        user_id=new_user.user_id,
        title="Welcome to Peacock!",
        message="Your wedding planning journey begins here. Browse our magnificent ballrooms and start reserving your date.",
        notification_type="system",
        link_url="/venues"
    ))
    db.commit()

    return response

@router.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response
