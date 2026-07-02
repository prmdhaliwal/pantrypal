import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "download_recipes.py"


def load_script_module():
    spec = importlib.util.spec_from_file_location("download_recipes", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_download_recipes_script_writes_json_cache_to_output_path(tmp_path, monkeypatch):
    script = load_script_module()
    output_path = tmp_path / "recipes.json"
    calls = {}

    def fake_fetch(letters: str):
        calls["letters"] = letters
        return [{"id": "52772", "name": "Chicken Handi"}]

    def fake_write(recipes, path: Path):
        calls["recipes"] = recipes
        calls["path"] = path

    monkeypatch.setattr(script, "fetch_meals_by_letters", fake_fetch)
    monkeypatch.setattr(script, "write_recipe_cache", fake_write)

    result = script.main(["--letters", "ch", "--output", str(output_path)])

    assert result == 0
    assert calls == {
        "letters": "ch",
        "recipes": [{"id": "52772", "name": "Chicken Handi"}],
        "path": output_path,
    }
