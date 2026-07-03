from dataclasses import dataclass
from typing import Iterable

from app.schemas import RecipeRecommendation


@dataclass(frozen=True)
class RecipeCandidate:
    id: str
    name: str
    ingredients: list[str]
    image_url: str | None = None
    category: str | None = None
    area: str | None = None
    instructions_url: str | None = None


def recommend_recipes(
    pantry_ingredients: list[str],
    recipes: list[RecipeCandidate],
) -> list[RecipeRecommendation]:
    normalized_pantry = {
        _normalize_ingredient(ingredient)
        for ingredient in pantry_ingredients
    }
    recommendations = []

    for recipe in recipes:
        recipe_ingredients = [
            _normalize_ingredient(ingredient)
            for ingredient in recipe.ingredients
        ]
        matched = [
            ingredient
            for ingredient in recipe_ingredients
            if ingredient in normalized_pantry
        ]

        if not matched:
            continue

        missing = [
            ingredient
            for ingredient in recipe_ingredients
            if ingredient not in normalized_pantry
        ]
        score = round(len(matched) / len(recipe_ingredients), 2)

        recommendations.append(_build_recommendation(recipe, matched, missing, score))

    return sorted(recommendations, key=lambda recipe: (-recipe.score, recipe.name))


def recommend_ranked_recipes(
    pantry_ingredients: list[str],
    ranked_recipes: Iterable[tuple[RecipeCandidate, float]],
) -> list[RecipeRecommendation]:
    normalized_pantry = {
        _normalize_ingredient(ingredient)
        for ingredient in pantry_ingredients
    }
    recommendations = []

    for recipe, similarity in ranked_recipes:
        recipe_ingredients = [
            _normalize_ingredient(ingredient)
            for ingredient in recipe.ingredients
        ]
        matched = [
            ingredient
            for ingredient in recipe_ingredients
            if ingredient in normalized_pantry
        ]

        if not matched:
            continue

        missing = [
            ingredient
            for ingredient in recipe_ingredients
            if ingredient not in normalized_pantry
        ]
        recommendations.append(
            _build_recommendation(
                recipe=recipe,
                matched=matched,
                missing=missing,
                score=round(similarity, 2),
            )
        )

    return recommendations


def _build_recommendation(
    recipe: RecipeCandidate,
    matched: list[str],
    missing: list[str],
    score: float,
) -> RecipeRecommendation:
    return RecipeRecommendation(
        id=recipe.id,
        name=recipe.name,
        imageUrl=recipe.image_url,
        category=recipe.category,
        area=recipe.area,
        matchedIngredients=matched,
        missingIngredients=missing,
        score=score,
        instructionsUrl=recipe.instructions_url,
    )


def _normalize_ingredient(ingredient: str) -> str:
    return " ".join(ingredient.lower().strip().split())
