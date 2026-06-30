from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_recommend_returns_ranked_recipes_for_matching_ingredients():
    response = client.post("/recommend", json={"ingredients": ["eggs", "rice"]})

    assert response.status_code == 200
    results = response.json()["results"]

    assert [recipe["name"] for recipe in results] == [
        "Egg Fried Rice",
        "Simple Omelette",
    ]
    assert results[0]["matchedIngredients"] == ["eggs", "rice"]
    assert results[0]["missingIngredients"] == ["soy sauce"]
    assert results[0]["score"] == 0.67
