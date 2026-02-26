from pathlib import Path
from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "ReceiptRipper"
    secret_key: str = os.getenv("APP_SECRET", "change-me-in-prod")
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = int(os.getenv("JWT_EXPIRES_MINUTES", "1440"))
    db_path: Path = Path(os.getenv("DB_PATH", "./data/receiptrip.db"))
    receipts_dir: Path = Path(os.getenv("RECEIPTS_DIR", "./data/receipts"))
    web_dist: Path = Path(os.getenv("WEB_DIST", "../web/dist"))
    ollama_enabled: bool = os.getenv("OLLAMA_ENABLED", "false").lower() == "true"
    ollama_url: str = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2")


settings = Settings()
settings.db_path.parent.mkdir(parents=True, exist_ok=True)
settings.receipts_dir.mkdir(parents=True, exist_ok=True)
