from pydantic import BaseModel, Field


class RecommendRequest(BaseModel):
    ingredients: list[str] = Field(min_length=1)


class RecipeRecommendation(BaseModel):
    id: str
    name: str
    imageUrl: str | None = None
    category: str | None = None
    area: str | None = None
    matchedIngredients: list[str]
    missingIngredients: list[str]
    score: float
    instructionsUrl: str | None = None


class RecommendResponse(BaseModel):
    results: list[RecipeRecommendation]
