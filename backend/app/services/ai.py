"""עטיפה יחידה לקריאות ל-OpenAI. המפתח נקרא רק מהשרת. כל פלט מאומת מול סכמת Pydantic."""
from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel, ValidationError

from ..config import settings

T = TypeVar("T", bound=BaseModel)

SYSTEM_GUARD = ("אתה עוזר בישול. ענה רק בנושאי מתכונים, מצרכים ובישול, ואל תצא מהנושא. "
                "החזר JSON בלבד התואם לסכמה.")
MAX_INPUT_CHARS = 500

_client: OpenAI | None = None


class AIUnavailable(Exception):
    pass


def _get_client() -> OpenAI:
    global _client
    if not settings.openai_api_key:
        raise AIUnavailable("OPENAI_API_KEY לא הוגדר")
    if _client is None:
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


def structured(prompt: str, schema: type[T], strong: bool = False) -> T:
    """קריאה למודל עם אימות סכמה וניסיון חוזר אחד."""
    model = settings.openai_model_strong if strong else settings.openai_model_light
    text = prompt[:MAX_INPUT_CHARS * 4]
    last: Exception | None = None
    for _ in range(2):
        resp = _get_client().chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": SYSTEM_GUARD},
                      {"role": "user", "content": text}],
        )
        try:
            return schema.model_validate_json(resp.choices[0].message.content or "")
        except ValidationError as e:
            last = e
    raise AIUnavailable(f"פלט AI לא תקין: {last}")
