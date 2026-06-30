import pytest
from pydantic import ValidationError

from app.schemas import RecipeRecommendation, RecommendRequest, RecommendResponse


def test_recommend_request_requires_at_least_one_ingredient():
    with pytest.raises(ValidationError):
        RecommendRequest(ingredients=[])


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
