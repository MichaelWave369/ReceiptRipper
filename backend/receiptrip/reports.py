from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from .fx import convert_cents
from .models import Category, Envelope, Transaction


def monthly_summary(db: Session, user_id: int, month: str, reporting_currency: str):
    year, mon = map(int, month.split("-"))
    txs = db.query(Transaction).filter(Transaction.user_id == user_id, func.strftime("%Y", Transaction.spent_at) == f"{year:04d}", func.strftime("%m", Transaction.spent_at) == f"{mon:02d}").all()

    total = 0
    by_category, by_envelope = {}, {}
    categories = {c.id: c.name for c in db.query(Category).filter(Category.user_id == user_id).all()}
    envelopes = {e.id: e.name for e in db.query(Envelope).filter(Envelope.user_id == user_id).all()}

    for t in txs:
        converted = convert_cents(db, t.amount_cents, t.currency, reporting_currency, t.spent_at)
        total += converted
        cname = categories.get(t.category_id, "Uncategorized")
        by_category[cname] = by_category.get(cname, 0) + converted
        ename = envelopes.get(t.envelope_id, "Unassigned")
        by_envelope[ename] = by_envelope.get(ename, 0) + converted
    return {"month": month, "currency": reporting_currency, "total_spent_cents": total, "by_category": by_category, "by_envelope": by_envelope}


def monthly_trend(db: Session, user_id: int, months: int, reporting_currency: str):
    now = datetime.utcnow()
    out = []
    for i in range(months - 1, -1, -1):
        total_month = (now.year * 12 + now.month - 1) - i
        y = total_month // 12
        m = total_month % 12 + 1
        key = f"{y:04d}-{m:02d}"
        out.append(monthly_summary(db, user_id, key, reporting_currency))
    return [{"month": x["month"], "total_spent_cents": x["total_spent_cents"]} for x in out]
