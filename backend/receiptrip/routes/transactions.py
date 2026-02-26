from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from receiptrip.auth import get_current_user
from receiptrip.db import get_db
from receiptrip.models import Transaction, User, Merchant
from receiptrip.schemas import TransactionIn

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get("")
def list_transactions(month: str | None = None, q: str | None = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Transaction).filter(Transaction.user_id == user.id)
    if month:
        year, mon = month.split("-")
        query = query.filter(func.strftime("%Y", Transaction.spent_at) == year, func.strftime("%m", Transaction.spent_at) == mon)
    if q:
        query = query.filter(or_(Transaction.merchant.ilike(f"%{q}%"), Transaction.note.ilike(f"%{q}%")))
    return query.order_by(Transaction.spent_at.desc()).all()


@router.post("")
def create_transaction(payload: TransactionIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    data = payload.model_dump()
    if not data.get("spent_at"):
        data["spent_at"] = datetime.utcnow()
    item = Transaction(user_id=user.id, **data)
    db.add(item)
    if payload.merchant and payload.category_id:
        existing = db.query(Merchant).filter(Merchant.user_id == user.id, Merchant.name.ilike(payload.merchant)).first()
        if not existing:
            db.add(Merchant(user_id=user.id, name=payload.merchant, category_id=payload.category_id, rules_json="{}"))
    db.commit()
    db.refresh(item)
    return item


@router.put("/{tx_id}")
def update_transaction(tx_id: int, payload: TransactionIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(Transaction).filter(Transaction.id == tx_id, Transaction.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit()
    return item


@router.delete("/{tx_id}")
def delete_transaction(tx_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(Transaction).filter(Transaction.id == tx_id, Transaction.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
