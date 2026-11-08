def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_register_login_me(client):
    r = client.post("/auth/register", json={"email": "foo@example.com", "password": "password123"})
    assert r.status_code == 201
    assert "refresh_token" in r.cookies
    token = client.post("/auth/login", json={"email": "foo@example.com", "password": "password123"}).json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.json()["email"] == "foo@example.com"
    assert client.post("/auth/refresh").status_code == 200


def test_duplicate_and_bad_login(client):
    body = {"email": "foo@example.com", "password": "password123"}
    client.post("/auth/register", json=body)
    assert client.post("/auth/register", json=body).status_code == 409
    for _ in range(5):
        assert client.post("/auth/login", json={**body, "password": "wrong-pass"}).status_code == 401
    assert client.post("/auth/login", json=body).status_code == 429


def test_me_requires_auth(client):
    assert client.get("/auth/me").status_code == 401


def test_ingredients_seed_and_synonyms(client):
    names = [i["name"] for i in client.get("/ingredients", params={"q": "שמנת לבישול"}).json()]
    assert "שמנת מתוקה" in names


def test_spin_rules_seeded(client):
    from app.database import SessionLocal
    from app.models import SpinRule
    with SessionLocal() as db:
        r = db.query(SpinRule).filter_by(cooking_method="גריל", dish_type="מרק").one()
        assert r.is_allowed is False
