from app.recipe_documents import build_recipe_document, build_recipe_documents


def test_build_recipe_document_formats_searchable_text_and_metadata():
    recipe = {
        "id": "52772",
        "name": "Teriyaki Chicken Casserole",
        "ingredients": ["chicken", "rice", "soy sauce"],
        "category": "Chicken",
        "area": "Japanese",
        "tags": ["Casserole", "Dinner"],
        "instructions": "Bake until cooked through.",
    }

    document = build_recipe_document(recipe)

    assert document.id == "52772"
    assert document.metadata == {
        "recipe_id": "52772",
        "name": "Teriyaki Chicken Casserole",
        "category": "Chicken",
        "area": "Japanese",
    }
    assert document.text == (
        "Name: Teriyaki Chicken Casserole\n"
        "Category: Chicken\n"
        "Area: Japanese\n"
        "Ingredients: chicken, rice, soy sauce\n"
        "Tags: Casserole, Dinner\n"
        "Instructions: Bake until cooked through."
    )


def test_build_recipe_document_omits_empty_optional_sections():
    recipe = {
        "id": "starter-rice",
        "name": "Rice Bowl",
        "ingredients": ["rice", "egg"],
        "category": None,
        "area": "",
        "tags": [],
        "instructions": None,
    }

    document = build_recipe_document(recipe)

    assert document.metadata == {
        "recipe_id": "starter-rice",
        "name": "Rice Bowl",
    }
    assert document.text == (
        "Name: Rice Bowl\n"
        "Ingredients: rice, egg"
    )


def test_build_recipe_documents_preserves_recipe_order():
    recipes = [
        {"id": "a", "name": "A", "ingredients": ["rice"]},
        {"id": "b", "name": "B", "ingredients": ["egg"]},
    ]

    documents = build_recipe_documents(recipes)

    assert [document.id for document in documents] == ["a", "b"]
