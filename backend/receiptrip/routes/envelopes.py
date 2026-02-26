from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from receiptrip.auth import get_current_user
from receiptrip.db import get_db
from receiptrip.models import Envelope, User
from receiptrip.schemas import EnvelopeIn

router = APIRouter(prefix="/api/envelopes", tags=["envelopes"])


@router.get("")
def list_envelopes(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Envelope).filter(Envelope.user_id == user.id).all()


@router.post("")
def create_envelope(payload: EnvelopeIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = Envelope(user_id=user.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{envelope_id}")
def update_envelope(envelope_id: int, payload: EnvelopeIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(Envelope).filter(Envelope.id == envelope_id, Envelope.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit()
    return item


@router.delete("/{envelope_id}")
def delete_envelope(envelope_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(Envelope).filter(Envelope.id == envelope_id, Envelope.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
