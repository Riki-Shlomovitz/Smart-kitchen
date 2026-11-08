from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Ingredient
from ..schemas import IngredientOut

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("", response_model=list[IngredientOut])
def search_ingredients(q: str = Query("", max_length=50), db: Session = Depends(get_db)):
    """חיפוש עם השלמה אוטומטית לפי שם או שם נרדף."""
    rows = db.scalars(select(Ingredient).order_by(Ingredient.name)).all()
    q = q.strip()
    if not q:
        return rows[:50]
    return [i for i in rows if q in i.name or any(q in s for s in i.synonyms)][:20]
