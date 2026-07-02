from typing import Annotated

from pydantic import BaseModel, Field


Ingredient = Annotated[str, Field(min_length=1, max_length=60)]
Question = Annotated[str, Field(min_length=1, max_length=500)]
RecipeId = Annotated[str, Field(min_length=1, max_length=120)]


class RecommendRequest(BaseModel):
    ingredients: list[Ingredient] = Field(min_length=1, max_length=20)


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
    question: Question
    ingredients: list[Ingredient] = Field(min_length=1, max_length=20)
    selectedRecipeId: RecipeId | None = None


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
