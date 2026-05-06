from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def index_by(items: list[dict], key: str) -> dict[str, dict]:
    result = {}

    for item in items:
        value = item.get(key)

        if value is None:
            raise ValueError(f"Missing key '{key}' in item: {item}")

        if value in result:
            raise ValueError(f"Duplicate value '{value}' for key '{key}'")

        result[value] = item

    return result