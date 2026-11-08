from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import Base, engine
from .routers import auth, health, ingredients
from .seed.loader import seed_all


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)  # בפריסה יוחלף ב-Alembic
    seed_all()
    yield


app = FastAPI(title="Cookly API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)
for r in (health.router, auth.router, ingredients.router):
    app.include_router(r)
