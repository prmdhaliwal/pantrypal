from app.recommender import RecipeCandidate
from app.recommender_model import build_recipe_ingredient_text, train_recipe_recommender


def test_build_recipe_ingredient_text_normalizes_recipe_ingredients():
    recipe = RecipeCandidate(
        id="teriyaki-chicken",
        name="Teriyaki Chicken",
        ingredients=[" Chicken Thighs ", "BASMATI   Rice", "Soy Sauce"],
    )

    text = build_recipe_ingredient_text(recipe)

    assert text == "chicken thighs basmati rice soy sauce"


def test_trained_recommender_ranks_recipe_by_pantry_similarity():
    recipes = [
        RecipeCandidate(
            id="fried-rice",
            name="Egg Fried Rice",
            ingredients=["eggs", "rice", "soy sauce"],
        ),
        RecipeCandidate(
            id="tomato-pasta",
            name="Tomato Pasta",
            ingredients=["pasta", "tomato", "garlic"],
        ),
        RecipeCandidate(
            id="omelette",
            name="Simple Omelette",
            ingredients=["eggs", "cheese"],
        ),
    ]
    recommender = train_recipe_recommender(recipes)

    results = recommender.rank(["rice", "soy sauce"], top_k=2)

    assert [result.recipe.id for result in results] == ["fried-rice"]
    assert results[0].similarity > 0
