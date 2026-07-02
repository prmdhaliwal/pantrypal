from dataclasses import dataclass
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.recommender import RecipeCandidate


@dataclass(frozen=True)
class RecipeSimilarity:
    recipe: RecipeCandidate
    similarity: float


@dataclass(frozen=True)
class TrainedRecipeRecommender:
    recipes: list[RecipeCandidate]
    vectorizer: TfidfVectorizer
    recipe_matrix: Any

    def rank(
        self,
        pantry_ingredients: list[str],
        top_k: int = 5,
    ) -> list[RecipeSimilarity]:
        if top_k <= 0:
            return []

        query_text = build_pantry_ingredient_text(pantry_ingredients)
        if not query_text:
            return []

        query_matrix = self.vectorizer.transform([query_text])
        similarities = cosine_similarity(query_matrix, self.recipe_matrix).ravel()
        ranked_indexes = sorted(
            range(len(self.recipes)),
            key=lambda index: (-similarities[index], self.recipes[index].name),
        )

        return [
            RecipeSimilarity(
                recipe=self.recipes[index],
                similarity=round(float(similarities[index]), 4),
            )
            for index in ranked_indexes
            if similarities[index] > 0
        ][:top_k]


def train_recipe_recommender(
    recipes: list[RecipeCandidate],
) -> TrainedRecipeRecommender:
    recipe_texts = [
        build_recipe_ingredient_text(recipe)
        for recipe in recipes
    ]
    vectorizer = TfidfVectorizer()
    recipe_matrix = vectorizer.fit_transform(recipe_texts)

    return TrainedRecipeRecommender(
        recipes=recipes,
        vectorizer=vectorizer,
        recipe_matrix=recipe_matrix,
    )


def build_recipe_ingredient_text(recipe: RecipeCandidate) -> str:
    return build_pantry_ingredient_text(recipe.ingredients)


def build_pantry_ingredient_text(ingredients: list[str]) -> str:
    return " ".join(
        _normalize_ingredient(ingredient)
        for ingredient in ingredients
        if _normalize_ingredient(ingredient)
    )


def _normalize_ingredient(ingredient: str) -> str:
    return " ".join(ingredient.lower().strip().split())
