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


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    ingredients: list[str] = Field(min_length=1)
    selectedRecipeId: str | None = None


class AskCitation(BaseModel):
    recipeId: str
    name: str


class RetrievedContext(BaseModel):
    recipeId: str
    name: str
    text: str
    score: float


class AskResponse(BaseModel):
    answer: str
    citations: list[AskCitation]
    retrievedContext: list[RetrievedContext]
    providerConfigured: bool
