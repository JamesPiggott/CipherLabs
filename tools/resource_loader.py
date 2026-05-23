import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def load_resources():
    path = Path(__file__).resolve().parent.parent / "reference" / "resources.json"

    with path.open("r", encoding="utf-8") as file:
        resources = json.load(file)

    return sorted(
        resources,
        key=lambda item: (
            item.get("category", "").lower(),
            item.get("title", "").lower(),
        ),
    )