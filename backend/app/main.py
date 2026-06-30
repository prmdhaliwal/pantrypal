from fastapi import FastAPI

from app.assistant import answer_cooking_question
from app.recipe_catalog import STARTER_RECIPE_RECORDS, STARTER_RECIPES
from app.recipe_documents import build_recipe_documents
from app.recommender import recommend_recipes
from app.schemas import AskRequest, AskResponse, RecommendRequest, RecommendResponse


app = FastAPI(title="PantryPal AI")


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
    )
