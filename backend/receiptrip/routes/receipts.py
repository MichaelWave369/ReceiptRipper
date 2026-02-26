import hashlib
import json
from pathlib import Path
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from receiptrip.auth import get_current_user
from receiptrip.categorize import categorize_transaction
from receiptrip.config import settings
from receiptrip.crypto import encrypt_bytes
from receiptrip.db import get_db
from receiptrip.models import Receipt, Transaction, User
from receiptrip.ocr import parse_receipt, run_ocr

router = APIRouter(prefix="/api/receipts", tags=["receipts"])


@router.post("/upload")
async def upload_receipt(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    raw = await file.read()
    sha = hashlib.sha256(raw).hexdigest()
    encrypted = encrypt_bytes(raw)
    stored_path = Path(settings.receipts_dir) / f"{sha}.bin"
    stored_path.write_bytes(encrypted)

    ocr_text = run_ocr(raw)
    parsed = parse_receipt(ocr_text)
    category_id, envelope_id, confidence = categorize_transaction(db, user.id, parsed.get("merchant", ""), ocr_text)

    receipt = Receipt(
        user_id=user.id,
        filename=file.filename,
        mime=file.content_type or "application/octet-stream",
        size=len(raw),
        sha256=sha,
        stored_path=str(stored_path),
        encrypted_bool=True,
        ocr_text=ocr_text,
        parsed_json=json.dumps(parsed),
    )
    db.add(receipt)
    db.flush()

    tx = Transaction(
        user_id=user.id,
        receipt_id=receipt.id,
        merchant=parsed.get("merchant", ""),
        category_id=category_id,
        envelope_id=envelope_id,
        amount_cents=parsed.get("amount_cents", 0),
        currency=user.default_currency,
        spent_at=datetime.fromisoformat(parsed.get("spent_at")) if parsed.get("spent_at") else datetime.utcnow(),
        note=f"OCR draft (confidence {confidence:.2f})",
    )
    db.add(tx)
    db.commit()
    db.refresh(receipt)
    db.refresh(tx)
    return {"receipt": receipt, "transaction_draft": tx}


@router.get("")
def list_receipts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Receipt).filter(Receipt.user_id == user.id).order_by(Receipt.created_at.desc()).all()


@router.get("/{receipt_id}")
def get_receipt(receipt_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(Receipt).filter(Receipt.id == receipt_id, Receipt.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item


@router.delete("/{receipt_id}")
def delete_receipt(receipt_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(Receipt).filter(Receipt.id == receipt_id, Receipt.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    try:
        Path(item.stored_path).unlink(missing_ok=True)
    except Exception:
        pass
    db.delete(item)
    db.commit()
    return {"ok": True}
