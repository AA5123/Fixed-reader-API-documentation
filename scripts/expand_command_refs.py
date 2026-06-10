#!/usr/bin/env python3
"""Expand local $ref values in schemas/commands into standalone JSON files.

Input : schemas/commands/**/*.json
Output: schemas/commands_expanded/**/*.json
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "schemas" / "commands"
OUT_DIR = ROOT / "schemas" / "commands_expanded"


def load_schema(path: Path) -> Any:
    text = path.read_text(encoding="utf-8-sig")
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    if suffix == ".json":
        return json.loads(text)
    raise ValueError(f"Unsupported schema file type: {path}")


def unescape_pointer_token(token: str) -> str:
    return token.replace("~1", "/").replace("~0", "~")


def resolve_json_pointer(document: Any, pointer: str) -> Any:
    if pointer == "" or pointer == "/":
        return document
    if pointer.startswith("/"):
        pointer = pointer[1:]

    current = document
    for raw_token in pointer.split("/"):
        token = unescape_pointer_token(raw_token)
        if isinstance(current, list):
            current = current[int(token)]
        else:
            current = current[token]
    return current


def split_ref(ref_value: str) -> tuple[str, str]:
    if "#" not in ref_value:
        return ref_value, ""
    file_part, pointer = ref_value.split("#", 1)
    return file_part, pointer


def resolve_ref_target(ref_value: str, current_file: Path) -> tuple[Any, Path]:
    file_part, pointer = split_ref(ref_value)

    if file_part:
        target_path = (current_file.parent / file_part).resolve()
        target_doc = load_schema(target_path)
    else:
        target_path = current_file
        target_doc = load_schema(current_file)

    if pointer:
        return resolve_json_pointer(target_doc, pointer), target_path
    return target_doc, target_path


def resolve_node(node: Any, current_file: Path, seen: tuple[Path, ...]) -> Any:
    if isinstance(node, list):
        return [resolve_node(item, current_file, seen) for item in node]

    if isinstance(node, dict):
        if "$ref" in node and isinstance(node["$ref"], str):
            ref_value = node["$ref"]
            target_node, target_file = resolve_ref_target(ref_value, current_file)

            if target_file in seen:
                chain = " -> ".join(str(p.relative_to(ROOT)) for p in (*seen, target_file))
                raise ValueError(f"Circular $ref detected: {chain}")

            expanded = resolve_node(target_node, target_file, (*seen, target_file))

            sibling_keys = [k for k in node.keys() if k != "$ref"]
            if sibling_keys and isinstance(expanded, dict):
                merged = copy.deepcopy(expanded)
                for key in sibling_keys:
                    merged[key] = resolve_node(node[key], current_file, seen)
                return merged

            if sibling_keys:
                wrapped = {"resolvedRef": expanded}
                for key in sibling_keys:
                    wrapped[key] = resolve_node(node[key], current_file, seen)
                return wrapped

            return expanded

        return {
            key: resolve_node(value, current_file, seen)
            for key, value in node.items()
        }

    return node


def main() -> None:
    if not SRC_DIR.exists():
        raise SystemExit(f"Source directory not found: {SRC_DIR}")

    files = sorted(SRC_DIR.rglob("*.json"))
    expanded_count = 0

    for src_file in files:
        rel = src_file.relative_to(SRC_DIR)
        out_file = OUT_DIR / rel
        out_file.parent.mkdir(parents=True, exist_ok=True)

        data = load_schema(src_file)
        expanded = resolve_node(data, src_file, (src_file,))
        out_file.write_text(json.dumps(expanded, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        expanded_count += 1

    print(f"Expanded files: {expanded_count}")
    print(f"Output folder : {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
