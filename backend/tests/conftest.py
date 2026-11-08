import os

os.environ["DATABASE_URL"] = "sqlite:///./test_cookly.db"

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


@pytest.fixture()
def client():
    Base.metadata.drop_all(engine)
    with TestClient(app) as c:  # lifespan יוצר טבלאות וטוען seed
        yield c
