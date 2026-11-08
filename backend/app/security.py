from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from .config import settings

_ph = PasswordHasher()
ALGO = "HS256"


def hash_password(password: str) -> str:
    return _ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        return _ph.verify(hashed, password)
    except VerifyMismatchError:
        return False


def _token(sub: int, kind: str, delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(sub), "type": kind, "iat": now, "exp": now + delta},
                      settings.secret_key, algorithm=ALGO)


def create_access_token(user_id: int) -> str:
    return _token(user_id, "access", timedelta(minutes=settings.access_token_minutes))


def create_refresh_token(user_id: int) -> str:
    return _token(user_id, "refresh", timedelta(days=settings.refresh_token_days))


def decode_token(token: str, kind: str) -> int | None:
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[ALGO])
    except jwt.PyJWTError:
        return None
    if data.get("type") != kind:
        return None
    return int(data["sub"])
