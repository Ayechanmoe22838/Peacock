from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
import app.models as models

def recalculate_budget(db: Session, budget_id: int) -> models.Budget:
    budget = db.query(models.Budget).filter(models.Budget.budget_id == budget_id).first()
    if not budget:
        raise ValueError("Budget not found.")

    expenses = db.query(models.Expense).filter(models.Expense.budget_id == budget_id).all()
    est_total = sum(e.estimated_cost for e in expenses)
    actual_spent = sum(e.actual_cost for e in expenses if e.is_paid)

    budget.estimated_cost = est_total
    budget.actual_spent = actual_spent
    budget.remaining_budget = max(Decimal("0.00"), budget.total_budget - actual_spent)

    db.commit()
    db.refresh(budget)
    return budget

def add_expense(
    db: Session,
    budget_id: int,
    category: str,
    item_name: str,
    estimated_cost: Decimal,
    actual_cost: Decimal = Decimal("0.00"),
    is_paid: bool = False,
    payment_reference: Optional[str] = None
) -> models.Expense:
    exp = models.Expense(
        budget_id=budget_id,
        category=category,
        item_name=item_name,
        estimated_cost=estimated_cost,
        actual_cost=actual_cost,
        is_paid=is_paid,
        payment_reference=payment_reference
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    recalculate_budget(db, budget_id)
    return exp
