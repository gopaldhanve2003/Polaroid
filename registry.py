from pathlib import Path

# Root-relative effects directory
EFFECTS_DIR = Path(__file__).parent / "effects"


def list_effects():
    """
    Return all available film effect names (from JSON files).
    """
    if not EFFECTS_DIR.exists():
        return []
    return sorted(p.stem for p in EFFECTS_DIR.glob("*.json"))


# Cached list for validation & CLI
EFFECTS = list_effects()

