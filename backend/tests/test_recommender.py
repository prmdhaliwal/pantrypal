from app.recommender import RecipeCandidate, recommend_recipes


def test_recommend_recipes_ranks_by_ingredient_overlap():
    recipes = [
        RecipeCandidate(
            id="fried-rice",
            name="Egg Fried Rice",
            ingredients=["eggs", "rice", "soy sauce"],
            category="Rice",
            area="Chinese",
        ),
        RecipeCandidate(
            id="omelette",
            name="Simple Omelette",
            ingredients=["eggs", "cheese"],
            category="Breakfast",
            area="French",
        ),
    ]

    results = recommend_recipes(["eggs", "rice"], recipes)

    assert [recipe.id for recipe in results] == ["fried-rice", "omelette"]
    assert results[0].matchedIngredients == ["eggs", "rice"]
    assert results[0].missingIngredients == ["soy sauce"]
    assert results[0].score == 0.67


def test_recommend_recipes_normalizes_ingredient_input():
    recipes = [
        RecipeCandidate(
            id="rice-bowl",
            name="Rice Bowl",
            ingredients=["rice", "egg"],
        )
    ]

    results = recommend_recipes([" RICE ", "Egg"], recipes)

    assert len(results) == 1
    assert results[0].matchedIngredients == ["rice", "egg"]
    assert results[0].missingIngredients == []
    assert results[0].score == 1.0


def test_recommend_recipes_skips_recipes_with_no_matches():
    recipes = [
        RecipeCandidate(
            id="toast",
            name="Toast",
            ingredients=["bread", "butter"],
        )
    ]

    results = recommend_recipes(["rice"], recipes)

    assert results == []
