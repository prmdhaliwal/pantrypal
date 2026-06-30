from app.assistant import answer_cooking_question
from app.recipe_documents import RecipeDocument


class FakeLLMClient:
    def __init__(self) -> None:
        self.prompt = ""

    def generate(self, prompt: str) -> str:
        self.prompt = prompt
        return "You can make egg fried rice with your pantry ingredients."


def test_answer_cooking_question_returns_retrieved_context_without_provider():
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

    response = answer_cooking_question(
        question="What can I cook with rice?",
        pantry_ingredients=["eggs"],
        documents=documents,
    )

    assert response.providerConfigured is False
    assert response.answer == (
        "Assistant provider is not configured. "
        "Showing retrieved recipe context instead."
    )
    assert response.citations[0].model_dump() == {
        "recipeId": "fried-rice",
        "name": "Egg Fried Rice",
    }
    assert response.retrievedContext[0].model_dump() == {
        "recipeId": "fried-rice",
        "name": "Egg Fried Rice",
        "text": (
            "Name: Egg Fried Rice\n"
            "Ingredients: eggs, rice, soy sauce"
        ),
        "score": 0.29,
    }


def test_answer_cooking_question_uses_pantry_ingredients_for_retrieval():
    documents = [
        RecipeDocument(
            id="fried-rice",
            text="Name: Egg Fried Rice\nIngredients: eggs, rice, soy sauce",
            metadata={"recipe_id": "fried-rice", "name": "Egg Fried Rice"},
        )
    ]

    response = answer_cooking_question(
        question="What can I cook?",
        pantry_ingredients=["rice"],
        documents=documents,
    )

    assert [citation.recipeId for citation in response.citations] == ["fried-rice"]


def test_answer_cooking_question_prioritizes_selected_recipe_context():
    documents = [
        RecipeDocument(
            id="fried-rice",
            text="Name: Egg Fried Rice\nIngredients: eggs, rice, soy sauce",
            metadata={"recipe_id": "fried-rice", "name": "Egg Fried Rice"},
        ),
        RecipeDocument(
            id="tomato-pasta",
            text="Name: Tomato Pasta\nIngredients: pasta, tomato, garlic",
            metadata={"recipe_id": "tomato-pasta", "name": "Tomato Pasta"},
        ),
    ]

    response = answer_cooking_question(
        question="What can I cook with rice?",
        pantry_ingredients=["eggs"],
        documents=documents,
        selected_recipe_id="tomato-pasta",
    )

    assert [citation.recipeId for citation in response.citations] == [
        "tomato-pasta",
        "fried-rice",
    ]
    assert response.retrievedContext[0].score == 1.0


def test_answer_cooking_question_uses_llm_client_when_configured():
    documents = [
        RecipeDocument(
            id="fried-rice",
            text="Name: Egg Fried Rice\nIngredients: eggs, rice, soy sauce",
            metadata={"recipe_id": "fried-rice", "name": "Egg Fried Rice"},
        )
    ]
    llm_client = FakeLLMClient()

    response = answer_cooking_question(
        question="Can I cook this with eggs?",
        pantry_ingredients=["eggs", "rice"],
        documents=documents,
        llm_client=llm_client,
    )

    assert response.providerConfigured is True
    assert response.answer == "You can make egg fried rice with your pantry ingredients."
    assert "Question: Can I cook this with eggs?" in llm_client.prompt
    assert "Pantry ingredients: eggs, rice" in llm_client.prompt
    assert (
        "Context 1: Egg Fried Rice\n"
        "Name: Egg Fried Rice\n"
        "Ingredients: eggs, rice, soy sauce"
    ) in llm_client.prompt
    assert [citation.recipeId for citation in response.citations] == ["fried-rice"]
