import csv
from pathlib import Path


DATASET_PATH = Path(__file__).resolve().parents[2] / "data" / "sample_recipes.csv"
REQUIRED_COLUMNS = {
    "recipe_id",
    "name",
    "category",
    "cuisine",
    "ingredients",
    "instructions",
    "image_url",
}


def test_sample_recipes_csv_has_step_two_recipe_fields():
    with DATASET_PATH.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    assert set(reader.fieldnames or []) == REQUIRED_COLUMNS
    assert 20 <= len(rows) <= 30

    for row in rows:
        for column in REQUIRED_COLUMNS:
            assert row[column].strip(), f"{row.get('name', 'recipe')} missing {column}"
        assert len([item for item in row["ingredients"].split(";") if item.strip()]) >= 3
