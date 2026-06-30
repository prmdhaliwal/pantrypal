from app.recipe_documents import RecipeDocument
from app.recipe_retriever import retrieve_recipe_documents
from app.schemas import AskCitation, AskResponse, RetrievedContext


FALLBACK_ANSWER = (
    "Assistant provider is not configured. "
    "Showing retrieved recipe context instead."
)


def answer_cooking_question(
    question: str,
    pantry_ingredients: list[str],
    documents: list[RecipeDocument],
) -> AskResponse:
    query = " ".join([question, *pantry_ingredients])
    retrieved_documents = retrieve_recipe_documents(query, documents)

    return AskResponse(
        answer=FALLBACK_ANSWER,
        citations=[
            AskCitation(
                recipeId=result.document.metadata["recipe_id"],
                name=result.document.metadata["name"],
            )
            for result in retrieved_documents
        ],
        retrievedContext=[
            RetrievedContext(
                recipeId=result.document.metadata["recipe_id"],
                name=result.document.metadata["name"],
                text=result.document.text,
                score=result.score,
            )
            for result in retrieved_documents
        ],
        providerConfigured=False,
    )
