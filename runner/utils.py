import json
from pathlib import Path

def load_dataset(path: str) -> list[dict]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
