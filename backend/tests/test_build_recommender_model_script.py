import importlib.util
import json
import warnings
from pathlib import Path

import joblib


SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "build_recommender_model.py"


def load_script_module():
    spec = importlib.util.spec_from_file_location("build_recommender_model", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_build_recommender_model_script_writes_loadable_joblib_model(tmp_path):
    script = load_script_module()
    recipe_cache = tmp_path / "recipes.json"
    output_path = tmp_path / "recipe_recommender.joblib"
    recipe_cache.write_text(
        json.dumps(
            [
                {
                    "id": "fried-rice",
                    "name": "Egg Fried Rice",
                    "ingredients": ["eggs", "rice", "soy sauce"],
                },
                {
                    "id": "tomato-pasta",
                    "name": "Tomato Pasta",
                    "ingredients": ["pasta", "tomato", "garlic"],
                },
            ]
        ),
        encoding="utf-8",
    )

    result = script.main(["--input", str(recipe_cache), "--output", str(output_path)])

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="Setting the shape on a NumPy array has been deprecated.*",
            category=DeprecationWarning,
        )
        recommender = joblib.load(output_path)
    ranked = recommender.rank(["rice", "soy sauce"], top_k=1)
    assert result == 0
    assert output_path.exists()
    assert ranked[0].recipe.id == "fried-rice"
