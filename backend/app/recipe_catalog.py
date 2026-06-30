from app.recommender import RecipeCandidate


STARTER_RECIPES = [
    RecipeCandidate(
        id="starter-egg-fried-rice",
        name="Egg Fried Rice",
        ingredients=["eggs", "rice", "soy sauce"],
        category="Rice",
        area="Chinese",
    ),
    RecipeCandidate(
        id="starter-simple-omelette",
        name="Simple Omelette",
        ingredients=["eggs", "cheese"],
        category="Breakfast",
        area="French",
    ),
    RecipeCandidate(
        id="starter-tomato-pasta",
        name="Tomato Pasta",
        ingredients=["pasta", "tomato", "garlic"],
        category="Pasta",
        area="Italian",
    ),
]
