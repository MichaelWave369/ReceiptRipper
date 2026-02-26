from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from receiptrip.auth import get_current_user
from receiptrip.db import get_db
from receiptrip.models import Transaction, User
from receiptrip.reports import monthly_summary, monthly_trend

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/summary")
def summary(month: str | None = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    month = month or datetime.utcnow().strftime("%Y-%m")
    return monthly_summary(db, user.id, month, user.default_currency)


@router.get("/trend")
def trend(months: int = 12, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return monthly_trend(db, user.id, months, user.default_currency)


@router.get("/merchants")
def merchants(month: str | None = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Transaction.merchant, func.sum(Transaction.amount_cents).label("total")).filter(Transaction.user_id == user.id)
    if month:
        year, mon = month.split("-")
        query = query.filter(func.strftime("%Y", Transaction.spent_at) == year, func.strftime("%m", Transaction.spent_at) == mon)
    return [{"merchant": row[0], "total_cents": row[1]} for row in query.group_by(Transaction.merchant).order_by(func.sum(Transaction.amount_cents).desc()).limit(10).all()]
