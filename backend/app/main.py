from fastapi import FastAPI

from app.assistant import LLMClient, answer_cooking_question
from app.llm_providers import build_llm_client_from_env
from app.recipe_catalog import STARTER_RECIPE_RECORDS, STARTER_RECIPES
from app.recipe_documents import build_recipe_documents
from app.recommender import recommend_recipes
from app.schemas import AskRequest, AskResponse, RecommendRequest, RecommendResponse


app = FastAPI(title="PantryPal AI")


def _build_optional_llm_client() -> LLMClient | None:
    try:
        return build_llm_client_from_env()
    except ValueError:
        return None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest) -> RecommendResponse:
    return RecommendResponse(
        results=recommend_recipes(request.ingredients, STARTER_RECIPES)
    )


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    documents = build_recipe_documents(STARTER_RECIPE_RECORDS)
    return answer_cooking_question(
        question=request.question,
        pantry_ingredients=request.ingredients,
        documents=documents,
        selected_recipe_id=request.selectedRecipeId,
        llm_client=_build_optional_llm_client(),
    )
