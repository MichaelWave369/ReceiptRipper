from datetime import date, datetime
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    default_currency: str = "USD"




class LoginIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    default_currency: str

    class Config:
        from_attributes = True


class CategoryIn(BaseModel):
    name: str
    color: str = "#7c3aed"
    icon: str = "tag"
    keywords_json: str = "[]"


class EnvelopeIn(BaseModel):
    name: str
    monthly_budget_cents: int
    currency: str = "USD"
    rollover_bool: bool = False


class TransactionIn(BaseModel):
    receipt_id: int | None = None
    merchant: str = ""
    category_id: int | None = None
    envelope_id: int | None = None
    amount_cents: int
    currency: str = "USD"
    spent_at: datetime | None = None
    note: str = ""
    tax_cents: int | None = None
    tip_cents: int | None = None


class FXRateIn(BaseModel):
    base_currency: str
    quote_currency: str
    rate: float
    as_of_date: date
    source: str = "manual"


class WipeRequest(BaseModel):
    confirm: str
