import pytest

def test_login_invalid_credentials(client):
    res = client.post("/login", data={"email": "nonexistent@peacock.com", "password": "WrongPassword"})
    assert res.status_code == 200
    assert "Invalid email address or password" in res.text

def test_login_valid_admin(client):
    res = client.post("/login", data={"email": "admin@peacock.com", "password": "AdminPassword123!"})
    assert res.status_code == 303
    assert res.headers["location"] == "/admin/dashboard"
    assert "access_token" in res.cookies

def test_login_valid_customer(client):
    res = client.post("/login", data={"email": "customer@peacock.com", "password": "CustomerPassword123!"})
    assert res.status_code == 303
    assert res.headers["location"] == "/customer/dashboard"
    assert "access_token" in res.cookies

def test_unauthenticated_protected_route_redirects(client):
    client.cookies.clear()
    res = client.get("/customer/dashboard", headers={"Accept": "text/html"})
    assert res.status_code == 303
    assert "/login" in res.headers["location"]

def test_customer_cannot_access_admin_dashboard(client, customer_token):
    client.cookies.set("access_token", f"Bearer {customer_token}")
    res = client.get("/admin/dashboard")
    assert res.status_code == 403
    assert "Admin role required" in res.text

def test_admin_can_access_admin_dashboard(client, admin_token):
    client.cookies.set("access_token", f"Bearer {admin_token}")
    res = client.get("/admin/dashboard")
    assert res.status_code == 200
    assert "Administrator Dashboard" in res.text
