from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from receiptrip.auth import get_current_user
from receiptrip.db import get_db
from receiptrip.models import Category, User
from receiptrip.schemas import CategoryIn

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("")
def list_categories(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Category).filter(Category.user_id == user.id).all()


@router.post("")
def create_category(payload: CategoryIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = Category(user_id=user.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{category_id}")
def update_category(category_id: int, payload: CategoryIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(Category).filter(Category.id == category_id, Category.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit()
    return item


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(Category).filter(Category.id == category_id, Category.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
