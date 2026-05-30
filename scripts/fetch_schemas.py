"""
Fetches avatar style definition JSONs from https://github.com/dicebear/styles
and saves them to src/dicebear/styles/schemas/.

Usage: python scripts/fetch_schemas.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests

GITHUB_CONTENTS_API = "https://api.github.com/repos/dicebear/styles/contents/src"
RAW_BASE = "https://raw.githubusercontent.com/dicebear/styles/main/src"
SCHEMAS_DIR = Path(__file__).parent.parent / "src" / "dicebear" / "styles" / "schemas"


def fetch() -> int:
    SCHEMAS_DIR.mkdir(parents=True, exist_ok=True)

    print("Listing styles from dicebear/styles repo...")
    resp = requests.get(GITHUB_CONTENTS_API, timeout=30)
    resp.raise_for_status()
    files = resp.json()

    json_files = [f for f in files if f["name"].endswith(".json")]
    print(f"Found {len(json_files)} style files\n")

    for entry in json_files:
        name = entry["name"]
        print(f"  Downloading {name}...")
        raw = requests.get(entry["download_url"], timeout=30)
        raw.raise_for_status()
        dest = SCHEMAS_DIR / name
        dest.write_text(json.dumps(raw.json(), indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nDone. {len(json_files)} schemas saved to {SCHEMAS_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(fetch())
