from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path(".")
ARTICLES_DIR = ROOT / "articles"
SHOWCASES_DIR = ROOT / "showcases"
OUTPUT = ROOT / "index.json"


def list_files(base: Path):
    if not base.exists():
        return []

    return sorted(str(p.relative_to(ROOT)) for p in base.rglob("*") if p.is_file())


data = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "articles": list_files(ARTICLES_DIR),
    "showcases": list_files(SHOWCASES_DIR),
}

with OUTPUT.open("w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Generated {OUTPUT}")
