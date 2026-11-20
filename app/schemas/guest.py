from typing import Optional
from pydantic import BaseModel, Field

class GuestCreate(BaseModel):
    guest_name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = None
    email: Optional[str] = None
    category: str = "Friends"
    rsvp_status: str = "Pending"
    dietary_requirements: Optional[str] = None
    plus_ones: int = 0
    notes: Optional[str] = None

class GuestUpdate(BaseModel):
    guest_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    category: str
    rsvp_status: str
    dietary_requirements: Optional[str] = None
    plus_ones: int = 0
    notes: Optional[str] = None

class PublicRSVP(BaseModel):
    rsvp_status: str  # Accepted, Declined
    dietary_requirements: Optional[str] = None
    plus_ones: int = 0
    notes: Optional[str] = None
