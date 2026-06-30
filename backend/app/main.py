from fastapi import FastAPI

from app.schemas import RecommendRequest, RecommendResponse


app = FastAPI(title="PantryPal AI")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest) -> RecommendResponse:
    return RecommendResponse(results=[])
