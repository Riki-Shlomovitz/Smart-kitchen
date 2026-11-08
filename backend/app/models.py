"""מודל הנתונים לפי האפיון. נמנעים מפיצ'רים ייחודיים ל-PostgreSQL (מערכים -> JSON)."""
import enum
from datetime import datetime, timezone

from sqlalchemy import (JSON, Boolean, DateTime, Enum, Float, ForeignKey, Integer,
                        String, Text, UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class KosherType(str, enum.Enum):
    meat = "meat"
    dairy = "dairy"
    parve = "parve"


class Role(str, enum.Enum):
    user = "user"
    editor = "editor"
    admin = "admin"


class RecipeSource(str, enum.Enum):
    curated = "curated"
    ai = "ai"


class RecipeStatus(str, enum.Enum):
    draft = "draft"
    trial = "trial"
    published = "published"
    hidden = "hidden"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.user)
    wake_word: Mapped[str] = mapped_column(String(32), default="שף")
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Ingredient(Base):
    __tablename__ = "ingredients"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    synonyms: Mapped[list] = mapped_column(JSON, default=list)
    kosher_type: Mapped[KosherType] = mapped_column(Enum(KosherType))
    store_section: Mapped[str] = mapped_column(String(50))
    shelf_life_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_staple_default: Mapped[bool] = mapped_column(Boolean, default=False)


class FridgeItem(Base):
    __tablename__ = "fridge_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    quantity: Mapped[float] = mapped_column(Float, default=1)
    unit: Mapped[str] = mapped_column(String(20), default="יח'")
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    compartment: Mapped[str] = mapped_column(String(20), default="fridge")  # fridge/freezer/pantry/spices
    ingredient: Mapped[Ingredient] = relationship()


class UserStaple(Base):
    __tablename__ = "user_staples"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)


class Recipe(Base):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    kosher_type: Mapped[KosherType] = mapped_column(Enum(KosherType))
    dish_type: Mapped[str] = mapped_column(String(30))
    cooking_method: Mapped[str] = mapped_column(String(30))
    total_minutes: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[str] = mapped_column(String(20), default="beginner")
    servings: Mapped[int] = mapped_column(Integer, default=4)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source: Mapped[RecipeSource] = mapped_column(Enum(RecipeSource), default=RecipeSource.curated)
    status: Mapped[RecipeStatus] = mapped_column(Enum(RecipeStatus), default=RecipeStatus.draft)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        cascade="all, delete-orphan", back_populates="recipe")
    steps: Mapped[list["RecipeStep"]] = relationship(
        cascade="all, delete-orphan", order_by="RecipeStep.order", back_populates="recipe")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)
    quantity: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(20))
    is_main: Mapped[bool] = mapped_column(Boolean, default=False)
    recipe: Mapped[Recipe] = relationship(back_populates="ingredients")
    ingredient: Mapped[Ingredient] = relationship()


class RecipeStep(Base):
    __tablename__ = "recipe_steps"
    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), index=True)
    order: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    timer_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_waiting_step: Mapped[bool] = mapped_column(Boolean, default=False)
    recipe: Mapped[Recipe] = relationship(back_populates="steps")


class CookSession(Base):
    __tablename__ = "cook_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    servings: Mapped[int] = mapped_column(Integer)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)


class Favorite(Base):
    __tablename__ = "favorites"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), primary_key=True)


class ShoppingItem(Base):
    __tablename__ = "shopping_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    quantity: Mapped[float] = mapped_column(Float, default=1)
    unit: Mapped[str] = mapped_column(String(20), default="יח'")
    source_recipe_id: Mapped[int | None] = mapped_column(ForeignKey("recipes.id"), nullable=True)
    is_bought: Mapped[bool] = mapped_column(Boolean, default=False)


class SpinRule(Base):
    __tablename__ = "spin_rules"
    __table_args__ = (UniqueConstraint("cooking_method", "dish_type"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    cooking_method: Mapped[str] = mapped_column(String(30))
    dish_type: Mapped[str] = mapped_column(String(30))
    is_allowed: Mapped[bool] = mapped_column(Boolean, default=True)


class SpinHistory(Base):
    __tablename__ = "spin_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    cooking_method: Mapped[str] = mapped_column(String(30))
    dish_type: Mapped[str] = mapped_column(String(30))
    recipe_id: Mapped[int | None] = mapped_column(ForeignKey("recipes.id"), nullable=True)
    spun_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
