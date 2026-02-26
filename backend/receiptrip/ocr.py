import io
import re
from datetime import datetime
from PIL import Image
import cv2
import numpy as np
import pytesseract
from dateutil import parser


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    arr = np.array(image)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray)
    thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return thresh


def run_ocr(image_bytes: bytes) -> str:
    try:
        pre = preprocess_image(image_bytes)
        return pytesseract.image_to_string(pre)
    except Exception:
        return ""


def parse_receipt(text: str) -> dict:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    merchant = next((l for l in lines[:5] if l.isupper() and len(l) > 2), lines[0] if lines else "Unknown Merchant")

    total = 0
    total_re = re.compile(r"(?:TOTAL|AMOUNT|BALANCE DUE)[^\d]*(\d+[\.,]\d{2})", re.IGNORECASE)
    for line in lines:
        match = total_re.search(line)
        if match:
            total = int(float(match.group(1).replace(",", ".")) * 100)

    date_found = datetime.utcnow()
    for line in lines[:12]:
        try:
            date_found = parser.parse(line, fuzzy=True)
            break
        except Exception:
            continue

    return {"merchant": merchant, "amount_cents": total, "spent_at": date_found.isoformat()}
