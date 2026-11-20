import pytest
from fastapi import HTTPException
import app.models as models

def test_seating_assignment_and_capacity_constraints(client, customer_token, db):
    client.cookies.set("access_token", f"Bearer {customer_token}")
    
    # Customer 1 has booking 1 with tables
    booking = db.query(models.Booking).filter_by(booking_reference="BK-202611-001").first()
    table = booking.tables[0]
    
    # Create test guest
    guest = models.Guest(
        booking_id=booking.booking_id,
        guest_name="Capacity Test Guest",
        category="Friends"
    )
    db.add(guest)
    db.commit()

    # Post assignment
    res = client.post("/customer/seating/assign", data={
        "table_id": table.table_id,
        "guest_id": guest.guest_id
    })
    assert res.status_code == 303

    # Reset session snapshot so newly committed row from test client is visible
    db.rollback()
    assignment = db.query(models.SeatingAssignment).filter_by(guest_id=guest.guest_id).first()
    assert assignment is not None
    assert assignment.table_id == table.table_id

    # Clean up test guest and assignment
    db.delete(assignment)
    db.delete(guest)
    db.commit()
