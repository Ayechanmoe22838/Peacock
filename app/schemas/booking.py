from typing import Optional, List
from datetime import date, time
from decimal import Decimal
from pydantic import BaseModel, Field

class BookingCreate(BaseModel):
    venue_id: int
    package_id: Optional[int] = None
    event_date: date
    start_time: time
    end_time: time
    guest_count: int = Field(..., gt=0)
    special_requirements: Optional[str] = None
    vendor_ids: Optional[List[int]] = []
    catering_items: Optional[List[dict]] = []  # [{"menu_id": int, "quantity": int}]

class BookingStatusUpdate(BaseModel):
    status: str
    reason: Optional[str] = None

class BookingCancelRequest(BaseModel):
    reason: str = Field(..., min_length=5)
