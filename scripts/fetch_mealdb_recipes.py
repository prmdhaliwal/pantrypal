import argparse
import string
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "recipes.json"

sys.path.insert(0, str(BACKEND_ROOT))

from app.themealdb import fetch_meals_by_letters, write_recipe_cache  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch TheMealDB recipes into the local PantryPal cache."
    )
    parser.add_argument(
        "--letters",
        default=string.ascii_lowercase,
        help="First letters to fetch, for example 'abc'. Defaults to a-z.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Recipe cache output path.",
    )
    args = parser.parse_args(argv)

    recipes = fetch_meals_by_letters(args.letters)
    write_recipe_cache(recipes, args.output)

    print(f"Wrote {len(recipes)} recipes to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
