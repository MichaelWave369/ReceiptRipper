from datetime import datetime
from sqlalchemy.orm import Session

from .models import ExchangeRate


def convert_cents(db: Session, amount_cents: int, from_currency: str, to_currency: str, at: datetime) -> int:
    if from_currency == to_currency:
        return amount_cents
    rate = (
        db.query(ExchangeRate)
        .filter(
            ExchangeRate.base_currency == from_currency,
            ExchangeRate.quote_currency == to_currency,
            ExchangeRate.as_of_date <= at.date(),
        )
        .order_by(ExchangeRate.as_of_date.desc())
        .first()
    )
    if not rate:
        rate = (
            db.query(ExchangeRate)
            .filter(ExchangeRate.base_currency == from_currency, ExchangeRate.quote_currency == to_currency)
            .order_by(ExchangeRate.as_of_date.desc())
            .first()
        )
    if not rate:
        return amount_cents
    return int(amount_cents * rate.rate)
