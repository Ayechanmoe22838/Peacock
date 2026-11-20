import random
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
import app.models as models
from app.services.notification_service import create_notification, notify_admins

def generate_payment_reference() -> str:
    now_str = datetime.utcnow().strftime("%Y%m")
    rnd = random.randint(1000, 9999)
    return f"PAY-{now_str}-{rnd}"

def submit_payment(
    db: Session,
    booking_id: int,
    amount: Decimal,
    payment_method: str,
    transaction_reference: str,
    receipt_image: Optional[str] = None,
    notes: Optional[str] = None
) -> models.Payment:
    """
    Submits a payment record with 'Pending Verification' status.
    """
    booking = db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    if not booking:
        raise ValueError("Booking not found.")

    if amount <= 0:
        raise ValueError("Payment amount must be greater than zero.")

    ref = generate_payment_reference()
    while db.query(models.Payment).filter_by(payment_reference=ref).first():
        ref = generate_payment_reference()

    payment = models.Payment(
        payment_reference=ref,
        booking_id=booking_id,
        amount=amount,
        payment_method=payment_method,
        transaction_reference=transaction_reference,
        receipt_image=receipt_image,
        payment_status="Pending Verification",
        notes=notes,
        payment_date=datetime.utcnow()
    )
    db.add(payment)
    db.flush()

    # Notify customer and admins
    create_notification(
        db, booking.customer_id,
        "Payment Submitted for Verification",
        f"Your payment of {amount:,.2f} MMK ({ref}) has been submitted. Our administrators will verify the transaction.",
        "payment",
        f"/customer/payments"
    )
    notify_admins(
        db,
        "Payment Verification Required",
        f"New payment of {amount:,.2f} MMK submitted for booking {booking.booking_reference}. Please verify receipt.",
        "payment",
        f"/admin/payments"
    )

    db.add(models.AuditLog(
        user_id=booking.customer_id,
        action="PAYMENT_SUBMITTED",
        entity_type="Payment",
        entity_id=payment.payment_id,
        details=f"Submitted payment {ref} for {amount:,.2f} MMK via {payment_method}. Txn: {transaction_reference}."
    ))

    db.commit()
    db.refresh(payment)
    return payment

def verify_payment(
    db: Session,
    payment_id: int,
    admin_id: int,
    action: str,  # 'approve' or 'reject'
    admin_notes: Optional[str] = None
) -> models.Payment:
    """
    Admin approves or rejects a submitted payment.
    Updates booking paid_amount, balance_amount, and automatically updates booking status.
    """
    payment = db.query(models.Payment).filter(models.Payment.payment_id == payment_id).first()
    if not payment:
        raise ValueError("Payment record not found.")

    booking = payment.booking

    if action == "approve":
        payment.payment_status = "Verified"
        payment.verified_by = admin_id
        payment.verified_at = datetime.utcnow()
        payment.admin_notes = admin_notes or "Payment verified against official merchant account."

        # Re-sum all verified payments for this booking
        verified_payments = db.query(models.Payment).filter(
            models.Payment.booking_id == booking.booking_id,
            models.Payment.payment_status == "Verified"
        ).all()

        total_paid = sum(p.amount for p in verified_payments)
        booking.paid_amount = total_paid
        booking.balance_amount = max(Decimal("0.00"), booking.total_cost - total_paid)

        # If booking is Approved or Pending and now has a verified deposit, transition to Confirmed
        if booking.booking_status in ["Pending", "Approved"]:
            booking.booking_status = "Confirmed"

        # Update budget actual spent
        if booking.budget:
            booking.budget.actual_spent = total_paid
            booking.budget.remaining_budget = max(Decimal("0.00"), booking.budget.total_budget - total_paid)

        create_notification(
            db, booking.customer_id,
            "Payment Verified & Approved!",
            f"Your payment {payment.payment_reference} ({payment.amount:,.2f} MMK) has been verified. Booking {booking.booking_reference} is Confirmed!",
            "payment",
            f"/customer/payments"
        )

        db.add(models.AuditLog(
            user_id=admin_id,
            action="PAYMENT_VERIFIED",
            entity_type="Payment",
            entity_id=payment.payment_id,
            details=f"Admin {admin_id} verified payment {payment.payment_reference} of {payment.amount:,.2f} MMK. Booking status now: {booking.booking_status}."
        ))

    elif action == "reject":
        payment.payment_status = "Rejected"
        payment.verified_by = admin_id
        payment.verified_at = datetime.utcnow()
        payment.admin_notes = admin_notes or "Payment could not be verified."

        create_notification(
            db, booking.customer_id,
            "Payment Verification Failed",
            f"Your payment {payment.payment_reference} was rejected. Reason: {payment.admin_notes}",
            "payment",
            f"/customer/payments"
        )

        db.add(models.AuditLog(
            user_id=admin_id,
            action="PAYMENT_REJECTED",
            entity_type="Payment",
            entity_id=payment.payment_id,
            details=f"Admin {admin_id} rejected payment {payment.payment_reference}. Reason: {payment.admin_notes}."
        ))
    else:
        raise ValueError(f"Invalid verification action: {action}")

    db.commit()
    db.refresh(payment)
    return payment
