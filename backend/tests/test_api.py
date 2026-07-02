import pytest
from fastapi.testclient import TestClient

import app.main as main
from app.main import app


client = TestClient(app)


class FakeLLMClient:
    def generate(self, prompt: str) -> str:
        return "Generated answer from configured provider."


@pytest.fixture(autouse=True)
def disable_llm_provider(monkeypatch):
    monkeypatch.setattr(
        main,
        "build_llm_client_from_env",
        lambda: None,
        raising=False,
    )


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


def test_recommend_allows_frontend_dev_origin():
    response = client.options(
        "/recommend",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"


def test_cors_preflight_limits_methods_and_headers():
    response = client.options(
        "/ask",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    allowed_methods = response.headers["access-control-allow-methods"]
    assert "GET" in allowed_methods
    assert "POST" in allowed_methods
    assert "OPTIONS" in allowed_methods
    assert "PUT" not in allowed_methods
    assert "DELETE" not in allowed_methods


def test_cors_preflight_rejects_unexpected_headers():
    response = client.options(
        "/ask",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "x-openai-api-key",
        },
    )

    assert response.status_code == 400


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


def test_ask_uses_configured_llm_provider(monkeypatch):
    monkeypatch.setattr(
        main,
        "build_llm_client_from_env",
        lambda: FakeLLMClient(),
        raising=False,
    )

    response = client.post(
        "/ask",
        json={
            "question": "Can I cook this with eggs?",
            "ingredients": ["eggs", "rice"],
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["providerConfigured"] is True
    assert body["answer"] == "Generated answer from configured provider."


def test_ask_falls_back_when_llm_provider_config_is_invalid(monkeypatch):
    def raise_provider_error():
        raise ValueError("LLM_API_KEY is required")

    monkeypatch.setattr(
        main,
        "build_llm_client_from_env",
        raise_provider_error,
        raising=False,
    )

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
    assert body["retrievedContext"][0]["recipeId"] == "starter-egg-fried-rice"
