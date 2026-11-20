from typing import Any, Dict, Optional
from fastapi import Request
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.core.encryption import decrypt_data

templates = Jinja2Templates(directory=str(settings.BASE_DIR / "app" / "templates"))

# Register custom Jinja2 template filters
templates.env.filters["decrypt_phone"] = lambda val: decrypt_data(val) if val else ""
templates.env.filters["currency"] = lambda val: f"{val:,.2f} MMK" if val is not None else "0.00 MMK"

def render_template(
    request: Request,
    name: str,
    context: Optional[Dict[str, Any]] = None,
    status_code: int = 200
):
    ctx = context.copy() if context else {}
    if "request" not in ctx:
        ctx["request"] = request
    if "settings" not in ctx:
        ctx["settings"] = settings
    return templates.TemplateResponse(
        request=request,
        name=name,
        context=ctx,
        status_code=status_code
    )
