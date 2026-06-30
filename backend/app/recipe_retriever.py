import re
from dataclasses import dataclass

from app.recipe_documents import RecipeDocument


@dataclass(frozen=True)
class RetrievedRecipeDocument:
    document: RecipeDocument
    score: float


def retrieve_recipe_documents(
    query: str,
    documents: list[RecipeDocument],
    limit: int = 3,
) -> list[RetrievedRecipeDocument]:
    query_tokens = _tokens(query)
    results = []

    for document in documents:
        overlap = query_tokens & _tokens(document.text)
        if not overlap:
            continue

        results.append(
            RetrievedRecipeDocument(
                document=document,
                score=round(len(overlap) / len(query_tokens), 2),
            )
        )

    ranked_results = sorted(
        results,
        key=lambda result: (
            -result.score,
            result.document.metadata.get("name", result.document.id),
        ),
    )
    return ranked_results[:limit]


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))
