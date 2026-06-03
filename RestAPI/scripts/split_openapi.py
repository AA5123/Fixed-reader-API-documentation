#!/usr/bin/env python3
"""
split_openapi.py
================
Split the monolithic ``RestAPI/FX90.yaml`` into a modular OpenAPI 3.1 structure:

  RestAPI/
    openapi.yaml                      root document ($ref to every path + schema)
    paths/<folder>/<path>.yaml        one file per REST path (all HTTP methods)
    schemas/<bucket>/<Name>.yaml      one file per reusable component schema

This script is part of the **independent REST API project** and never touches the
MQTT project. It only reads ``FX90.yaml`` and writes under ``RestAPI/``.

Run:
    python RestAPI/scripts/split_openapi.py
"""

from __future__ import annotations

import shutil
from collections import OrderedDict
from pathlib import Path

import yaml

REST_DIR = Path(__file__).resolve().parent.parent      # .../RestAPI
SOURCE = REST_DIR / "FX90.yaml"
PATHS_DIR = REST_DIR / "paths"
SCHEMAS_DIR = REST_DIR / "schemas"
ROOT_OUT = REST_DIR / "openapi.yaml"

# ---------------------------------------------------------------------------
# Folder assignment (driven by the operation's OpenAPI tag)
# ---------------------------------------------------------------------------
TAG_TO_FOLDER = {
    "Login": "login",
    "System": "system",
    "Network": "network",
    "Control": "control",
    "Region": "region",
    "Gpio": "gpio",
    "App-led": "led",
    "Stack-led": "led",
    "Logs": "logs",
    "Date&Time": "datetime",
    "Certificate": "certificates",
    "Firmware": "firmware",
    "userapp": "userapps",
    "Ble": "ble",
    "ImpinjGen2X": "impinj",
}

# Explicit per-path folder overrides (path string -> folder).
PATH_FOLDER_OVERRIDE = {
    "/cloud/cloudConfig": "network",
}

SCHEMA_BUCKETS = ("common", "requests", "responses")


# ---------------------------------------------------------------------------
# YAML helpers (preserve key order, avoid line wrapping)
# ---------------------------------------------------------------------------
def _represent_ordereddict(dumper, data):
    return dumper.represent_mapping("tag:yaml.org,2002:map", data.items())


yaml.add_representer(OrderedDict, _represent_ordereddict)
yaml.SafeDumper.add_representer(OrderedDict, _represent_ordereddict)


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def dump_yaml(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(
            data,
            fh,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
            width=4096,
        )


# ---------------------------------------------------------------------------
# Naming helpers
# ---------------------------------------------------------------------------
def path_filename(path: str) -> str:
    """`/cloud/apps/{appname}/start` -> `apps_appname_start`."""
    segments = [s for s in path.strip("/").split("/") if s]
    if segments and segments[0] == "cloud":
        segments = segments[1:]
    cleaned = [s.replace("{", "").replace("}", "") for s in segments]
    return "_".join(cleaned) if cleaned else "root"


def folder_for_path(path: str, item: dict) -> str:
    if path in PATH_FOLDER_OVERRIDE:
        return PATH_FOLDER_OVERRIDE[path]
    for method, op in item.items():
        if isinstance(op, dict) and op.get("tags"):
            tag = str(op["tags"][0]).strip()
            return TAG_TO_FOLDER.get(tag, "misc")
    return "misc"


def classify_schema(name: str) -> str:
    """Bucket a component schema into common / requests / responses."""
    low = name.lower()
    request_hints = ("set", "update", "_command", "config", "os_update")
    response_hints = (
        "get",
        "response",
        "stats",
        "version",
        "status",
        "capabilit",
        "supportedstandardlist",
        "supportedregionlist",
    )
    if low.startswith("set") or "update" in low or "_command" in low or low.endswith("config") or "config." in low or low in ("os_update.v1", "batching", "retention"):
        return "requests"
    if any(h in low for h in response_hints):
        return "responses"
    return "common"


# ---------------------------------------------------------------------------
# $ref rewriting
# ---------------------------------------------------------------------------
def rewrite_refs(node, ref_resolver):
    """Recursively rewrite ``#/components/schemas/NAME`` refs via ref_resolver."""
    if isinstance(node, dict):
        new = {}
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str) and value.startswith("#/components/schemas/"):
                name = value.split("/")[-1]
                new[key] = ref_resolver(name)
            else:
                new[key] = rewrite_refs(value, ref_resolver)
        return new
    if isinstance(node, list):
        return [rewrite_refs(v, ref_resolver) for v in node]
    return node


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Source not found: {SOURCE}")

    doc = load_yaml(SOURCE)
    paths = doc.get("paths", {})
    schemas = doc.get("components", {}).get("schemas", {})

    # Fresh generated dirs (only the generated subfolders, never the scripts).
    for folder in (PATHS_DIR, SCHEMAS_DIR):
        if folder.exists():
            shutil.rmtree(folder)

    # 1) Decide a bucket for every schema first (needed for relative refs).
    schema_bucket = {name: classify_schema(name) for name in schemas}

    # 2) Write schema files, rewriting cross-schema refs to relative file paths.
    for name, body in schemas.items():
        bucket = schema_bucket[name]

        def resolver(target, _from=bucket):
            tgt_bucket = schema_bucket.get(target, "common")
            if tgt_bucket == _from:
                return f"./{target}.yaml"
            return f"../{tgt_bucket}/{target}.yaml"

        rewritten = rewrite_refs(body, resolver)
        dump_yaml(SCHEMAS_DIR / bucket / f"{name}.yaml", rewritten)

    # 3) Write one path file per REST path (all methods together).
    path_index = []  # (path, folder, filename)
    for path, item in paths.items():
        folder = folder_for_path(path, item)
        fname = path_filename(path)

        def resolver(target):
            tgt_bucket = schema_bucket.get(target, "common")
            return f"../../schemas/{tgt_bucket}/{target}.yaml"

        rewritten_item = rewrite_refs(item, resolver)
        dump_yaml(PATHS_DIR / folder / f"{fname}.yaml", rewritten_item)
        path_index.append((path, folder, fname))

    # 4) Build the root openapi.yaml.
    root = OrderedDict()
    root["openapi"] = doc.get("openapi", "3.1.0")
    root["info"] = doc.get("info", {})
    if "externalDocs" in doc:
        root["externalDocs"] = doc["externalDocs"]
    if "servers" in doc:
        root["servers"] = doc["servers"]
    if "tags" in doc:
        root["tags"] = doc["tags"]

    root_paths = OrderedDict()
    for path, folder, fname in path_index:
        root_paths[path] = {"$ref": f"./paths/{folder}/{fname}.yaml"}
    root["paths"] = root_paths

    components = OrderedDict()
    sec = doc.get("components", {}).get("securitySchemes")
    if sec:
        components["securitySchemes"] = sec
    comp_schemas = OrderedDict()
    for name in schemas:
        bucket = schema_bucket[name]
        comp_schemas[name] = {"$ref": f"./schemas/{bucket}/{name}.yaml"}
    components["schemas"] = comp_schemas
    root["components"] = components

    dump_yaml(ROOT_OUT, root)

    # Report
    by_folder = {}
    for _, folder, _ in path_index:
        by_folder[folder] = by_folder.get(folder, 0) + 1
    by_bucket = {}
    for name in schemas:
        b = schema_bucket[name]
        by_bucket[b] = by_bucket.get(b, 0) + 1

    print(f"Source            : {SOURCE.name}")
    print(f"Paths written     : {len(path_index)}")
    for folder in sorted(by_folder):
        print(f"  paths/{folder:<13}: {by_folder[folder]}")
    print(f"Schemas written   : {len(schemas)}")
    for bucket in SCHEMA_BUCKETS:
        print(f"  schemas/{bucket:<10}: {by_bucket.get(bucket, 0)}")
    print(f"Root document     : {ROOT_OUT.relative_to(REST_DIR.parent)}")


if __name__ == "__main__":
    main()
