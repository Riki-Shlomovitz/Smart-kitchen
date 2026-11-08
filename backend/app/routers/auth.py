import time
from collections import defaultdict, deque

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..deps import get_current_user
from ..models import User
from ..schemas import LoginIn, RegisterIn, TokenOut, UserOut
from ..security import (create_access_token, create_refresh_token, decode_token,
                        hash_password, verify_password)

router = APIRouter(prefix="/auth", tags=["auth"])
REFRESH_COOKIE = "refresh_token"

# הגבלת קצב בזיכרון (בפריסה יעבור ל-Redis): 5 ניסיונות שגויים ב-15 דקות
_failures: dict[str, deque] = defaultdict(deque)


def _check_rate(email: str) -> None:
    window = settings.login_window_minutes * 60
    q = _failures[email]
    while q and time.time() - q[0] > window:
        q.popleft()
    if len(q) >= settings.login_max_attempts:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "יותר מדי ניסיונות, נסי שוב מאוחר יותר")


def _set_refresh(response: Response, user_id: int) -> None:
    response.set_cookie(REFRESH_COOKIE, create_refresh_token(user_id), httponly=True,
                        samesite="lax", max_age=settings.refresh_token_days * 86400)


@router.post("/register", response_model=TokenOut, status_code=201)
def register(data: RegisterIn, response: Response, db: Session = Depends(get_db)):
    email = data.email.lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "האימייל כבר רשום")
    user = User(email=email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    _set_refresh(response, user.id)
    return TokenOut(access_token=create_access_token(user.id))


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, response: Response, db: Session = Depends(get_db)):
    email = data.email.lower()
    _check_rate(email)
    user = db.scalar(select(User).where(User.email == email))
    if not user or not verify_password(data.password, user.password_hash):
        _failures[email].append(time.time())
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "אימייל או סיסמה שגויים")
    _failures.pop(email, None)
    _set_refresh(response, user.id)
    return TokenOut(access_token=create_access_token(user.id))


@router.post("/refresh", response_model=TokenOut)
def refresh(refresh_token: str | None = Cookie(default=None), db: Session = Depends(get_db)):
    user_id = decode_token(refresh_token, "refresh") if refresh_token else None
    if not user_id or not db.get(User, user_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "פג תוקף ההתחברות")
    return TokenOut(access_token=create_access_token(user_id))


@router.post("/logout", status_code=204)
def logout(response: Response):
    response.delete_cookie(REFRESH_COOKIE)


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
