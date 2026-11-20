import pytest

def test_admin_reports_page(client, admin_token):
    client.cookies.set("access_token", f"Bearer {admin_token}")
    res = client.get("/admin/reports")
    assert res.status_code == 200
    assert "Management Reports & Analytics" in res.text

def test_export_bookings_csv(client, admin_token):
    client.cookies.set("access_token", f"Bearer {admin_token}")
    res = client.get("/admin/reports/export/csv?type=bookings")
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]
    assert "Reference,Customer,Venue,Event Date" in res.text

def test_export_payments_csv(client, admin_token):
    client.cookies.set("access_token", f"Bearer {admin_token}")
    res = client.get("/admin/reports/export/csv?type=payments")
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]
    assert "Reference,Booking Ref,Customer,Amount (MMK)" in res.text

def test_export_bookings_pdf(client, admin_token):
    client.cookies.set("access_token", f"Bearer {admin_token}")
    res = client.get("/admin/reports/export/pdf?type=bookings")
    assert res.status_code == 200
    assert "application/pdf" in res.headers["content-type"]
    assert len(res.content) > 1000
    assert res.content.startswith(b"%PDF")

def test_export_payments_pdf(client, admin_token):
    client.cookies.set("access_token", f"Bearer {admin_token}")
    res = client.get("/admin/reports/export/pdf?type=payments")
    assert res.status_code == 200
    assert "application/pdf" in res.headers["content-type"]
    assert len(res.content) > 1000
    assert res.content.startswith(b"%PDF")
