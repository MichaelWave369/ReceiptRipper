import io
import json
import zipfile
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from receiptrip.auth import get_current_user
from receiptrip.config import settings
from receiptrip.db import get_db
from receiptrip.models import User
from receiptrip.schemas import WipeRequest

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/data.zip")
def export_data(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as zf:
        db_file = Path(settings.db_path)
        if db_file.exists():
            zf.write(db_file, arcname="receiptrip.db")
        for file in Path(settings.receipts_dir).glob("*"):
            zf.write(file, arcname=f"receipts/{file.name}")
        zf.writestr("meta.json", json.dumps({"app": "ReceiptRipper", "note": "local export"}))
    stream.seek(0)
    return StreamingResponse(stream, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=data.zip"})


@router.post("/wipe")
def wipe_data(payload: WipeRequest, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if payload.confirm != "WIPE MY DATA":
        raise HTTPException(status_code=400, detail="Confirm phrase mismatch")
    db.execute(text("DELETE FROM transactions"))
    db.execute(text("DELETE FROM receipts"))
    db.execute(text("DELETE FROM merchants"))
    db.execute(text("DELETE FROM envelopes"))
    db.execute(text("DELETE FROM categories"))
    db.execute(text("DELETE FROM exchange_rates"))
    db.commit()
    for file in Path(settings.receipts_dir).glob("*"):
        file.unlink(missing_ok=True)
    return {"ok": True}
