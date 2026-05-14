# tools/glossary_loader.py

import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def load_glossary_terms():
    path = Path(__file__).resolve().parent.parent / "reference" / "glossary.json"

    with path.open("r", encoding="utf-8") as file:
        terms = json.load(file)

    return sorted(terms, key=lambda item: item["term"].lower())