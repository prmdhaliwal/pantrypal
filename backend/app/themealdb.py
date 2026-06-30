import json
import string
from pathlib import Path
from typing import Any

import httpx


THEMEALDB_BASE_URL = "https://www.themealdb.com/api/json/v1/1"


def normalize_meal(meal: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": meal["idMeal"],
        "name": meal["strMeal"],
        "ingredients": _ingredients_from_meal(meal),
        "imageUrl": meal.get("strMealThumb"),
        "category": meal.get("strCategory"),
        "area": meal.get("strArea"),
        "instructionsUrl": meal.get("strSource"),
    }


def fetch_meals_by_first_letter(
    letter: str,
    client: httpx.Client,
) -> list[dict[str, Any]]:
    response = client.get(
        f"{THEMEALDB_BASE_URL}/search.php",
        params={"f": letter.lower()},
    )
    response.raise_for_status()

    meals = response.json().get("meals") or []
    return [normalize_meal(meal) for meal in meals]


def fetch_meals_by_letters(
    letters: str = string.ascii_lowercase,
) -> list[dict[str, Any]]:
    recipes_by_id = {}

    with httpx.Client(timeout=20) as client:
        for letter in letters:
            for recipe in fetch_meals_by_first_letter(letter, client):
                recipes_by_id[recipe["id"]] = recipe

    return sorted(recipes_by_id.values(), key=lambda recipe: recipe["name"])


def write_recipe_cache(recipes: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(recipes, indent=2),
        encoding="utf-8",
    )


def _ingredients_from_meal(meal: dict[str, Any]) -> list[str]:
    ingredients = []

    for index in range(1, 21):
        ingredient = meal.get(f"strIngredient{index}")
        if ingredient and ingredient.strip():
            ingredients.append(ingredient.strip().lower())

    return ingredients
