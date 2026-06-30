import json

from app.recipe_catalog import load_recipe_candidates


def test_load_recipe_candidates_from_json_file(tmp_path):
    cache_path = tmp_path / "recipes.json"
    cache_path.write_text(
        json.dumps(
            [
                {
                    "id": "52772",
                    "name": "Teriyaki Chicken Casserole",
                    "ingredients": ["chicken", "rice", "soy sauce"],
                    "imageUrl": "https://example.test/chicken.jpg",
                    "category": "Chicken",
                    "area": "Japanese",
                    "instructionsUrl": "https://example.test/recipe",
                }
            ]
        ),
        encoding="utf-8",
    )

    recipes = load_recipe_candidates(cache_path)

    assert len(recipes) == 1
    assert recipes[0].id == "52772"
    assert recipes[0].name == "Teriyaki Chicken Casserole"
    assert recipes[0].ingredients == ["chicken", "rice", "soy sauce"]
    assert recipes[0].image_url == "https://example.test/chicken.jpg"
    assert recipes[0].category == "Chicken"
    assert recipes[0].area == "Japanese"
    assert recipes[0].instructions_url == "https://example.test/recipe"
