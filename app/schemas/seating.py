from typing import Optional
from pydantic import BaseModel, Field

class TableCreate(BaseModel):
    table_number: int
    table_name: str = Field(..., min_length=2, max_length=100)
    capacity: int = Field(10, gt=0, le=50)
    notes: Optional[str] = None

class AssignSeat(BaseModel):
    table_id: int
    guest_id: int
    seat_number: Optional[int] = None
