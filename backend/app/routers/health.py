from fastapi import APIRouter

from ..config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok", "ai_configured": bool(settings.openai_api_key)}
