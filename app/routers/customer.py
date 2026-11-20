import os
import shutil
from datetime import datetime, date, time
from decimal import Decimal
from typing import Optional, List
from fastapi import APIRouter, Request, Depends, Form, File, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.permissions import get_current_customer
from app.core.security import verify_password, get_password_hash, generate_shareable_token
from app.core.encryption import encrypt_data
from app.core.invitation_templates import INVITATION_TEMPLATES, get_template_image
from app.core.templates import render_template
from app.services.booking_service import create_booking
from app.services.payment_service import submit_payment
from app.services.budget_service import add_expense, recalculate_budget
from app.services.notification_service import create_notification
import app.models as models

router = APIRouter(prefix="/customer", tags=["Customer Portal"])

# ================= Dashboard Overview =================
@router.get("/dashboard", response_class=HTMLResponse)
def customer_dashboard(
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.event_date.desc()).first()

    days_left = -1
    budget = None
    budget_spent_percent = 0
    total_guests = 0
    rsvp_accepted = 0
    rsvp_pending = 0
    rsvp_declined = 0
    total_tables = 0
    seated_guests = 0
    schedules = []

    if primary_booking:
        today = date.today()
        days_left = (primary_booking.event_date - today).days
        budget = primary_booking.budget
        if budget and budget.total_budget > 0:
            budget_spent_percent = min(100, int((budget.actual_spent / budget.total_budget) * 100))

        guests = primary_booking.guests
        total_guests = len(guests)
        rsvp_accepted = sum(1 for g in guests if g.rsvp_status == "Accepted")
        rsvp_pending = sum(1 for g in guests if g.rsvp_status == "Pending")
        rsvp_declined = sum(1 for g in guests if g.rsvp_status == "Declined")

        tables = primary_booking.tables
        total_tables = len(tables)
        seated_guests = sum(len(t.assignments) for t in tables)

        schedules = primary_booking.schedules

    notifications = db.query(models.Notification).filter(
        models.Notification.user_id == user.user_id
    ).order_by(models.Notification.created_at.desc()).limit(5).all()

    return render_template(
        request=request,
        name="customer/dashboard.html",
        context={
            "current_user": user,
            "active_page": "dashboard",
            "primary_booking": primary_booking,
            "days_left": days_left,
            "budget": budget,
            "budget_spent_percent": budget_spent_percent,
            "total_guests": total_guests,
            "rsvp_accepted": rsvp_accepted,
            "rsvp_pending": rsvp_pending,
            "rsvp_declined": rsvp_declined,
            "total_tables": total_tables,
            "seated_guests": seated_guests,
            "schedules": schedules,
            "notifications": notifications
        }
    )

# ================= Profile Management =================
@router.get("/profile", response_class=HTMLResponse)
def profile_page(
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    return render_template(
        request=request,
        name="customer/profile.html",
        context={"current_user": user, "active_page": "profile"}
    )

@router.post("/profile/update")
def profile_update(
    request: Request,
    full_name: str = Form(...),
    phone: str = Form(...),
    address: str = Form(None),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    user.full_name = full_name.strip()
    user.phone = encrypt_data(phone.strip())
    user.address = address.strip() if address else None
    db.commit()
    return RedirectResponse(url="/customer/profile?success=1", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/profile/change-password")
def change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_new_password: str = Form(...),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    if not verify_password(current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Current password incorrect.")
    if new_password != confirm_new_password:
        raise HTTPException(status_code=400, detail="New passwords do not match.")
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")

    user.password_hash = get_password_hash(new_password)
    db.commit()
    return RedirectResponse(url="/customer/profile?pwd_success=1", status_code=status.HTTP_303_SEE_OTHER)

# ================= Booking Wizard =================
@router.get("/booking/wizard", response_class=HTMLResponse)
def booking_wizard_page(
    request: Request,
    venue_id: Optional[int] = None,
    package_id: Optional[int] = None,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    venues = db.query(models.Venue).filter(models.Venue.is_active == True).all()
    packages = db.query(models.Package).filter(models.Package.is_active == True).all()
    vendors = db.query(models.Vendor).filter(models.Vendor.is_active == True).all()

    return render_template(
        request=request,
        name="customer/booking_wizard.html",
        context={
            "current_user": user,
            "active_page": "booking_wizard",
            "venues": venues,
            "packages": packages,
            "vendors": vendors,
            "selected_venue_id": venue_id,
            "selected_package_id": package_id
        }
    )

@router.post("/booking/wizard")
def booking_wizard_submit(
    request: Request,
    venue_id: int = Form(...),
    package_id: Optional[str] = Form(None),
    event_date: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    guest_count: int = Form(...),
    special_requirements: Optional[str] = Form(None),
    vendor_ids: List[int] = Form([]),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    parsed_date = datetime.strptime(event_date, "%Y-%m-%d").date()
    st_parts = [int(p) for p in start_time.split(":")]
    et_parts = [int(p) for p in end_time.split(":")]
    parsed_st = time(st_parts[0], st_parts[1])
    parsed_et = time(et_parts[0], et_parts[1])

    parsed_pkg = int(package_id) if (package_id and package_id.isdigit()) else None

    try:
        booking = create_booking(
            db=db,
            customer_id=user.user_id,
            venue_id=venue_id,
            package_id=parsed_pkg,
            event_date=parsed_date,
            start_time=parsed_st,
            end_time=parsed_et,
            guest_count=guest_count,
            special_requirements=special_requirements,
            vendor_ids=vendor_ids
        )
        return RedirectResponse(
            url=f"/customer/bookings/{booking.booking_id}?created=1",
            status_code=status.HTTP_303_SEE_OTHER
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ================= Bookings List & Detail =================
@router.get("/bookings", response_class=HTMLResponse)
def customer_bookings(
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    bookings = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).all()

    return render_template(
        request=request,
        name="customer/bookings.html",
        context={"current_user": user, "active_page": "bookings", "bookings": bookings}
    )

@router.get("/bookings/{booking_id}", response_class=HTMLResponse)
def customer_booking_detail(
    request: Request,
    booking_id: int,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    booking = db.query(models.Booking).filter(
        models.Booking.booking_id == booking_id,
        models.Booking.customer_id == user.user_id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found.")

    return render_template(
        request=request,
        name="customer/booking_detail.html",
        context={"current_user": user, "active_page": "bookings", "booking": booking}
    )

@router.post("/bookings/{booking_id}/cancel")
def request_cancellation(
    booking_id: int,
    reason: str = Form(...),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    booking = db.query(models.Booking).filter(
        models.Booking.booking_id == booking_id,
        models.Booking.customer_id == user.user_id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found.")

    booking.booking_status = "Cancellation Requested"
    booking.cancellation_reason = reason.strip()
    
    db.add(models.AuditLog(
        user_id=user.user_id,
        action="CANCELLATION_REQUESTED",
        entity_type="Booking",
        entity_id=booking.booking_id,
        details=f"Customer requested cancellation for {booking.booking_reference}. Reason: {reason}"
    ))
    db.commit()

    return RedirectResponse(
        url=f"/customer/bookings/{booking.booking_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )

# ================= Vendors & Catering =================
@router.get("/vendors", response_class=HTMLResponse)
def customer_vendors(
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    vendors = db.query(models.Vendor).filter(models.Vendor.is_active == True).all()
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    return render_template(
        request=request,
        name="customer/vendors.html",
        context={"current_user": user, "active_page": "vendors", "vendors": vendors, "primary_booking": primary_booking}
    )

@router.get("/catering", response_class=HTMLResponse)
def customer_catering(
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    menus = db.query(models.Menu).filter(models.Menu.is_active == True).all()
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    selected_menus = []
    if primary_booking:
        selected_menus = db.query(models.BookingMenu).filter(
            models.BookingMenu.booking_id == primary_booking.booking_id
        ).all()

    return render_template(
        request=request,
        name="customer/catering.html",
        context={
            "current_user": user,
            "active_page": "catering",
            "menus": menus,
            "primary_booking": primary_booking,
            "selected_menus": selected_menus
        }
    )

@router.post("/catering/add-item")
def add_catering_item(
    request: Request,
    menu_id: int = Form(...),
    quantity: int = Form(...),
    dietary_notes: str = Form(None),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    if not primary_booking:
        return RedirectResponse(url="/customer/catering?error=No+active+booking+found", status_code=status.HTTP_303_SEE_OTHER)

    menu = db.query(models.Menu).filter(models.Menu.menu_id == menu_id).first()
    if not menu:
        return RedirectResponse(url="/customer/catering?error=Menu+item+not+found", status_code=status.HTTP_303_SEE_OTHER)

    if quantity <= 0:
        return RedirectResponse(url="/customer/catering?error=Quantity+must+be+greater+than+zero", status_code=status.HTTP_303_SEE_OTHER)

    unit_price = Decimal(str(menu.price_per_person))
    total_price = unit_price * Decimal(quantity)

    # Check if already added, update quantity
    existing = db.query(models.BookingMenu).filter(
        models.BookingMenu.booking_id == primary_booking.booking_id,
        models.BookingMenu.menu_id == menu_id
    ).first()

    if existing:
        existing.quantity += quantity
        existing.total_price = existing.unit_price * Decimal(existing.quantity)
        if dietary_notes:
            existing.dietary_notes = dietary_notes
    else:
        bm = models.BookingMenu(
            booking_id=primary_booking.booking_id,
            menu_id=menu.menu_id,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            dietary_notes=dietary_notes
        )
        db.add(bm)
    
    db.flush()

    # Recalculate catering cost and booking total
    all_bms = db.query(models.BookingMenu).filter(models.BookingMenu.booking_id == primary_booking.booking_id).all()
    catering_sum = sum(Decimal(str(item.total_price)) for item in all_bms)
    primary_booking.catering_cost = catering_sum
    primary_booking.total_cost = (
        Decimal(str(primary_booking.venue_cost)) +
        Decimal(str(primary_booking.package_cost)) +
        Decimal(str(primary_booking.vendors_cost)) +
        catering_sum
    )
    primary_booking.balance_amount = max(Decimal("0.00"), primary_booking.total_cost - Decimal(str(primary_booking.paid_amount)))

    # Recalculate or update budget expense
    budget = db.query(models.Budget).filter(models.Budget.booking_id == primary_booking.booking_id).first()
    if budget:
        cat_exp = db.query(models.Expense).filter(
            models.Expense.budget_id == budget.budget_id,
            models.Expense.category == "Catering"
        ).first()
        if cat_exp:
            cat_exp.estimated_cost = catering_sum
            cat_exp.actual_cost = catering_sum
        else:
            new_exp = models.Expense(
                budget_id=budget.budget_id,
                category="Catering",
                item_name="Wedding Reception Catering & Menus",
                estimated_cost=catering_sum,
                actual_cost=Decimal("0.00"),
                is_paid=False
            )
            db.add(new_exp)

        db.flush()
        all_exps = db.query(models.Expense).filter(models.Expense.budget_id == budget.budget_id).all()
        budget.estimated_cost = sum(Decimal(str(e.estimated_cost)) for e in all_exps)
        budget.actual_spent = sum(Decimal(str(e.actual_cost)) for e in all_exps if e.is_paid)
        budget.remaining_budget = max(Decimal("0.00"), Decimal(str(budget.total_budget)) - budget.actual_spent)

    db.commit()
    return RedirectResponse(url="/customer/catering?success=Menu+item+added+successfully", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/catering/remove-item/{booking_menu_id}")
def remove_catering_item(
    booking_menu_id: int,
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    if not primary_booking:
        return RedirectResponse(url="/customer/catering", status_code=status.HTTP_303_SEE_OTHER)

    bm = db.query(models.BookingMenu).filter(
        models.BookingMenu.id == booking_menu_id,
        models.BookingMenu.booking_id == primary_booking.booking_id
    ).first()

    if bm:
        db.delete(bm)
        db.flush()

        all_bms = db.query(models.BookingMenu).filter(models.BookingMenu.booking_id == primary_booking.booking_id).all()
        catering_sum = sum(Decimal(str(item.total_price)) for item in all_bms) if all_bms else Decimal("0.00")
        primary_booking.catering_cost = catering_sum
        primary_booking.total_cost = (
            Decimal(str(primary_booking.venue_cost)) +
            Decimal(str(primary_booking.package_cost)) +
            Decimal(str(primary_booking.vendors_cost)) +
            catering_sum
        )
        primary_booking.balance_amount = max(Decimal("0.00"), primary_booking.total_cost - Decimal(str(primary_booking.paid_amount)))

        # Update budget
        budget = db.query(models.Budget).filter(models.Budget.booking_id == primary_booking.booking_id).first()
        if budget:
            cat_exp = db.query(models.Expense).filter(
                models.Expense.budget_id == budget.budget_id,
                models.Expense.category == "Catering"
            ).first()
            if cat_exp:
                cat_exp.estimated_cost = catering_sum
                cat_exp.actual_cost = Decimal("0.00")
            db.flush()
            all_exps = db.query(models.Expense).filter(models.Expense.budget_id == budget.budget_id).all()
            budget.estimated_cost = sum(Decimal(str(e.estimated_cost)) for e in all_exps)
            budget.actual_spent = sum(Decimal(str(e.actual_cost)) for e in all_exps if e.is_paid)
            budget.remaining_budget = max(Decimal("0.00"), Decimal(str(budget.total_budget)) - budget.actual_spent)

        db.commit()

    return RedirectResponse(url="/customer/catering?success=Item+removed+successfully", status_code=status.HTTP_303_SEE_OTHER)

# ================= Guest Management =================
@router.get("/guests", response_class=HTMLResponse)
def customer_guests(
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    guests = primary_booking.guests if primary_booking else []
    accepted = sum(1 for g in guests if g.rsvp_status == "Accepted")
    pending = sum(1 for g in guests if g.rsvp_status == "Pending")
    declined = sum(1 for g in guests if g.rsvp_status == "Declined")

    return render_template(
        request=request,
        name="customer/guests.html",
        context={
            "current_user": user,
            "active_page": "guests",
            "guests": guests,
            "accepted_count": accepted,
            "pending_count": pending,
            "declined_count": declined
        }
    )

@router.post("/guests/add")
def add_guest(
    guest_name: str = Form(...),
    phone: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    category: str = Form("Friends"),
    rsvp_status: str = Form("Pending"),
    dietary_requirements: Optional[str] = Form(None),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    if not primary_booking:
        raise HTTPException(status_code=400, detail="Please create a wedding booking first.")

    guest = models.Guest(
        booking_id=primary_booking.booking_id,
        guest_name=guest_name.strip(),
        phone=encrypt_data(phone.strip()) if phone else None,
        email=email.strip() if email else None,
        category=category,
        rsvp_status=rsvp_status,
        dietary_requirements=dietary_requirements.strip() if dietary_requirements else None,
        invitation_token=generate_shareable_token()
    )
    db.add(guest)
    db.commit()

    return RedirectResponse(url="/customer/guests", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/guests/{guest_id}/delete")
def delete_guest(
    guest_id: int,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    guest = db.query(models.Guest).join(models.Booking).filter(
        models.Guest.guest_id == guest_id,
        models.Booking.customer_id == user.user_id
    ).first()
    if guest:
        db.delete(guest)
        db.commit()
    return RedirectResponse(url="/customer/guests", status_code=status.HTTP_303_SEE_OTHER)

# ================= Digital Invitations =================
@router.get("/invitations", response_class=HTMLResponse)
def customer_invitations(
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    invitation = primary_booking.invitation if primary_booking else None
    template_image = get_template_image(invitation.template_name if invitation else "royal_rose")

    return render_template(
        request=request,
        name="customer/invitation.html",
        context={
            "current_user": user,
            "active_page": "invitations",
            "booking": primary_booking,
            "invitation": invitation,
            "templates": INVITATION_TEMPLATES,
            "template_image": template_image
        }
    )

@router.post("/invitations/save")
def save_invitation(
    template_name: str = Form(...),
    custom_title: str = Form(...),
    custom_message: str = Form(...),
    wedding_date: str = Form(...),
    start_time: str = Form(...),
    venue_name: str = Form(...),
    venue_address: str = Form(...),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    if not primary_booking:
        raise HTTPException(status_code=400, detail="No booking found.")

    w_date = datetime.strptime(wedding_date, "%Y-%m-%d").date()
    st_parts = [int(p) for p in start_time.split(":")]
    st_time = time(st_parts[0], st_parts[1])

    invitation = primary_booking.invitation
    if not invitation:
        invitation = models.Invitation(
            booking_id=primary_booking.booking_id,
            template_name=template_name,
            custom_title=custom_title.strip(),
            custom_message=custom_message.strip(),
            wedding_date=w_date,
            start_time=st_time,
            end_time=primary_booking.end_time,
            venue_name=venue_name.strip(),
            venue_address=venue_address.strip(),
            shareable_token=generate_shareable_token()
        )
        db.add(invitation)
    else:
        invitation.template_name = template_name
        invitation.custom_title = custom_title.strip()
        invitation.custom_message = custom_message.strip()
        invitation.wedding_date = w_date
        invitation.start_time = st_time
        invitation.venue_name = venue_name.strip()
        invitation.venue_address = venue_address.strip()

    db.commit()
    return RedirectResponse(url="/customer/invitations", status_code=status.HTTP_303_SEE_OTHER)

# ================= Seating Planner =================
@router.get("/seating", response_class=HTMLResponse)
def customer_seating(
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    tables = primary_booking.tables if primary_booking else []
    
    all_guests = primary_booking.guests if primary_booking else []
    assigned_guest_ids = set()
    for t in tables:
        for a in t.assignments:
            assigned_guest_ids.add(a.guest_id)
    unassigned = [g for g in all_guests if g.guest_id not in assigned_guest_ids]

    return render_template(
        request=request,
        name="customer/seating.html",
        context={
            "current_user": user,
            "active_page": "seating",
            "tables": tables,
            "unassigned_guests": unassigned
        }
    )

@router.post("/seating/tables/add")
def add_table(
    table_number: int = Form(...),
    table_name: str = Form(...),
    capacity: int = Form(10),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    if not primary_booking:
        raise HTTPException(status_code=400, detail="No booking found.")

    tbl = models.ReceptionTable(
        booking_id=primary_booking.booking_id,
        table_number=table_number,
        table_name=table_name.strip(),
        capacity=capacity
    )
    db.add(tbl)
    db.commit()
    return RedirectResponse(url="/customer/seating", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/seating/tables/{table_id}/delete")
def delete_table(
    table_id: int,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    tbl = db.query(models.ReceptionTable).join(models.Booking).filter(
        models.ReceptionTable.table_id == table_id,
        models.Booking.customer_id == user.user_id
    ).first()
    if tbl:
        db.delete(tbl)
        db.commit()
    return RedirectResponse(url="/customer/seating", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/seating/assign")
def assign_seat(
    table_id: int = Form(...),
    guest_id: int = Form(...),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    table = db.query(models.ReceptionTable).join(models.Booking).filter(
        models.ReceptionTable.table_id == table_id,
        models.Booking.customer_id == user.user_id
    ).first()
    guest = db.query(models.Guest).join(models.Booking).filter(
        models.Guest.guest_id == guest_id,
        models.Booking.customer_id == user.user_id
    ).first()

    if not table or not guest:
        raise HTTPException(status_code=400, detail="Invalid table or guest assignment.")

    if len(table.assignments) >= table.capacity:
        raise HTTPException(status_code=400, detail="Table capacity reached.")

    existing = db.query(models.SeatingAssignment).filter(
        models.SeatingAssignment.guest_id == guest_id
    ).first()
    if existing:
        existing.table_id = table_id
    else:
        assignment = models.SeatingAssignment(table_id=table_id, guest_id=guest_id)
        db.add(assignment)

    db.commit()
    return RedirectResponse(url="/customer/seating", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/seating/unassign/{assignment_id}")
def unassign_seat(
    assignment_id: int,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    assign = db.query(models.SeatingAssignment).join(models.ReceptionTable).join(models.Booking).filter(
        models.SeatingAssignment.assignment_id == assignment_id,
        models.Booking.customer_id == user.user_id
    ).first()
    if assign:
        db.delete(assign)
        db.commit()
    return RedirectResponse(url="/customer/seating", status_code=status.HTTP_303_SEE_OTHER)

# ================= Budget Tracker =================
@router.get("/budget", response_class=HTMLResponse)
def customer_budget(
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    budget = primary_booking.budget if primary_booking else None
    expenses = budget.expenses if budget else []

    return render_template(
        request=request,
        name="customer/budget.html",
        context={
            "current_user": user,
            "active_page": "budget",
            "budget": budget,
            "expenses": expenses
        }
    )

@router.post("/budget/set-total")
def set_total_budget(
    total_budget: Decimal = Form(...),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    if primary_booking and primary_booking.budget:
        primary_booking.budget.total_budget = total_budget
        recalculate_budget(db, primary_booking.budget.budget_id)

    return RedirectResponse(url="/customer/budget", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/budget/expenses/add")
def add_budget_expense(
    item_name: str = Form(...),
    category: str = Form(...),
    estimated_cost: Decimal = Form(...),
    actual_cost: Decimal = Form(Decimal("0.00")),
    is_paid: bool = Form(False),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    if primary_booking and primary_booking.budget:
        add_expense(
            db=db,
            budget_id=primary_booking.budget.budget_id,
            category=category,
            item_name=item_name.strip(),
            estimated_cost=estimated_cost,
            actual_cost=actual_cost,
            is_paid=is_paid
        )

    return RedirectResponse(url="/customer/budget", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/budget/expenses/{expense_id}/delete")
def delete_budget_expense(
    expense_id: int,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    exp = db.query(models.Expense).join(models.Budget).join(models.Booking).filter(
        models.Expense.expense_id == expense_id,
        models.Booking.customer_id == user.user_id
    ).first()
    if exp:
        b_id = exp.budget_id
        db.delete(exp)
        db.commit()
        recalculate_budget(db, b_id)
    return RedirectResponse(url="/customer/budget", status_code=status.HTTP_303_SEE_OTHER)

# ================= Payments & KBZPay Workflow =================
@router.get("/payments", response_class=HTMLResponse)
def customer_payments(
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    payments = primary_booking.payments if primary_booking else []

    return render_template(
        request=request,
        name="customer/payments.html",
        context={
            "current_user": user,
            "active_page": "payments",
            "primary_booking": primary_booking,
            "payments": payments
        }
    )

@router.post("/payments/submit")
def submit_customer_payment(
    booking_id: int = Form(...),
    amount: Decimal = Form(...),
    payment_method: str = Form("KBZPay"),
    transaction_reference: str = Form(...),
    notes: Optional[str] = Form(None),
    receipt_file: Optional[UploadFile] = File(None),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    booking = db.query(models.Booking).filter(
        models.Booking.booking_id == booking_id,
        models.Booking.customer_id == user.user_id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found.")

    receipt_url = None
    if receipt_file and receipt_file.filename:
        safe_name = f"receipt_{booking.booking_reference}_{int(datetime.utcnow().timestamp())}.jpg"
        save_path = settings.UPLOAD_DIR / "payment_receipts" / safe_name
        os.makedirs(save_path.parent, exist_ok=True)
        with open(save_path, "wb") as f:
            shutil.copyfileobj(receipt_file.file, f)
        receipt_url = f"/media/payment_receipts/{safe_name}"

    submit_payment(
        db=db,
        booking_id=booking.booking_id,
        amount=amount,
        payment_method=payment_method,
        transaction_reference=transaction_reference.strip(),
        receipt_image=receipt_url,
        notes=notes
    )

    return RedirectResponse(url="/customer/payments?submitted=1", status_code=status.HTTP_303_SEE_OTHER)

# ================= Schedules Timeline =================
@router.get("/schedules", response_class=HTMLResponse)
def customer_schedules(
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    schedules = primary_booking.schedules if primary_booking else []

    return render_template(
        request=request,
        name="customer/schedules.html",
        context={
            "current_user": user,
            "active_page": "schedules",
            "schedules": schedules
        }
    )

@router.post("/schedules/add")
def add_schedule_activity(
    activity_name: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    description: Optional[str] = Form(None),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    primary_booking = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id
    ).order_by(models.Booking.created_at.desc()).first()

    if not primary_booking:
        raise HTTPException(status_code=400, detail="No booking found.")

    st_parts = [int(p) for p in start_time.split(":")]
    et_parts = [int(p) for p in end_time.split(":")]
    st = time(st_parts[0], st_parts[1])
    et = time(et_parts[0], et_parts[1])

    order_idx = len(primary_booking.schedules) + 1

    act = models.EventSchedule(
        booking_id=primary_booking.booking_id,
        activity_name=activity_name.strip(),
        start_time=st,
        end_time=et,
        description=description.strip() if description else None,
        order_index=order_idx
    )
    db.add(act)
    db.commit()

    return RedirectResponse(url="/customer/schedules", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/schedules/{schedule_id}/delete")
def delete_schedule_activity(
    schedule_id: int,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    act = db.query(models.EventSchedule).join(models.Booking).filter(
        models.EventSchedule.schedule_id == schedule_id,
        models.Booking.customer_id == user.user_id
    ).first()
    if act:
        db.delete(act)
        db.commit()
    return RedirectResponse(url="/customer/schedules", status_code=status.HTTP_303_SEE_OTHER)

# ================= Notifications =================
@router.get("/notifications", response_class=HTMLResponse)
def customer_notifications(
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    notifs = db.query(models.Notification).filter(
        models.Notification.user_id == user.user_id
    ).order_by(models.Notification.created_at.desc()).all()

    return render_template(
        request=request,
        name="customer/notifications.html",
        context={"current_user": user, "active_page": "notifications", "notifications": notifs}
    )

@router.post("/notifications/mark-all-read")
def mark_notifications_read(
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    db.query(models.Notification).filter(
        models.Notification.user_id == user.user_id,
        models.Notification.is_read == False
    ).update({"is_read": True})
    db.commit()
    return RedirectResponse(url="/customer/notifications", status_code=status.HTTP_303_SEE_OTHER)

# ================= Feedback =================
@router.get("/feedback", response_class=HTMLResponse)
def customer_feedback(
    request: Request,
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    completed_bookings = db.query(models.Booking).filter(
        models.Booking.customer_id == user.user_id,
        models.Booking.booking_status == "Completed"
    ).all()

    feedbacks = db.query(models.Feedback).filter(
        models.Feedback.customer_id == user.user_id
    ).order_by(models.Feedback.created_at.desc()).all()

    return render_template(
        request=request,
        name="customer/feedback.html",
        context={
            "current_user": user,
            "active_page": "feedback",
            "completed_bookings": completed_bookings,
            "feedbacks": feedbacks
        }
    )

@router.post("/feedback/submit")
def submit_feedback(
    booking_id: int = Form(...),
    rating: int = Form(...),
    review_title: str = Form(...),
    comments: str = Form(...),
    user: models.User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    booking = db.query(models.Booking).filter(
        models.Booking.booking_id == booking_id,
        models.Booking.customer_id == user.user_id,
        models.Booking.booking_status == "Completed"
    ).first()
    if not booking:
        raise HTTPException(status_code=400, detail="Reviews can only be submitted for completed wedding bookings.")

    fb = models.Feedback(
        booking_id=booking.booking_id,
        customer_id=user.user_id,
        rating=rating,
        review_title=review_title.strip(),
        comments=comments.strip(),
        is_approved=True
    )
    db.add(fb)
    db.commit()
    return RedirectResponse(url="/customer/feedback?submitted=1", status_code=status.HTTP_303_SEE_OTHER)
