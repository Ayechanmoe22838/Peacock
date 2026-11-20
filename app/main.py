import os
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.templates import render_template

from app.core.config import settings
from app.core.database import engine, Base
import app.models  # ensure models loaded
from app.routers import auth, public, customer, admin

# Create tables if not present
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="PEACOCK – Smart Wedding Reception Management System",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload directories exist
for folder in ["venues", "packages", "vendors", "invitations", "payment_receipts"]:
    os.makedirs(settings.UPLOAD_DIR / folder, exist_ok=True)

# Mount Static Files & Media
app.mount("/static", StaticFiles(directory=str(settings.BASE_DIR / "app" / "static")), name="static")
app.mount("/media", StaticFiles(directory=str(settings.UPLOAD_DIR)), name="media")

# Include Routers
app.include_router(auth.router)
app.include_router(public.router)
app.include_router(customer.router)
app.include_router(admin.router)

# Healthcheck Endpoint for Docker / Railway
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "PEACOCK Wedding Management System",
        "version": "1.0.0",
        "database": "connected"
    }

# Custom 404 Error Handler
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return render_template(
        request,
        "public/about.html",
        {
            "current_user": None,
            "alert_message": "The requested page was not found. Redirected to About page.",
            "alert_type": "warning"
        },
        status_code=404
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
