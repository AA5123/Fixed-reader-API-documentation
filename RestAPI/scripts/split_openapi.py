#!/usr/bin/env python3
"""
split_openapi.py
================
Split the monolithic ``RestAPI/FX90.yaml`` into modular path files under
``RestAPI/paths/`` and regenerate ``RestAPI/openapi.yaml``.

WARNING: This script deletes and recreates ``RestAPI/paths/``. Do not run it
casually if you have manual edits in path files; export or commit first.
For day-to-day work, edit ``RestAPI/paths/`` and run ``build_openapi.py`` only.

Run:
   python RestAPI/scripts/split_openapi.py
"""

from __future__ import annotations

import re
import shutil
from copy import deepcopy
from pathlib import Path

import build_openapi as bo

REST_DIR = Path(__file__).resolve().parent.parent
SOURCE = REST_DIR / "FX90.yaml"
PATHS_DIR = REST_DIR / "paths"
ROOT_OUT = REST_DIR / "openapi.yaml"


def component_name_part(value: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z_]+", "_", value).strip("_")
    if not cleaned:
        cleaned = "schema"
    if cleaned[0].isdigit():
        cleaned = f"schema_{cleaned}"
    return cleaned


def operation_schema_base(api_path: str, method: str, operation: dict, suffix: str) -> str:
    op_id = operation.get("operationId")
    if op_id:
        base = component_name_part(str(op_id))
    else:
        base = component_name_part(f"{method}_{bo.path_filename(api_path)}")
    return f"{base}{suffix}"


def add_component_schema(schemas: dict, base_name: str, schema: dict) -> str:
    name = base_name
    index = 2
    while name in schemas and schemas[name] != schema:
        name = f"{base_name}{index}"
        index += 1
    schemas[name] = deepcopy(schema)
    return name


def component_ref(name: str) -> str:
    return f"../../openapi.yaml#/components/schemas/{name}"


def externalize_operation_schemas(path_item: dict, api_path: str, schemas: dict) -> int:
    """Move method request/response schemas into components and replace with refs."""
    refs_written = 0
    for method, operation in path_item.items():
        if method not in bo.HTTP_METHODS or not isinstance(operation, dict):
            continue

        request_body = operation.get("requestBody", {})
        for content in (request_body.get("content") or {}).values():
            if not isinstance(content, dict):
                continue
            schema = content.get("schema")
            if isinstance(schema, dict) and "$ref" not in schema:
                name = add_component_schema(
                    schemas,
                    operation_schema_base(api_path, method, operation, "Request"),
                    schema,
                )
                content["schema"] = {"$ref": component_ref(name)}
                refs_written += 1

        for status_code, response in (operation.get("responses") or {}).items():
            if not isinstance(response, dict):
                continue
            for content in (response.get("content") or {}).values():
                if not isinstance(content, dict):
                    continue
                schema = content.get("schema")
                if isinstance(schema, dict) and "$ref" not in schema:
                    suffix = "Response" if str(status_code) == "200" else f"Response{component_name_part(str(status_code))}"
                    name = add_component_schema(
                        schemas,
                        operation_schema_base(api_path, method, operation, suffix),
                        schema,
                    )
                    content["schema"] = {"$ref": component_ref(name)}
                    refs_written += 1
    return refs_written


def rewrite_refs(node, ref_resolver):
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
        return [rewrite_refs(value, ref_resolver) for value in node]
    return node


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Source not found: {SOURCE}")

    doc = bo.load_yaml(SOURCE)
    paths = doc.get("paths", {})
    schemas = deepcopy(doc.get("components", {}).get("schemas", {}))

    if PATHS_DIR.exists():
        shutil.rmtree(PATHS_DIR)

    by_folder: dict[str, int] = {}
    schema_refs = 0
    for api_path, item in paths.items():
        folder = bo.folder_for_path(api_path, item)
        fname = bo.path_filename(api_path)

        def resolver(target):
            return f"../../openapi.yaml#/components/schemas/{target}"

        rewritten_item = deepcopy(item)
        schema_refs += externalize_operation_schemas(rewritten_item, api_path, schemas)
        rewritten_item = rewrite_refs(rewritten_item, resolver)

        out = PATHS_DIR / folder / f"{fname}.yaml"
        bo.dump_yaml(out, rewritten_item)
        by_folder[folder] = by_folder.get(folder, 0) + 1

    root, missing = bo.build_openapi_root(doc, PATHS_DIR)
    if missing:
        raise SystemExit(f"Internal error: missing path files after split: {missing}")
    root["components"]["schemas"] = schemas
    bo.dump_yaml(ROOT_OUT, root, header=bo.AUTO_GENERATED_HEADER)

    print(f"Source            : {SOURCE.name}")
    print(f"Paths written     : {sum(by_folder.values())}")
    for folder in sorted(by_folder):
        print(f"  paths/{folder:<13}: {by_folder[folder]}")
    print(f"Method schema refs: {schema_refs}")
    print(f"Schemas (inline)  : {len(schemas)} in openapi.yaml")
    print(f"Root document     : {ROOT_OUT.relative_to(REST_DIR.parent)} (auto-generated)")


if __name__ == "__main__":
    main()
