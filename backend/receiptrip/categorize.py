import json
import httpx
from sqlalchemy.orm import Session

from .config import settings
from .models import Category, Merchant


def categorize_transaction(db: Session, user_id: int, merchant_name: str, ocr_text: str) -> tuple[int | None, int | None, float]:
    merchant = db.query(Merchant).filter(Merchant.user_id == user_id, Merchant.name.ilike(merchant_name)).first()
    if merchant and merchant.category_id:
        rules = json.loads(merchant.rules_json or "{}")
        return merchant.category_id, rules.get("envelope_id"), 0.95

    categories = db.query(Category).filter(Category.user_id == user_id).all()
    text = (merchant_name + " " + ocr_text).lower()
    for cat in categories:
        for keyword in json.loads(cat.keywords_json or "[]"):
            if keyword.lower() in text:
                return cat.id, None, 0.75

    if settings.ollama_enabled:
        try:
            prompt = f"Categories: {[c.name for c in categories]} Merchant: {merchant_name} Text: {ocr_text[:500]}"
            resp = httpx.post(settings.ollama_url, json={"model": settings.ollama_model, "prompt": prompt, "stream": False}, timeout=4.0)
            if resp.status_code == 200:
                raw = resp.json().get("response", "").strip().lower()
                for cat in categories:
                    if cat.name.lower() in raw:
                        return cat.id, None, 0.6
        except Exception:
            pass

    return None, None, 0.0
