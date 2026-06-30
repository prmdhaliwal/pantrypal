from app.recipe_documents import RecipeDocument
from app.recipe_retriever import retrieve_recipe_documents


def test_retrieve_recipe_documents_ranks_by_query_overlap():
    documents = [
        RecipeDocument(
            id="fried-rice",
            text=(
                "Name: Egg Fried Rice\n"
                "Ingredients: eggs, rice, soy sauce"
            ),
            metadata={"recipe_id": "fried-rice", "name": "Egg Fried Rice"},
        ),
        RecipeDocument(
            id="omelette",
            text=(
                "Name: Simple Omelette\n"
                "Ingredients: eggs, cheese"
            ),
            metadata={"recipe_id": "omelette", "name": "Simple Omelette"},
        ),
    ]

    results = retrieve_recipe_documents("eggs rice", documents)

    assert [result.document.id for result in results] == ["fried-rice", "omelette"]
    assert results[0].score == 1.0
    assert results[1].score == 0.5


def test_retrieve_recipe_documents_applies_limit():
    documents = [
        RecipeDocument(
            id="a",
            text="Name: A\nIngredients: rice",
            metadata={"recipe_id": "a", "name": "A"},
        ),
        RecipeDocument(
            id="b",
            text="Name: B\nIngredients: rice",
            metadata={"recipe_id": "b", "name": "B"},
        ),
    ]

    results = retrieve_recipe_documents("rice", documents, limit=1)

    assert [result.document.id for result in results] == ["a"]


def test_retrieve_recipe_documents_omits_documents_without_matches():
    documents = [
        RecipeDocument(
            id="toast",
            text="Name: Toast\nIngredients: bread, butter",
            metadata={"recipe_id": "toast", "name": "Toast"},
        )
    ]

    results = retrieve_recipe_documents("rice", documents)

    assert results == []
