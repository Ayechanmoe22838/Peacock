import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.main import app
from app.core.database import SessionLocal
from app.core.security import create_access_token
import app.models as models

@pytest.fixture(scope="session")
def client():
    with TestClient(app, base_url="http://testserver", follow_redirects=False) as c:
        yield c

@pytest.fixture(scope="session")
def db():
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture
def admin_token(db: Session):
    admin = db.query(models.User).filter_by(email="admin@peacock.com").first()
    return create_access_token({"sub": str(admin.user_id), "role": admin.role, "email": admin.email})

@pytest.fixture
def customer_token(db: Session):
    cust = db.query(models.User).filter_by(email="customer@peacock.com").first()
    return create_access_token({"sub": str(cust.user_id), "role": cust.role, "email": cust.email})
