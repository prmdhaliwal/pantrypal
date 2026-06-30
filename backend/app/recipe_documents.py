from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RecipeDocument:
    id: str
    text: str
    metadata: dict[str, str]


def build_recipe_document(recipe: dict[str, Any]) -> RecipeDocument:
    metadata = _metadata_from_recipe(recipe)
    sections = [
        ("Name", recipe["name"]),
        ("Category", recipe.get("category")),
        ("Area", recipe.get("area")),
        ("Ingredients", _format_items(recipe["ingredients"])),
        ("Tags", _format_items(recipe.get("tags", []))),
        ("Instructions", recipe.get("instructions")),
    ]
    text = "\n".join(
        f"{label}: {value}"
        for label, value in sections
        if value
    )

    return RecipeDocument(
        id=recipe["id"],
        text=text,
        metadata=metadata,
    )


def build_recipe_documents(recipes: list[dict[str, Any]]) -> list[RecipeDocument]:
    return [build_recipe_document(recipe) for recipe in recipes]


def _metadata_from_recipe(recipe: dict[str, Any]) -> dict[str, str]:
    metadata = {
        "recipe_id": recipe["id"],
        "name": recipe["name"],
    }

    for field in ("category", "area"):
        if recipe.get(field):
            metadata[field] = recipe[field]

    return metadata


def _format_items(items: list[str]) -> str:
    return ", ".join(items)
