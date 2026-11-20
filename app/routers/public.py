from datetime import datetime, date, time
from typing import Optional
from fastapi import APIRouter, Request, Depends, HTTPException, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import BaseModel
from app.core.config import settings
from app.core.database import get_db
from app.core.permissions import get_current_user_optional
from app.core.templates import render_template
from app.core.encryption import encrypt_data
from app.core.invitation_templates import get_template_image
from app.services.booking_service import check_venue_availability
import app.models as models

router = APIRouter(tags=["Public Pages"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    
    venues = db.query(models.Venue).filter(models.Venue.is_active == True).limit(3).all()
    packages = db.query(models.Package).filter(models.Package.is_active == True).limit(3).all()
    testimonials = db.query(models.Feedback).filter(models.Feedback.is_approved == True).limit(2).all()
    
    total_venues = db.query(models.Venue).filter(models.Venue.is_active == True).count()
    total_packages = db.query(models.Package).filter(models.Package.is_active == True).count()
    total_vendors = db.query(models.Vendor).filter(models.Vendor.is_active == True).count()

    return render_template(
        request=request,
        name="public/index.html",
        context={
            "current_user": current_user,
            "featured_venues": venues,
            "popular_packages": packages,
            "testimonials": testimonials,
            "total_venues": total_venues,
            "total_packages": total_packages,
            "total_vendors": total_vendors
        }
    )

@router.get("/venues", response_class=HTMLResponse)
def venues_list(
    request: Request,
    q: Optional[str] = None,
    city: Optional[str] = None,
    capacity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    current_user = get_current_user_optional(request, db)
    query = db.query(models.Venue).filter(models.Venue.is_active == True)

    if q:
        query = query.filter(or_(
            models.Venue.venue_name.ilike(f"%{q}%"),
            models.Venue.description.ilike(f"%{q}%"),
            models.Venue.facilities.ilike(f"%{q}%")
        ))
    if city:
        query = query.filter(models.Venue.city == city)
    if capacity:
        try:
            cap_int = int(capacity)
            query = query.filter(models.Venue.capacity >= cap_int)
        except ValueError:
            pass

    venues = query.all()
    all_cities = [c[0] for c in db.query(models.Venue.city).distinct().all()]

    return render_template(
        request=request,
        name="public/venues.html",
        context={
            "current_user": current_user,
            "venues": venues,
            "cities": all_cities,
            "query_q": q,
            "query_city": city,
            "query_capacity": capacity
        }
    )

@router.get("/venues/{venue_id}", response_class=HTMLResponse)
def venue_detail(request: Request, venue_id: int, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    venue = db.query(models.Venue).filter(models.Venue.venue_id == venue_id, models.Venue.is_active == True).first()
    if not venue:
        raise HTTPException(status_code=404, detail="Wedding venue not found.")

    return render_template(
        request=request,
        name="public/venue_detail.html",
        context={"current_user": current_user, "venue": venue}
    )

@router.get("/packages", response_class=HTMLResponse)
def packages_list(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    packages = db.query(models.Package).filter(models.Package.is_active == True).all()
    return render_template(
        request=request,
        name="public/packages.html",
        context={"current_user": current_user, "packages": packages}
    )

@router.get("/packages/{package_id}", response_class=HTMLResponse)
def package_detail(request: Request, package_id: int, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    pkg = db.query(models.Package).filter(models.Package.package_id == package_id, models.Package.is_active == True).first()
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found.")

    return render_template(
        request=request,
        name="public/package_detail.html",
        context={"current_user": current_user, "package": pkg}
    )

@router.get("/services", response_class=HTMLResponse)
def services_list(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    vendors = db.query(models.Vendor).filter(models.Vendor.is_active == True).all()
    menus = db.query(models.Menu).filter(models.Menu.is_active == True).all()

    return render_template(
        request=request,
        name="public/services.html",
        context={"current_user": current_user, "vendors": vendors, "menus": menus}
    )

@router.get("/about", response_class=HTMLResponse)
def about_page(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    return render_template(
        request=request,
        name="public/about.html",
        context={"current_user": current_user}
    )

@router.get("/contact", response_class=HTMLResponse)
def contact_page(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    return render_template(
        request=request,
        name="public/contact.html",
        context={"current_user": current_user}
    )

@router.get("/privacy", response_class=HTMLResponse)
def privacy_page(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    return render_template(
        request=request,
        name="public/privacy.html",
        context={"current_user": current_user}
    )

@router.get("/terms", response_class=HTMLResponse)
def terms_page(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    return render_template(
        request=request,
        name="public/terms.html",
        context={"current_user": current_user}
    )

# ================= Public Digital Invitation & RSVP =================
@router.get("/invitation/{token}", response_class=HTMLResponse)
def view_digital_invitation(request: Request, token: str, db: Session = Depends(get_db)):
    invitation = db.query(models.Invitation).filter(models.Invitation.shareable_token == token).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found.")

    invitation.views_count += 1
    db.commit()

    template_image = get_template_image(invitation.template_name)

    return render_template(
        request=request,
        name="public/invitation_view.html",
        context={"current_user": None, "invitation": invitation, "template_image": template_image}
    )

class PublicRSVPPayload(BaseModel):
    guest_name: str
    phone: Optional[str] = None
    rsvp_status: str
    plus_ones: int = 0
    dietary_requirements: Optional[str] = None
    notes: Optional[str] = None

@router.post("/api/invitations/{token}/rsvp")
def submit_public_rsvp(token: str, payload: PublicRSVPPayload, db: Session = Depends(get_db)):
    invitation = db.query(models.Invitation).filter(models.Invitation.shareable_token == token).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found.")

    guest = None
    if payload.phone:
        guest = db.query(models.Guest).filter(
            models.Guest.booking_id == invitation.booking_id,
            models.Guest.phone == payload.phone
        ).first()

    if not guest:
        guest = db.query(models.Guest).filter(
            models.Guest.booking_id == invitation.booking_id,
            models.Guest.guest_name.ilike(payload.guest_name.strip())
        ).first()

    if guest:
        guest.rsvp_status = payload.rsvp_status
        guest.plus_ones = payload.plus_ones
        if payload.dietary_requirements:
            guest.dietary_requirements = payload.dietary_requirements
        if payload.notes:
            guest.notes = payload.notes
    else:
        guest = models.Guest(
            booking_id=invitation.booking_id,
            guest_name=payload.guest_name.strip(),
            phone=encrypt_data(payload.phone.strip()) if payload.phone else None,
            category="Friends",
            rsvp_status=payload.rsvp_status,
            plus_ones=payload.plus_ones,
            dietary_requirements=payload.dietary_requirements,
            notes=payload.notes
        )
        db.add(guest)

    db.commit()
    return {"success": True, "message": "RSVP recorded successfully."}

# ================= AJAX Live Availability Checker =================
@router.get("/api/venues/{venue_id}/check-availability")
def check_availability_api(
    venue_id: int,
    date_str: str = Query(..., alias="date"),
    start_time_str: str = Query(..., alias="start_time"),
    end_time_str: str = Query(..., alias="end_time"),
    db: Session = Depends(get_db)
):
    try:
        ev_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        st_parts = [int(p) for p in start_time_str.split(":")]
        et_parts = [int(p) for p in end_time_str.split(":")]
        st_time = time(st_parts[0], st_parts[1])
        et_time = time(et_parts[0], et_parts[1])
    except Exception:
        return JSONResponse(status_code=400, content={"available": False, "reason": "Invalid date or time format."})

    is_avail, reason = check_venue_availability(db, venue_id, ev_date, st_time, et_time)
    return {"available": is_avail, "reason": reason}
