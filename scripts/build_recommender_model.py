import argparse
import sys
from pathlib import Path

import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
DEFAULT_INPUT = PROJECT_ROOT / "data" / "recipes.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "models" / "recipe_recommender.joblib"

sys.path.insert(0, str(BACKEND_ROOT))

from app.recipe_catalog import load_recipe_candidates  # noqa: E402
from app.recommender_model import train_recipe_recommender  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Train and save the PantryPal TF-IDF recipe recommender model."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Recipe JSON cache input path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Joblib model output path.",
    )
    args = parser.parse_args(argv)

    recipes = load_recipe_candidates(args.input)
    recommender = train_recipe_recommender(recipes)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(recommender, args.output)

    print(f"Wrote recommender model for {len(recipes)} recipes to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
