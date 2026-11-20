import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.invitation_templates import INVITATION_TEMPLATES

client = TestClient(app)

def test_invitation_templates_catalog():
    """Verify all 13 exclusive stationery templates exist."""
    assert len(INVITATION_TEMPLATES) == 13
    template_ids = [t["id"] for t in INVITATION_TEMPLATES]
    assert "royal_rose" in template_ids
    assert "peacock_sapphire" in template_ids
    assert "watercolour_sunset" in template_ids

def test_public_invitation_view():
    """Test public invitation page access with shareable token."""
    response = client.get("/invitation/peacock-acm-minthant-2026")
    assert response.status_code == 200
    assert "Wedding Reception Invitation" in response.text or "Kindly Respond" in response.text

def test_public_venues_and_menus():
    """Test public services page displays both vendors and catering menus."""
    response = client.get("/services")
    assert response.status_code == 200
    assert "Vendors &amp; Wedding Services" in response.text or "Vendors & Wedding Services" in response.text
    assert "Royal Catering Menus" in response.text

def test_customer_catering_flow():
    """Test customer viewing catering catalog with login."""
    # Login as Cherry
    login_res = client.post("/login", data={
        "email": "customer@peacock.com",
        "password": "CustomerPassword123!"
    }, follow_redirects=False)
    assert login_res.status_code == 303

    # Access catering page
    cat_res = client.get("/customer/catering")
    assert cat_res.status_code == 200
    assert "Gourmet Catering" in cat_res.text
    assert "Traditional Myanmar" in cat_res.text
