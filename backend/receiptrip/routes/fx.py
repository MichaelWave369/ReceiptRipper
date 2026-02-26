from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from receiptrip.auth import get_current_user
from receiptrip.db import get_db
from receiptrip.models import ExchangeRate, User
from receiptrip.schemas import FXRateIn

router = APIRouter(prefix="/api/fx", tags=["fx"])


@router.get("/rates")
def list_rates(base: str | None = None, quote: str | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    query = db.query(ExchangeRate)
    if base:
        query = query.filter(ExchangeRate.base_currency == base.upper())
    if quote:
        query = query.filter(ExchangeRate.quote_currency == quote.upper())
    return query.order_by(ExchangeRate.as_of_date.desc()).all()


@router.post("/rates")
def create_rate(payload: FXRateIn, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    item = ExchangeRate(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
