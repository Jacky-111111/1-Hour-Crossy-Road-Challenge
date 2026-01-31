"""
Persist best score to local JSON file.
"""

import json
from pathlib import Path

import settings


def get_save_path() -> Path:
    """Path to save file (next to main or in user dir)."""
    base = Path(__file__).resolve().parent.parent
    return base.parent / settings.SAVE_FILE


def load_best_score() -> int:
    """Load best score from file; 0 if missing."""
    path = get_save_path()
    if not path.exists():
        return 0
    try:
        with open(path, "r") as f:
            data = json.load(f)
            return int(data.get("best_score", 0))
    except Exception:
        return 0


def save_best_score(score: int) -> None:
    """Write best score to file."""
    path = get_save_path()
    try:
        with open(path, "w") as f:
            json.dump({"best_score": score}, f, indent=2)
    except Exception:
        pass
