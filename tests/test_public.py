import pytest

def test_home_page(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "Plan Your Perfect Wedding Reception" in res.text
    assert "PEACOCK" in res.text

def test_venues_list(client):
    res = client.get("/venues")
    assert res.status_code == 200
    assert "Wedding Venues" in res.text
    assert "The Grand Peacock Ballroom" in res.text

def test_venue_detail(client):
    res = client.get("/venues/1")
    assert res.status_code == 200
    assert "The Grand Peacock Ballroom" in res.text
    assert "Check Date Availability" in res.text

def test_packages_page(client):
    res = client.get("/packages")
    assert res.status_code == 200
    assert "Curated Wedding Packages" in res.text
    assert "Imperial Gold Royal Package" in res.text

def test_services_page(client):
    res = client.get("/services")
    assert res.status_code == 200
    assert "Vendors & Wedding Services" in res.text
    assert "Royal Catering Menus" in res.text

def test_about_page(client):
    res = client.get("/about")
    assert res.status_code == 200
    assert "About Peacock" in res.text

def test_contact_page(client):
    res = client.get("/contact")
    assert res.status_code == 200
    assert "PEACOCK WEDDING SERVICES" in res.text
    assert "09450012345" in res.text

def test_digital_invitation_view_and_rsvp(client):
    # Test viewing invitation via shareable token
    res = client.get("/invitation/peacock-acm-minthant-2026")
    assert res.status_code == 200
    assert ("Anirudh" in res.text or "Cherry" in res.text or "Aye Chan Moe" in res.text)
    assert "RSVP & Dietary Preferences" in res.text or "RSVP &amp; Dietary Preferences" in res.text

    # Test RSVP submission
    rsvp_payload = {
        "guest_name": "Test RSVP Guest",
        "phone": "09998877665",
        "rsvp_status": "Accepted",
        "plus_ones": 1,
        "dietary_requirements": "Vegetarian",
        "notes": "Looking forward to celebrating!"
    }
    api_res = client.post("/api/invitations/peacock-acm-minthant-2026/rsvp", json=rsvp_payload)
    assert api_res.status_code == 200
    data = api_res.json()
    assert data["success"] is True

def test_availability_api(client):
    # Check availability for a future date
    res = client.get("/api/venues/1/check-availability?date=2027-05-20&start_time=17:00&end_time=22:00")
    assert res.status_code == 200
    data = res.json()
    assert "available" in data

def test_healthcheck(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "PEACOCK" in data["service"]

def test_railway_config_url_normalization():
    from app.core.config import Settings
    # Test normalization of Railway's raw mysql:// URL
    s = Settings(DATABASE_URL="mysql://root:password@containers.railway.app:3306/railway")
    assert s.DATABASE_URL.startswith("mysql+pymysql://")
    assert "charset=utf8mb4" in s.DATABASE_URL

