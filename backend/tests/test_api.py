from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_recommend_accepts_ingredients_and_returns_results_list():
    response = client.post("/recommend", json={"ingredients": ["eggs", "rice"]})

    assert response.status_code == 200
    assert response.json() == {"results": []}
