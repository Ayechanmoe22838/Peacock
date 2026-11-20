from datetime import date, time
from decimal import Decimal
import pytest
from app.services.booking_service import create_booking, check_venue_availability
import app.models as models

def test_booking_cost_calculation_and_budget_creation(db):
    cust = db.query(models.User).filter_by(email="customer@peacock.com").first()
    venue = db.query(models.Venue).filter_by(venue_id=1).first()
    package = db.query(models.Package).filter_by(package_id=1).first()
    
    test_date = date(2027, 8, 15)
    booking = create_booking(
        db=db,
        customer_id=cust.user_id,
        venue_id=venue.venue_id,
        package_id=package.package_id,
        event_date=test_date,
        start_time=time(16, 0),
        end_time=time(21, 0),
        guest_count=200,
        special_requirements="Test automated booking creation"
    )

    assert booking.booking_id is not None
    assert booking.total_cost == venue.base_price + package.price
    assert booking.balance_amount == booking.total_cost
    assert booking.booking_status == "Pending"

    # Verify auto-generated budget
    assert booking.budget is not None
    assert booking.budget.total_budget == booking.total_cost
    assert len(booking.schedules) > 0

    # Clean up test booking
    db.delete(booking)
    db.commit()

def test_overlapping_confirmed_booking_is_prevented(db):
    # Venue 1 has a confirmed booking on 2026-12-28 from 17:00 to 22:00
    is_avail, reason = check_venue_availability(
        db=db,
        venue_id=1,
        event_date=date(2026, 12, 28),
        start_time=time(18, 0),
        end_time=time(21, 0)
    )
    assert is_avail is False
    assert "already has a confirmed event" in reason
