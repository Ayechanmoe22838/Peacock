from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

class PaymentSubmit(BaseModel):
    booking_id: int
    amount: Decimal = Field(..., gt=0)
    payment_method: str = "KBZPay"
    transaction_reference: str = Field(..., min_length=4, max_length=100)
    notes: Optional[str] = None

class PaymentVerify(BaseModel):
    action: str  # "approve" or "reject"
    admin_notes: Optional[str] = None
