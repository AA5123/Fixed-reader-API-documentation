#!/usr/bin/env python3
"""Validate that every $ref in the generated schema tree resolves to a file.

Handles both JSON and YAML schema files. Only file ($ref) references are
checked; internal JSON-pointer refs ("#/...") are ignored.
"""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"


def load(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    return json.loads(text)


def walk(node, base_dir: Path, file_rel: str, broken: list, counter: list):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str):
                if value.startswith("#"):
                    continue
                counter[0] += 1
                target = (base_dir / value).resolve()
                if not target.exists():
                    broken.append((file_rel, value))
            else:
                walk(value, base_dir, file_rel, broken, counter)
    elif isinstance(node, list):
        for item in node:
            walk(item, base_dir, file_rel, broken, counter)


def main() -> None:
    files = sorted(
        list(SCHEMAS.rglob("*.json"))
        + list(SCHEMAS.rglob("*.yaml"))
        + list(SCHEMAS.rglob("*.yml"))
    )
    broken: list = []
    counter = [0]
    for f in files:
        try:
            data = load(f)
        except Exception as exc:  # noqa: BLE001
            broken.append((str(f.relative_to(ROOT)), f"<parse error: {exc}>"))
            continue
        walk(data, f.parent, str(f.relative_to(ROOT)), broken, counter)

    print(f"files scanned : {len(files)}")
    print(f"refs checked  : {counter[0]}")
    print(f"broken refs   : {len(broken)}")
    for b in broken[:30]:
        print("  BROKEN:", b)


if __name__ == "__main__":
    main()
