from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_backend_requirements_pin_direct_dependencies():
    requirements_path = PROJECT_ROOT / "backend" / "requirements.txt"
    dependencies = [
        line.strip()
        for line in requirements_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    assert dependencies
    assert all("==" in dependency for dependency in dependencies)


def test_download_recipes_is_the_single_recipe_download_script():
    scripts_dir = PROJECT_ROOT / "scripts"

    assert (scripts_dir / "download_recipes.py").exists()
    assert not (scripts_dir / "fetch_mealdb_recipes.py").exists()
