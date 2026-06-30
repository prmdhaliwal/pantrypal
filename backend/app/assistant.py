from app.recipe_documents import RecipeDocument
from app.recipe_retriever import RetrievedRecipeDocument, retrieve_recipe_documents
from app.schemas import AskCitation, AskResponse, RetrievedContext


FALLBACK_ANSWER = (
    "Assistant provider is not configured. "
    "Showing retrieved recipe context instead."
)


def answer_cooking_question(
    question: str,
    pantry_ingredients: list[str],
    documents: list[RecipeDocument],
    selected_recipe_id: str | None = None,
) -> AskResponse:
    query = " ".join([question, *pantry_ingredients])
    retrieved_documents = retrieve_recipe_documents(query, documents)
    retrieved_documents = _prioritize_selected_recipe(
        selected_recipe_id,
        documents,
        retrieved_documents,
    )

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


def _prioritize_selected_recipe(
    selected_recipe_id: str | None,
    documents: list[RecipeDocument],
    retrieved_documents: list[RetrievedRecipeDocument],
) -> list[RetrievedRecipeDocument]:
    if selected_recipe_id is None:
        return retrieved_documents

    selected_document = _find_recipe_document(selected_recipe_id, documents)
    if selected_document is None:
        return retrieved_documents

    remaining_documents = [
        result
        for result in retrieved_documents
        if result.document.id != selected_document.id
    ]
    return [
        RetrievedRecipeDocument(document=selected_document, score=1.0),
        *remaining_documents,
    ]


def _find_recipe_document(
    recipe_id: str,
    documents: list[RecipeDocument],
) -> RecipeDocument | None:
    for document in documents:
        if document.id == recipe_id:
            return document

    return None
