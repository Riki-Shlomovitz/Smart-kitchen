import json
from pathlib import Path

from sqlalchemy import select

from ..database import SessionLocal
from ..models import Ingredient, SpinRule

HERE = Path(__file__).parent


def seed_all() -> None:
    """טעינה ראשונית אידמפוטנטית של מאגר מצרכים וטבלת התאמות המכונה."""
    with SessionLocal() as db:
        if not db.scalar(select(Ingredient.id).limit(1)):
            for row in json.loads((HERE / "ingredients.json").read_text("utf-8")):
                db.add(Ingredient(**row))
        if not db.scalar(select(SpinRule.id).limit(1)):
            data = json.loads((HERE / "spin_rules.json").read_text("utf-8"))
            bad = {tuple(p) for p in data["disallowed"]}
            for m in data["methods"]:
                for d in data["dishes"]:
                    db.add(SpinRule(cooking_method=m, dish_type=d, is_allowed=(m, d) not in bad))
        db.commit()
