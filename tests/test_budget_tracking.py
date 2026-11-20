from decimal import Decimal
from datetime import date, time
from sqlalchemy.orm import Session
from app.services.budget_service import add_expense, recalculate_budget
import app.models as models

def test_budget_calculations_and_recalculation(db: Session):
    customer = db.query(models.User).filter_by(role="customer").first()
    venue = db.query(models.Venue).filter_by(is_active=True).first()
    pkg = db.query(models.Package).filter_by(is_active=True).first()

    booking = models.Booking(
        booking_reference="BK-BUDGET-TEST",
        customer_id=customer.user_id,
        venue_id=venue.venue_id,
        package_id=pkg.package_id,
        event_date=date(2027, 8, 15),
        start_time=time(17, 0),
        end_time=time(22, 0),
        guest_count=200,
        venue_cost=Decimal("3000000.00"),
        package_cost=Decimal("2000000.00"),
        vendors_cost=Decimal("0.00"),
        catering_cost=Decimal("0.00"),
        total_cost=Decimal("5000000.00"),
        paid_amount=Decimal("0.00"),
        balance_amount=Decimal("5000000.00"),
        booking_status="Confirmed"
    )
    db.add(booking)
    db.flush()

    budget = models.Budget(
        booking_id=booking.booking_id,
        total_budget=Decimal("10000000.00"),
        estimated_cost=Decimal("5000000.00"),
        actual_spent=Decimal("0.00"),
        remaining_budget=Decimal("10000000.00")
    )
    db.add(budget)
    db.flush()

    # Add expense
    expense = add_expense(
        db=db,
        budget_id=budget.budget_id,
        category="Flowers",
        item_name="Bridal Roses Centerpiece",
        estimated_cost=Decimal("400000.00"),
        actual_cost=Decimal("450000.00"),
        is_paid=True
    )
    assert expense.expense_id is not None

    recalculate_budget(db, budget.budget_id)
    db.refresh(budget)

    assert budget.actual_spent == Decimal("450000.00")
    assert budget.remaining_budget == Decimal("9550000.00")

    # Cleanup test records
    db.delete(expense)
    db.delete(budget)
    db.delete(booking)
    db.commit()
