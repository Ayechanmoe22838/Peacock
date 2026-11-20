from decimal import Decimal
import pytest
from app.services.payment_service import submit_payment, verify_payment
import app.models as models

def test_kpay_payment_submission_and_verification_workflow(db):
    admin = db.query(models.User).filter_by(email="admin@peacock.com").first()
    cust = db.query(models.User).filter_by(email="customer@peacock.com").first()
    booking = db.query(models.Booking).filter_by(booking_reference="BK-202611-001").first()

    initial_paid = booking.paid_amount
    initial_balance = booking.balance_amount
    test_amount = Decimal("500000.00")

    # 1. Customer submits payment
    payment = submit_payment(
        db=db,
        booking_id=booking.booking_id,
        amount=test_amount,
        payment_method="KBZPay",
        transaction_reference="KPay-TEST-9988776655",
        notes="Automated test deposit"
    )
    assert payment.payment_status == "Pending Verification"

    # 2. Admin verifies payment
    verified = verify_payment(
        db=db,
        payment_id=payment.payment_id,
        admin_id=admin.user_id,
        action="approve",
        admin_notes="Verified via test suite"
    )
    assert verified.payment_status == "Verified"
    assert verified.verified_by == admin.user_id

    # Verify booking balance updated
    db.refresh(booking)
    assert booking.paid_amount == initial_paid + test_amount
    assert booking.balance_amount == initial_balance - test_amount

    # Clean up test payment
    db.delete(payment)
    # Restore booking paid and balance
    booking.paid_amount = initial_paid
    booking.balance_amount = initial_balance
    db.commit()
