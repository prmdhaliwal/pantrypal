import json
from pathlib import Path
from typing import Any

from app.recommender import RecipeCandidate


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RECIPE_CACHE = PROJECT_ROOT / "data" / "recipes.json"


def load_recipe_candidates(path: Path) -> list[RecipeCandidate]:
    raw_recipes = json.loads(path.read_text(encoding="utf-8"))

    return [_recipe_from_json(recipe) for recipe in raw_recipes]


def load_default_recipes() -> list[RecipeCandidate]:
    return load_recipe_candidates(DEFAULT_RECIPE_CACHE)


def _recipe_from_json(recipe: dict[str, Any]) -> RecipeCandidate:
    return RecipeCandidate(
        id=recipe["id"],
        name=recipe["name"],
        ingredients=recipe["ingredients"],
        image_url=recipe.get("imageUrl"),
        category=recipe.get("category"),
        area=recipe.get("area"),
        instructions_url=recipe.get("instructionsUrl"),
    )


STARTER_RECIPES = load_default_recipes()
