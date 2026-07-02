import pytest
from pydantic import ValidationError

from app.schemas import AskRequest, RecipeRecommendation, RecommendRequest, RecommendResponse


def test_recommend_request_requires_at_least_one_ingredient():
    with pytest.raises(ValidationError):
        RecommendRequest(ingredients=[])


def test_recommend_request_limits_ingredient_count_and_length():
    with pytest.raises(ValidationError):
        RecommendRequest(ingredients=["rice"] * 21)

    with pytest.raises(ValidationError):
        RecommendRequest(ingredients=["x" * 61])


def test_ask_request_limits_question_ingredients_and_selected_recipe_id():
    with pytest.raises(ValidationError):
        AskRequest(question="x" * 501, ingredients=["rice"])

    with pytest.raises(ValidationError):
        AskRequest(question="Can I cook this?", ingredients=["rice"] * 21)

    with pytest.raises(ValidationError):
        AskRequest(question="Can I cook this?", ingredients=["x" * 61])

    with pytest.raises(ValidationError):
        AskRequest(
            question="Can I cook this?",
            ingredients=["rice"],
            selectedRecipeId="recipe-" + ("x" * 121),
        )


def test_recommend_response_serializes_recipe_result():
    recipe = RecipeRecommendation(
        id="52772",
        name="Teriyaki Chicken Casserole",
        imageUrl="https://example.test/chicken.jpg",
        category="Chicken",
        area="Japanese",
        matchedIngredients=["chicken", "rice"],
        missingIngredients=["soy sauce"],
        score=0.67,
        instructionsUrl=None,
    )

    response = RecommendResponse(results=[recipe])

    assert response.model_dump() == {
        "results": [
            {
                "id": "52772",
                "name": "Teriyaki Chicken Casserole",
                "imageUrl": "https://example.test/chicken.jpg",
                "category": "Chicken",
                "area": "Japanese",
                "matchedIngredients": ["chicken", "rice"],
                "missingIngredients": ["soy sauce"],
                "score": 0.67,
                "instructionsUrl": None,
            }
        ]
    }
