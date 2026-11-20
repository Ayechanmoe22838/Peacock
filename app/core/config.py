import os
from pathlib import Path
from typing import Any
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "Peacock – Smart Wedding Reception Management System"
    SECRET_KEY: str = "peacock-secret-key-secure-wedding-system-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "root"
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = "peacock_db"
    DATABASE_URL: str = "mysql+pymysql://root:root@127.0.0.1:3306/peacock_db?charset=utf8mb4"
    
    BASE_DIR: Path = BASE_DIR
    UPLOAD_DIR: Path = BASE_DIR / "media"
    
    CURRENCY_CODE: str = "MMK"
    CURRENCY_SYMBOL: str = "Ks"
    
    ADMIN_EMAIL: str = "admin@peacock.com"
    ADMIN_PASSWORD: str = "AdminPassword123!"
    ADMIN_NAME: str = "Peacock Administrator"
    
    # Official KPay account details for customer payment display
    KPAY_PHONE: str = "09450012345"
    KPAY_NAME: str = "PEACOCK WEDDING SERVICES"
    KPAY_QR_IMAGE: str = "/static/images/kpay_qr.png"

    PORT: int = 8000
    HOST: str = "0.0.0.0"
    ENVIRONMENT: str = "development"

    @model_validator(mode="before")
    @classmethod
    def assemble_db_connection(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # 1. Resolve PORT from environment if provided by Railway
            port_env = os.getenv("PORT")
            if port_env and not data.get("PORT"):
                try:
                    data["PORT"] = int(port_env)
                except ValueError:
                    pass
            
            # 2. Check for Railway MYSQL_URL or DATABASE_URL
            raw_url = (
                data.get("DATABASE_URL")
                or data.get("MYSQL_URL")
                or os.getenv("DATABASE_URL")
                or os.getenv("MYSQL_URL")
                or os.getenv("DATABASE_PUBLIC_URL")
            )
            
            # If explicit raw URL is found, normalize it for PyMySQL
            if raw_url and raw_url != "mysql+pymysql://root:root@127.0.0.1:3306/peacock_db?charset=utf8mb4":
                if raw_url.startswith("mysql://"):
                    raw_url = raw_url.replace("mysql://", "mysql+pymysql://", 1)
                if "?" not in raw_url:
                    raw_url = f"{raw_url}?charset=utf8mb4"
                data["DATABASE_URL"] = raw_url
            else:
                # 3. Check for individual Railway environment variables:
                # Railway MySQL plugin provides: MYSQLHOST, MYSQLPORT, MYSQLUSER, MYSQLPASSWORD, MYSQLDATABASE
                railway_host = os.getenv("MYSQLHOST") or os.getenv("MYSQL_HOST")
                railway_port = os.getenv("MYSQLPORT") or os.getenv("MYSQL_PORT")
                railway_user = os.getenv("MYSQLUSER") or os.getenv("MYSQL_USER")
                railway_pass = os.getenv("MYSQLPASSWORD") or os.getenv("MYSQL_PASSWORD")
                railway_db = os.getenv("MYSQLDATABASE") or os.getenv("MYSQL_DB")
                
                if railway_host or railway_user:
                    host = railway_host or "127.0.0.1"
                    port = int(railway_port or 3306)
                    user = railway_user or "root"
                    password = railway_pass or "root"
                    db = railway_db or "peacock_db"
                    
                    data["MYSQL_HOST"] = host
                    data["MYSQL_PORT"] = port
                    data["MYSQL_USER"] = user
                    data["MYSQL_PASSWORD"] = password
                    data["MYSQL_DB"] = db
                    data["DATABASE_URL"] = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"
                    
        return data

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
