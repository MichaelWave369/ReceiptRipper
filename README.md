# ReceiptRipper v0.1 MVP

Privacy-first, local-first, self-hosted expense tracker with OCR receipt scanning, envelope budgets, multi-currency reporting, and mobile-first UI.

> **Warning:** ReceiptRipper is not a bank, accountant, or tax advisor. You are responsible for legal, tax, and compliance obligations.

## Features
- FastAPI backend + SQLite storage (self-host friendly)
- Encrypted receipt file storage at rest (Fernet + app secret)
- OCR pipeline (Pillow + OpenCV + Tesseract)
- Heuristic receipt parsing (merchant/date/total)
- Rule/keyword categorization + optional localhost Ollama
- Envelope budgeting with monthly budget tracking
- Multi-currency transactions + manual FX rates
- Reports: summary, trend, and top merchants
- React + Vite + TypeScript mobile-first PWA shell
- Local export (zip) + destructive wipe endpoint with confirm phrase

## Repo layout
- `backend/` FastAPI app and tests
- `web/` React mobile-first frontend
- `docker-compose.yml` one-container self-host deploy

## Install (Local)
### Prereqs
- Python 3.11+
- Node 20+
- Tesseract OCR binary installed and in PATH

### Tesseract install
- **Ubuntu/Debian:** `sudo apt install tesseract-ocr`
- **macOS (brew):** `brew install tesseract`
- **Windows:** install from UB Mannheim builds and add install path to `PATH`

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$(pwd)
uvicorn receiptrip.main:app --reload
```

### Web
```bash
cd web
npm install
npm run dev
```

## Docker
```bash
cd web && npm install && npm run build && cd ..
docker compose up --build
```
App/API: http://localhost:8000

## Privacy & Security
- Local processing by default.
- No third-party OCR/LLM enabled by default.
- Optional Ollama only via localhost URL.
- Receipt bytes encrypted at rest with `APP_SECRET` derived key.
- Use strong secrets and secure host storage.

## API highlights
- `POST /api/receipts/upload` upload + OCR + draft transaction
- `GET /api/reports/summary` monthly spend by category/envelope
- `POST /api/fx/rates` set manual exchange rate
- `GET /api/export/data.zip` download db + receipts export
- `POST /api/export/wipe` destructive wipe requiring `WIPE MY DATA`

## Roadmap
- True end-to-end encrypted receipt vault
- Bank imports (OFX/CSV)
- Better ML categorization models
- Household/shared accounts
- Barcode scanning
