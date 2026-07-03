import json
import warnings
from pathlib import Path
from typing import Any

import joblib

from app.recommender import RecipeCandidate


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RECIPE_CACHE = PROJECT_ROOT / "data" / "recipes.json"
DEFAULT_RECOMMENDER_MODEL = PROJECT_ROOT / "data" / "models" / "recipe_recommender.joblib"


def load_recipe_candidates(path: Path) -> list[RecipeCandidate]:
    raw_recipes = load_recipe_records(path)

    return [_recipe_from_json(recipe) for recipe in raw_recipes]


def load_recipe_records(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_default_recipes() -> list[RecipeCandidate]:
    return load_recipe_candidates(DEFAULT_RECIPE_CACHE)


def load_default_recipe_records() -> list[dict[str, Any]]:
    return load_recipe_records(DEFAULT_RECIPE_CACHE)


def load_optional_recommender_model(path: Path) -> Any | None:
    if not path.exists():
        return None

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="Setting the shape on a NumPy array has been deprecated.*",
            category=DeprecationWarning,
        )
        return joblib.load(path)


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
STARTER_RECIPE_RECORDS = load_default_recipe_records()
STARTER_RECOMMENDER_MODEL = load_optional_recommender_model(DEFAULT_RECOMMENDER_MODEL)
