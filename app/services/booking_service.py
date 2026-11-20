import random
from datetime import datetime, date, time
from decimal import Decimal
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import app.models as models
from app.services.notification_service import create_notification, notify_admins

def check_venue_availability(
    db: Session,
    venue_id: int,
    event_date: date,
    start_time: time,
    end_time: time,
    exclude_booking_id: Optional[int] = None
) -> Tuple[bool, str]:
    """
    Check if a venue is available on a specific date and time slot.
    Returns (is_available, reason).
    """
    # 1. Check if venue exists and is active
    venue = db.query(models.Venue).filter(models.Venue.venue_id == venue_id).first()
    if not venue:
        return False, "Venue not found."
    if not venue.is_active or venue.status != "active":
        return False, f"Venue '{venue.venue_name}' is currently unavailable for bookings."

    # 2. Check if explicitly marked unavailable in VenueAvailability
    unavail = db.query(models.VenueAvailability).filter(
        models.VenueAvailability.venue_id == venue_id,
        models.VenueAvailability.date == event_date,
        models.VenueAvailability.is_available == False
    ).first()
    if unavail:
        reason = unavail.reason or "Venue is reserved or under scheduled maintenance."
        return False, f"Date unavailable: {reason}"

    # 3. Check for overlapping Confirmed or Approved bookings
    # Overlap condition: start_time < existing_end and end_time > existing_start
    query = db.query(models.Booking).filter(
        models.Booking.venue_id == venue_id,
        models.Booking.event_date == event_date,
        models.Booking.booking_status.in_(["Approved", "Confirmed"]),
        models.Booking.start_time < end_time,
        models.Booking.end_time > start_time
    )
    if exclude_booking_id:
        query = query.filter(models.Booking.booking_id != exclude_booking_id)

    overlapping = query.first()
    if overlapping:
        return False, f"Venue already has a confirmed event on {event_date} between {overlapping.start_time.strftime('%H:%M')} and {overlapping.end_time.strftime('%H:%M')}."

    return True, "Venue is available."

def generate_booking_reference() -> str:
    now_str = datetime.utcnow().strftime("%Y%m")
    random_num = random.randint(100, 999)
    return f"BK-{now_str}-{random_num}"

def create_booking(
    db: Session,
    customer_id: int,
    venue_id: int,
    package_id: Optional[int],
    event_date: date,
    start_time: time,
    end_time: time,
    guest_count: int,
    special_requirements: Optional[str] = None,
    vendor_ids: Optional[List[int]] = None,
    catering_items: Optional[List[dict]] = None
) -> models.Booking:
    """
    Validates venue availability, calculates exact MMK costs, creates booking, budget, and default schedule.
    """
    is_avail, reason = check_venue_availability(db, venue_id, event_date, start_time, end_time)
    if not is_avail:
        raise ValueError(reason)

    venue = db.query(models.Venue).filter(models.Venue.venue_id == venue_id).first()
    if guest_count > venue.capacity:
        raise ValueError(f"Guest count ({guest_count}) exceeds maximum venue capacity ({venue.capacity}).")

    venue_cost = venue.base_price
    package_cost = Decimal("0.00")
    if package_id:
        pkg = db.query(models.Package).filter(models.Package.package_id == package_id, models.Package.is_active == True).first()
        if pkg:
            package_cost = pkg.price

    # Vendors cost
    vendors_cost = Decimal("0.00")
    selected_vendors = []
    if vendor_ids:
        for vid in vendor_ids:
            vend = db.query(models.Vendor).filter(models.Vendor.vendor_id == vid, models.Vendor.is_active == True).first()
            if vend:
                selected_vendors.append(vend)
                vendors_cost += vend.price

    # Catering cost
    catering_cost = Decimal("0.00")
    selected_menus = []
    if catering_items:
        for ci in catering_items:
            mid = ci.get("menu_id")
            qty = ci.get("quantity", guest_count)
            menu_obj = db.query(models.Menu).filter(models.Menu.menu_id == mid, models.Menu.is_active == True).first()
            if menu_obj and qty > 0:
                item_total = menu_obj.price_per_person * Decimal(qty)
                catering_cost += item_total
                selected_menus.append((menu_obj, qty, item_total))

    total_cost = venue_cost + package_cost + vendors_cost + catering_cost
    balance_amount = total_cost

    ref = generate_booking_reference()
    while db.query(models.Booking).filter_by(booking_reference=ref).first():
        ref = generate_booking_reference()

    booking = models.Booking(
        booking_reference=ref,
        customer_id=customer_id,
        venue_id=venue_id,
        package_id=package_id,
        event_date=event_date,
        start_time=start_time,
        end_time=end_time,
        guest_count=guest_count,
        special_requirements=special_requirements,
        venue_cost=venue_cost,
        package_cost=package_cost,
        vendors_cost=vendors_cost,
        catering_cost=catering_cost,
        total_cost=total_cost,
        paid_amount=Decimal("0.00"),
        balance_amount=balance_amount,
        booking_status="Pending"
    )
    db.add(booking)
    db.flush()

    # Add vendor associations
    for vend in selected_vendors:
        db.add(models.BookingVendor(
            booking_id=booking.booking_id,
            vendor_id=vend.vendor_id,
            price_agreed=vend.price,
            notes=f"Selected during booking creation ({vend.category})"
        ))

    # Add catering associations
    for menu_obj, qty, item_total in selected_menus:
        db.add(models.BookingMenu(
            booking_id=booking.booking_id,
            menu_id=menu_obj.menu_id,
            quantity=qty,
            unit_price=menu_obj.price_per_person,
            total_price=item_total,
            dietary_notes=None
        ))

    # Automatically create Budget entity
    budget = models.Budget(
        booking_id=booking.booking_id,
        total_budget=total_cost,
        estimated_cost=total_cost,
        actual_spent=Decimal("0.00"),
        remaining_budget=total_cost,
        notes=f"Auto-generated budget for booking {ref}"
    )
    db.add(budget)
    db.flush()

    # Add initial standard expenses
    db.add(models.Expense(
        budget_id=budget.budget_id,
        category="Venue",
        item_name=f"{venue.venue_name} Base Charge",
        estimated_cost=venue_cost,
        actual_cost=Decimal("0.00"),
        is_paid=False
    ))
    if package_cost > 0:
        db.add(models.Expense(
            budget_id=budget.budget_id,
            category="Package",
            item_name="Wedding Package Service Fee",
            estimated_cost=package_cost,
            actual_cost=Decimal("0.00"),
            is_paid=False
        ))

    # Initialize standard event schedule timeline
    schedules = [
        ("Guest Arrival & Reception", start_time, time((start_time.hour + 1) % 24, start_time.minute), "Welcome drinks and guest registration", 1),
        ("Main Wedding Ceremony", time((start_time.hour + 1) % 24, start_time.minute), time((start_time.hour + 2) % 24, start_time.minute), "Vows, rings exchange, speeches", 2),
        ("Banquet Dinner Service", time((start_time.hour + 2) % 24, start_time.minute), time((start_time.hour + 3) % 24, start_time.minute), "Catering service and music performance", 3),
        ("Celebration & Photo Sessions", time((start_time.hour + 3) % 24, start_time.minute), end_time, "Cake cutting, bouquet toss, photos", 4)
    ]
    for name, s_t, e_t, desc, ord_idx in schedules:
        db.add(models.EventSchedule(
            booking_id=booking.booking_id,
            activity_name=name,
            start_time=s_t,
            end_time=e_t,
            description=desc,
            order_index=ord_idx
        ))

    # Notifications
    create_notification(
        db, customer_id,
        "Booking Request Submitted",
        f"Your booking request {ref} has been received. Our team will review and respond shortly.",
        "booking",
        f"/customer/bookings/{booking.booking_id}"
    )
    notify_admins(
        db,
        "New Booking Request",
        f"New booking request {ref} submitted for {venue.venue_name} on {event_date}.",
        "booking",
        f"/admin/bookings"
    )

    # Audit log
    db.add(models.AuditLog(
        user_id=customer_id,
        action="BOOKING_CREATED",
        entity_type="Booking",
        entity_id=booking.booking_id,
        details=f"Created booking {ref} for venue {venue.venue_name} on {event_date} with total {total_cost} MMK."
    ))

    db.commit()
    db.refresh(booking)
    return booking
