import httpx

from app.themealdb import fetch_meals_by_first_letter, normalize_meal


def test_normalize_meal_maps_themealdb_fields_to_recipe_cache_record():
    meal = {
        "idMeal": "52772",
        "strMeal": "Teriyaki Chicken Casserole",
        "strMealThumb": "https://example.test/chicken.jpg",
        "strCategory": "Chicken",
        "strArea": "Japanese",
        "strSource": "https://example.test/recipe",
        "strIngredient1": "Chicken",
        "strIngredient2": "Rice",
        "strIngredient3": "Soy Sauce",
        "strIngredient4": "",
        "strIngredient5": None,
    }

    recipe = normalize_meal(meal)

    assert recipe == {
        "id": "52772",
        "name": "Teriyaki Chicken Casserole",
        "ingredients": ["chicken", "rice", "soy sauce"],
        "imageUrl": "https://example.test/chicken.jpg",
        "category": "Chicken",
        "area": "Japanese",
        "instructionsUrl": "https://example.test/recipe",
    }


def test_fetch_meals_by_first_letter_uses_themealdb_search_endpoint():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/json/v1/1/search.php"
        assert request.url.params["f"] == "a"
        return httpx.Response(
            200,
            json={
                "meals": [
                    {
                        "idMeal": "52768",
                        "strMeal": "Apple Frangipan Tart",
                        "strMealThumb": None,
                        "strCategory": "Dessert",
                        "strArea": "British",
                        "strSource": None,
                        "strIngredient1": "Apple",
                        "strIngredient2": "Butter",
                    }
                ]
            },
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))

    recipes = fetch_meals_by_first_letter("a", client)

    assert recipes == [
        {
            "id": "52768",
            "name": "Apple Frangipan Tart",
            "ingredients": ["apple", "butter"],
            "imageUrl": None,
            "category": "Dessert",
            "area": "British",
            "instructionsUrl": None,
        }
    ]
