from pathlib import Path
import json
from datetime import datetime, timezone
import uuid

ROOT = Path(".")
ARTICLES_DIR = ROOT / "articles"
SHOWCASES_DIR = ROOT / "showcases"
OUTPUT = ROOT / "index.json"


def list_files(base: Path):
    if not base.exists():
        return []

    return sorted(str(p.relative_to(ROOT)) for p in base.rglob("*") if p.is_file())


def load_index():
    import json

    return json.load(open("index.json", "r"))


def rename_unindexed_files(new_index: dict, index: dict):
    unindexed_articles = set([i["name"] for i in new_index["articles"]]) - set(
        [i["name"] for i in index["articles"]]
    )
    unindexed_showcases = set([i["name"] for i in new_index["showcases"]]) - set(
        [i["name"] for i in index["showcases"]]
    )

    for unindexed_article in unindexed_articles:
        Path(unindexed_article).rename(f"{ARTICLES_DIR / uuid.uuid4().hex}.md")

    for unindexed_showcase in unindexed_showcases:
        Path(unindexed_showcase).rename(f"{SHOWCASES_DIR / uuid.uuid4().hex}.md")


data = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "articles": [
        {"name": f, "title": open(f, "r").read().split()[0]}
        for f in list_files(ARTICLES_DIR)
    ],
    "showcases": [
        {"name": f, "title": open(f, "r").read().split()[0]}
        for f in list_files(SHOWCASES_DIR)
    ],
}


index = load_index()

rename_unindexed_files(data, index)

data = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "articles": [
        {"name": f, "title": open(f, "r").readline()} for f in list_files(ARTICLES_DIR)
    ],
    "showcases": [
        {"name": f, "title": open(f, "r").readline()} for f in list_files(SHOWCASES_DIR)
    ],
}

with OUTPUT.open("w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Generated {OUTPUT}")
