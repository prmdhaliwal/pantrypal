from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.assistant import LLMClient, answer_cooking_question
from app.llm_providers import build_llm_client_from_env
from app.recipe_catalog import (
    STARTER_RECIPE_RECORDS,
    STARTER_RECOMMENDER_MODEL,
    STARTER_RECIPES,
)
from app.recipe_documents import build_recipe_documents
from app.recommender import recommend_ranked_recipes, recommend_recipes
from app.schemas import AskRequest, AskResponse, RecommendRequest, RecommendResponse


app = FastAPI(title="PantryPal AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


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
    if STARTER_RECOMMENDER_MODEL is not None:
        rankings = STARTER_RECOMMENDER_MODEL.rank(
            request.ingredients,
            top_k=len(STARTER_RECIPES),
        )
        return RecommendResponse(
            results=recommend_ranked_recipes(
                request.ingredients,
                [
                    (ranking.recipe, ranking.similarity)
                    for ranking in rankings
                ],
            )
        )

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
