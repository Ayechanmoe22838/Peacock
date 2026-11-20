from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, HTTPException, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from app.core.templates import render_template
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.core.config import settings
from app.core.database import get_db
from app.core.permissions import get_current_admin
from app.services.payment_service import verify_payment
from app.services.report_service import generate_bookings_csv, generate_payments_csv, generate_pdf_report
from app.services.notification_service import create_notification
import app.models as models

router = APIRouter(prefix="/admin", tags=["Admin Management"])

# ================= Admin Dashboard Overview =================
@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    total_customers = db.query(models.User).filter(models.User.role == "customer").count()
    total_venues = db.query(models.Venue).filter(models.Venue.is_active == True).count()
    total_bookings = db.query(models.Booking).count()
    pending_bookings_count = db.query(models.Booking).filter(models.Booking.booking_status == "Pending").count()
    confirmed_bookings_count = db.query(models.Booking).filter(models.Booking.booking_status == "Confirmed").count()

    total_revenue = db.query(func.coalesce(func.sum(models.Payment.amount), Decimal("0.00"))).filter(
        models.Payment.payment_status == "Verified"
    ).scalar()

    pending_bookings = db.query(models.Booking).filter(
        models.Booking.booking_status == "Pending"
    ).order_by(models.Booking.created_at.desc()).limit(5).all()

    pending_payments = db.query(models.Payment).filter(
        models.Payment.payment_status == "Pending Verification"
    ).order_by(models.Payment.created_at.desc()).limit(5).all()

    return render_template(
        request,
        "admin/dashboard.html",
        {
            "current_user": admin,
            "active_page": "dashboard",
            "total_customers": total_customers,
            "total_venues": total_venues,
            "total_bookings": total_bookings,
            "pending_bookings_count": pending_bookings_count,
            "confirmed_bookings_count": confirmed_bookings_count,
            "total_revenue": total_revenue,
            "pending_bookings": pending_bookings,
            "pending_payments": pending_payments
        }
    )

# ================= Booking Management =================
@router.get("/bookings", response_class=HTMLResponse)
def admin_bookings(
    request: Request,
    q: Optional[str] = None,
    status: Optional[str] = None,
    venue_id: Optional[int] = None,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    query = db.query(models.Booking)

    if q:
        query = query.join(models.User).filter(or_(
            models.Booking.booking_reference.ilike(f"%{q}%"),
            models.User.full_name.ilike(f"%{q}%")
        ))
    if status:
        query = query.filter(models.Booking.booking_status == status)
    if venue_id:
        query = query.filter(models.Booking.venue_id == venue_id)

    bookings = query.order_by(models.Booking.created_at.desc()).all()
    venues = db.query(models.Venue).all()

    return render_template(
        request,
        "admin/bookings.html",
        {
            "current_user": admin,
            "active_page": "bookings",
            "bookings": bookings,
            "venues": venues,
            "query_q": q,
            "query_status": status,
            "query_venue_id": venue_id
        }
    )

@router.get("/bookings/{booking_id}", response_class=HTMLResponse)
def admin_booking_detail(
    request: Request,
    booking_id: int,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    booking = db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found.")

    return render_template(
        request,
        "admin/booking_detail.html",
        {"current_user": admin, "active_page": "bookings", "booking": booking}
    )

@router.post("/bookings/{booking_id}/status")
def update_booking_status(
    booking_id: int,
    status: str = Form(...),
    reason: Optional[str] = Form(None),
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    booking = db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found.")

    booking.booking_status = status
    if reason:
        booking.rejection_reason = reason.strip()

    # Create notification for customer
    create_notification(
        db,
        user_id=booking.customer_id,
        title=f"Booking {status}!",
        message=f"Your wedding booking request {booking.booking_reference} is now marked as {status}. {reason or ''}",
        notification_type="booking",
        link_url=f"/customer/bookings/{booking.booking_id}"
    )

    # Log audit event
    db.add(models.AuditLog(
        user_id=admin.user_id,
        action="BOOKING_STATUS_CHANGED",
        entity_type="Booking",
        entity_id=booking.booking_id,
        details=f"Admin {admin.full_name} updated booking {booking.booking_reference} status to {status}."
    ))
    db.commit()

    return RedirectResponse(url=f"/admin/bookings/{booking_id}", status_code=status.HTTP_303_SEE_OTHER)

# ================= Payment Verification =================
@router.get("/payments", response_class=HTMLResponse)
def admin_payments(
    request: Request,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    payments = db.query(models.Payment).order_by(models.Payment.payment_date.desc()).all()
    return render_template(
        request,
        "admin/payments.html",
        {"current_user": admin, "active_page": "payments", "payments": payments}
    )

@router.post("/payments/{payment_id}/verify")
def admin_verify_payment(
    payment_id: int,
    action: str = Form(...),
    admin_notes: Optional[str] = Form(None),
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    try:
        verify_payment(
            db=db,
            payment_id=payment_id,
            admin_id=admin.user_id,
            action=action,
            admin_notes=admin_notes
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return RedirectResponse(url="/admin/payments?verified=1", status_code=status.HTTP_303_SEE_OTHER)

# ================= Venue Management =================
@router.get("/venues", response_class=HTMLResponse)
def admin_venues(
    request: Request,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    venues = db.query(models.Venue).all()
    return render_template(
        request,
        "admin/venues.html",
        {"current_user": admin, "active_page": "venues", "venues": venues}
    )

@router.post("/venues/add")
def admin_add_venue(
    venue_name: str = Form(...),
    city: str = Form(...),
    address: str = Form(...),
    capacity: int = Form(...),
    base_price: Decimal = Form(...),
    facilities: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    v = models.Venue(
        venue_name=venue_name.strip(),
        city=city.strip(),
        address=address.strip(),
        capacity=capacity,
        base_price=base_price,
        facilities=facilities.strip() if facilities else None,
        description=description.strip() if description else None,
        status="active",
        is_active=True
    )
    db.add(v)
    db.commit()
    db.refresh(v)

    # Attach default image
    db.add(models.VenueImage(
        venue_id=v.venue_id,
        image_url="/static/images/luxury_ballroom.jpg",
        is_primary=True,
        caption="Ballroom View"
    ))
    db.commit()

    return RedirectResponse(url="/admin/venues", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/venues/{venue_id}/toggle")
def admin_toggle_venue(
    venue_id: int,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    v = db.query(models.Venue).filter(models.Venue.venue_id == venue_id).first()
    if v:
        v.is_active = not v.is_active
        v.status = "active" if v.is_active else "inactive"
        db.commit()
    return RedirectResponse(url="/admin/venues", status_code=status.HTTP_303_SEE_OTHER)

# ================= Venue Availability & Date Locks =================
@router.get("/availability", response_class=HTMLResponse)
def admin_availability(
    request: Request,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    availabilities = db.query(models.VenueAvailability).all()
    venues = db.query(models.Venue).filter(models.Venue.is_active == True).all()
    confirmed = db.query(models.Booking).filter(models.Booking.booking_status == "Confirmed").all()

    return render_template(
        request,
        "admin/availability.html",
        {
            "current_user": admin,
            "active_page": "availability",
            "availabilities": availabilities,
            "venues": venues,
            "confirmed_bookings": confirmed
        }
    )

@router.post("/availability/block")
def admin_block_availability(
    venue_id: int = Form(...),
    date: str = Form(...),
    reason: str = Form(...),
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    d_obj = datetime.strptime(date, "%Y-%m-%d").date()
    av = models.VenueAvailability(
        venue_id=venue_id,
        date=d_obj,
        is_available=False,
        reason=reason.strip()
    )
    db.add(av)
    db.commit()
    return RedirectResponse(url="/admin/availability", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/availability/{availability_id}/delete")
def admin_delete_availability(
    availability_id: int,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    av = db.query(models.VenueAvailability).filter(models.VenueAvailability.availability_id == availability_id).first()
    if av:
        db.delete(av)
        db.commit()
    return RedirectResponse(url="/admin/availability", status_code=status.HTTP_303_SEE_OTHER)

# ================= User Management =================
@router.get("/users", response_class=HTMLResponse)
def admin_users(
    request: Request,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return render_template(
        request,
        "admin/users.html",
        {"current_user": admin, "active_page": "users", "users": users}
    )

@router.post("/users/{user_id}/toggle")
def admin_toggle_user(
    user_id: int,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    u = db.query(models.User).filter(models.User.user_id == user_id).first()
    if u and u.role != "admin":
        u.is_active = not u.is_active
        db.commit()
    return RedirectResponse(url="/admin/users", status_code=status.HTTP_303_SEE_OTHER)

# ================= Package Management =================
@router.get("/packages", response_class=HTMLResponse)
def admin_packages(
    request: Request,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    packages = db.query(models.Package).all()
    return render_template(
        request,
        "admin/packages.html",
        {"current_user": admin, "active_page": "packages", "packages": packages}
    )

@router.post("/packages/add")
def admin_add_package(
    package_name: str = Form(...),
    price: Decimal = Form(...),
    services: str = Form(...),
    description: Optional[str] = Form(None),
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    pkg = models.Package(
        package_name=package_name.strip(),
        price=price,
        description=description.strip() if description else None,
        image_url="/static/images/banquet_feast.jpg",
        is_active=True
    )
    db.add(pkg)
    db.flush()

    for s_name in services.split(","):
        clean_s = s_name.strip()
        if clean_s:
            db.add(models.PackageService(package_id=pkg.package_id, service_name=clean_s, is_included=True))

    db.commit()
    return RedirectResponse(url="/admin/packages", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/packages/{package_id}/toggle")
def admin_toggle_package(
    package_id: int,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    pkg = db.query(models.Package).filter(models.Package.package_id == package_id).first()
    if pkg:
        pkg.is_active = not pkg.is_active
        db.commit()
    return RedirectResponse(url="/admin/packages", status_code=status.HTTP_303_SEE_OTHER)

# ================= Vendor Management =================
@router.get("/vendors", response_class=HTMLResponse)
def admin_vendors(
    request: Request,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    vendors = db.query(models.Vendor).all()
    return render_template(
        request,
        "admin/vendors.html",
        {"current_user": admin, "active_page": "vendors", "vendors": vendors}
    )

@router.post("/vendors/add")
def admin_add_vendor(
    vendor_name: str = Form(...),
    category: str = Form(...),
    price: Decimal = Form(...),
    phone: str = Form(...),
    contact_name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    v = models.Vendor(
        vendor_name=vendor_name.strip(),
        category=category,
        price=price,
        phone=phone.strip(),
        contact_name=contact_name.strip() if contact_name else None,
        description=description.strip() if description else None,
        image_url="/static/images/hero_wedding_couple.jpg",
        is_active=True
    )
    db.add(v)
    db.commit()
    return RedirectResponse(url="/admin/vendors", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/vendors/{vendor_id}/toggle")
def admin_toggle_vendor(
    vendor_id: int,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    v = db.query(models.Vendor).filter(models.Vendor.vendor_id == vendor_id).first()
    if v:
        v.is_active = not v.is_active
        db.commit()
    return RedirectResponse(url="/admin/vendors", status_code=status.HTTP_303_SEE_OTHER)

# ================= Catering Management =================
@router.get("/catering", response_class=HTMLResponse)
def admin_catering(
    request: Request,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    menus = db.query(models.Menu).all()
    return render_template(
        request,
        "admin/catering.html",
        {"current_user": admin, "active_page": "catering", "menus": menus}
    )

@router.post("/catering/add")
def admin_add_menu(
    name: str = Form(...),
    category: str = Form(...),
    price_per_person: Decimal = Form(...),
    description: Optional[str] = Form(None),
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    m = models.Menu(
        name=name.strip(),
        category=category,
        price_per_person=price_per_person,
        description=description.strip() if description else None,
        image_url="/static/images/banquet_feast.jpg",
        is_active=True
    )
    db.add(m)
    db.commit()
    return RedirectResponse(url="/admin/catering", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/catering/{menu_id}/toggle")
def admin_toggle_menu(
    menu_id: int,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    m = db.query(models.Menu).filter(models.Menu.menu_id == menu_id).first()
    if m:
        m.is_active = not m.is_active
        db.commit()
    return RedirectResponse(url="/admin/catering", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/catering/{menu_id}/edit")
def admin_edit_menu(
    menu_id: int,
    name: str = Form(...),
    category: str = Form(...),
    price_per_person: Decimal = Form(...),
    description: Optional[str] = Form(None),
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    m = db.query(models.Menu).filter(models.Menu.menu_id == menu_id).first()
    if m:
        m.name = name.strip()
        m.category = category
        m.price_per_person = price_per_person
        if description:
            m.description = description.strip()
        db.commit()
    return RedirectResponse(url="/admin/catering", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/catering/{menu_id}/delete")
def admin_delete_menu(
    menu_id: int,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    m = db.query(models.Menu).filter(models.Menu.menu_id == menu_id).first()
    if m:
        # Check if attached to bookings
        has_bookings = db.query(models.BookingMenu).filter(models.BookingMenu.menu_id == menu_id).first()
        if has_bookings:
            m.is_active = False
        else:
            db.delete(m)
        db.commit()
    return RedirectResponse(url="/admin/catering", status_code=status.HTTP_303_SEE_OTHER)

# ================= Guest Overview =================
@router.get("/guests", response_class=HTMLResponse)
def admin_guests(
    request: Request,
    booking_id: Optional[int] = None,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    query = db.query(models.Guest)
    if booking_id:
        query = query.filter(models.Guest.booking_id == booking_id)
    guests = query.order_by(models.Guest.created_at.desc()).all()
    bookings = db.query(models.Booking).all()

    return render_template(
        request,
        "admin/guests.html",
        {
            "current_user": admin,
            "active_page": "guests",
            "guests": guests,
            "bookings": bookings,
            "selected_booking_id": booking_id
        }
    )

# ================= Feedback Management =================
@router.get("/feedback", response_class=HTMLResponse)
def admin_feedback(
    request: Request,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    feedbacks = db.query(models.Feedback).order_by(models.Feedback.created_at.desc()).all()
    return render_template(
        request,
        "admin/feedback.html",
        {"current_user": admin, "active_page": "feedback", "feedbacks": feedbacks}
    )

@router.post("/feedback/{feedback_id}/respond")
def admin_respond_feedback(
    feedback_id: int,
    response: str = Form(...),
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    fb = db.query(models.Feedback).filter(models.Feedback.feedback_id == feedback_id).first()
    if fb:
        fb.admin_response = response.strip()
        fb.response_at = datetime.utcnow()
        db.commit()
    return RedirectResponse(url="/admin/feedback", status_code=status.HTTP_303_SEE_OTHER)

# ================= Notification Broadcasts =================
@router.get("/notifications", response_class=HTMLResponse)
def admin_notifications(
    request: Request,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return render_template(
        request,
        "admin/notifications.html",
        {"current_user": admin, "active_page": "notifications"}
    )

@router.post("/notifications/broadcast")
def admin_broadcast_notification(
    title: str = Form(...),
    message: str = Form(...),
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    customers = db.query(models.User).filter(models.User.role == "customer", models.User.is_active == True).all()
    for c in customers:
        db.add(models.Notification(
            user_id=c.user_id,
            title=title.strip(),
            message=message.strip(),
            notification_type="system"
        ))
    db.commit()
    return RedirectResponse(url="/admin/notifications?sent=1", status_code=status.HTTP_303_SEE_OTHER)

# ================= Reports & Analytics =================
@router.get("/reports", response_class=HTMLResponse)
def admin_reports(
    request: Request,
    type: str = "bookings",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    records = []
    total_sum = Decimal("0.00")

    if type == "bookings":
        q = db.query(models.Booking)
        if start_date:
            q = q.filter(models.Booking.event_date >= datetime.strptime(start_date, "%Y-%m-%d").date())
        if end_date:
            q = q.filter(models.Booking.event_date <= datetime.strptime(end_date, "%Y-%m-%d").date())
        records = q.order_by(models.Booking.event_date.desc()).all()
        total_sum = sum(b.total_cost for b in records)
    else:
        q = db.query(models.Payment)
        if start_date:
            q = q.filter(models.Payment.payment_date >= datetime.strptime(start_date, "%Y-%m-%d"))
        if end_date:
            q = q.filter(models.Payment.payment_date <= datetime.strptime(end_date, "%Y-%m-%d"))
        records = q.order_by(models.Payment.payment_date.desc()).all()
        total_sum = sum(p.amount for p in records if p.payment_status == "Verified")

    records_count = len(records)
    avg_sum = (total_sum / records_count) if records_count > 0 else Decimal("0.00")

    return render_template(
        request,
        "admin/reports.html",
        {
            "current_user": admin,
            "active_page": "reports",
            "report_type": type,
            "start_date": start_date,
            "end_date": end_date,
            "records": records,
            "records_count": records_count,
            "total_sum": total_sum,
            "avg_sum": avg_sum
        }
    )

@router.get("/reports/export/csv")
def export_csv(
    type: str = "bookings",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    if type == "bookings":
        q = db.query(models.Booking)
        if start_date:
            q = q.filter(models.Booking.event_date >= datetime.strptime(start_date, "%Y-%m-%d").date())
        if end_date:
            q = q.filter(models.Booking.event_date <= datetime.strptime(end_date, "%Y-%m-%d").date())
        data = generate_bookings_csv(q.all())
        filename = f"peacock_bookings_{date.today()}.csv"
    else:
        q = db.query(models.Payment)
        if start_date:
            q = q.filter(models.Payment.payment_date >= datetime.strptime(start_date, "%Y-%m-%d"))
        if end_date:
            q = q.filter(models.Payment.payment_date <= datetime.strptime(end_date, "%Y-%m-%d"))
        data = generate_payments_csv(q.all())
        filename = f"peacock_payments_{date.today()}.csv"

    return Response(
        content=data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/reports/export/pdf")
def export_pdf(
    type: str = "bookings",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    if type == "bookings":
        q = db.query(models.Booking)
        if start_date:
            q = q.filter(models.Booking.event_date >= datetime.strptime(start_date, "%Y-%m-%d").date())
        if end_date:
            q = q.filter(models.Booking.event_date <= datetime.strptime(end_date, "%Y-%m-%d").date())
        bookings = q.all()
        headers = ["Ref", "Customer", "Venue", "Event Date", "Total (MMK)", "Status"]
        table_rows = [
            [b.booking_reference, b.customer.full_name[:15], b.venue.venue_name[:18], str(b.event_date), f"{b.total_cost:,.0f} Ks", b.booking_status]
            for b in bookings
        ]
        pdf_bytes = generate_pdf_report(
            title="Bookings & Revenue Summary",
            headers=headers,
            data=table_rows,
            summary={"Total Bookings": str(len(bookings)), "Total Value": f"{sum(b.total_cost for b in bookings):,.0f} MMK"}
        )
        filename = f"peacock_bookings_report_{date.today()}.pdf"
    else:
        q = db.query(models.Payment)
        if start_date:
            q = q.filter(models.Payment.payment_date >= datetime.strptime(start_date, "%Y-%m-%d"))
        if end_date:
            q = q.filter(models.Payment.payment_date <= datetime.strptime(end_date, "%Y-%m-%d"))
        payments = q.all()
        headers = ["Payment Ref", "Booking", "Amount (MMK)", "Method", "Txn ID", "Status"]
        table_rows = [
            [p.payment_reference, p.booking.booking_reference, f"{p.amount:,.0f} Ks", p.payment_method, p.transaction_reference[:16], p.payment_status]
            for p in payments
        ]
        pdf_bytes = generate_pdf_report(
            title="Payments & Deposit Audit Report",
            headers=headers,
            data=table_rows,
            summary={"Total Transactions": str(len(payments)), "Total Verified": f"{sum(p.amount for p in payments if p.payment_status == 'Verified'):,.0f} MMK"}
        )
        filename = f"peacock_payments_report_{date.today()}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# ================= Audit Logs & Settings =================
@router.get("/audit-logs", response_class=HTMLResponse)
def admin_audit_logs(
    request: Request,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    logs = db.query(models.AuditLog).order_by(models.AuditLog.created_at.desc()).limit(100).all()
    return render_template(
        request,
        "admin/audit_logs.html",
        {"current_user": admin, "active_page": "audit", "audit_logs": logs}
    )

@router.get("/settings", response_class=HTMLResponse)
def admin_settings(
    request: Request,
    admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return render_template(
        request,
        "admin/settings.html",
        {"current_user": admin, "active_page": "settings"}
    )
