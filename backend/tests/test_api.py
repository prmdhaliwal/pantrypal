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


def test_ask_returns_assistant_fallback_with_recipe_context():
    response = client.post(
        "/ask",
        json={
            "question": "What can I cook with rice?",
            "ingredients": ["eggs"],
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["providerConfigured"] is False
    assert body["answer"] == (
        "Assistant provider is not configured. "
        "Showing retrieved recipe context instead."
    )
    assert body["citations"][0] == {
        "recipeId": "starter-egg-fried-rice",
        "name": "Egg Fried Rice",
    }
    assert body["retrievedContext"][0]["recipeId"] == "starter-egg-fried-rice"
    assert body["retrievedContext"][0]["score"] == 0.29


def test_ask_prioritizes_selected_recipe_context():
    response = client.post(
        "/ask",
        json={
            "question": "What can I cook with rice?",
            "ingredients": ["eggs"],
            "selectedRecipeId": "starter-tomato-pasta",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["citations"][0] == {
        "recipeId": "starter-tomato-pasta",
        "name": "Tomato Pasta",
    }
    assert body["retrievedContext"][0]["recipeId"] == "starter-tomato-pasta"
    assert body["retrievedContext"][0]["score"] == 1.0
