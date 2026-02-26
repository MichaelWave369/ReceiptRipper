from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .db import Base, engine
from .routes import auth, categories, envelopes, export, fx, receipts, reports, transactions

Base.metadata.create_all(bind=engine)
app = FastAPI(title="ReceiptRipper")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(receipts.router)
app.include_router(transactions.router)
app.include_router(categories.router)
app.include_router(envelopes.router)
app.include_router(fx.router)
app.include_router(reports.router)
app.include_router(export.router)


@app.get("/api/healthz")
def healthz():
    return {"status": "ok"}


web_dist = Path(__file__).resolve().parents[2] / "web" / "dist"
if web_dist.exists():
    app.mount("/assets", StaticFiles(directory=web_dist / "assets"), name="assets")


@app.get("/{full_path:path}")
def spa(full_path: str):
    index = web_dist / "index.html"
    if index.exists() and not full_path.startswith("api"):
        return FileResponse(index)
    return {"message": "ReceiptRipper API"}
