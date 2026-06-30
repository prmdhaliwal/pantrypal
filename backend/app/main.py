from fastapi import FastAPI

from app.recipe_catalog import STARTER_RECIPES
from app.recommender import recommend_recipes
from app.schemas import RecommendRequest, RecommendResponse


app = FastAPI(title="PantryPal AI")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest) -> RecommendResponse:
    return RecommendResponse(
        results=recommend_recipes(request.ingredients, STARTER_RECIPES)
    )
