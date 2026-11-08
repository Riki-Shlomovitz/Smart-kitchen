from pydantic import BaseModel, EmailStr, Field

from .models import KosherType, Role


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Role
    wake_word: str
    model_config = {"from_attributes": True}


class IngredientOut(BaseModel):
    id: int
    name: str
    synonyms: list[str]
    kosher_type: KosherType
    store_section: str
    shelf_life_days: int | None
    is_staple_default: bool
    model_config = {"from_attributes": True}
