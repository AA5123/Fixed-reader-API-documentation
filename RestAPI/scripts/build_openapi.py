#!/usr/bin/env python3
"""
build_openapi.py
================
Bundle the modular ``RestAPI/`` tree back into a single self-contained OpenAPI
document (``RestAPI/openapi.bundled.yaml``).

It reads the root ``openapi.yaml`` and:
  * inlines each ``paths/<folder>/<file>.yaml`` as the path item,
  * reconstructs ``components.schemas`` from ``schemas/<bucket>/<Name>.yaml``,
  * converts every external file ``$ref`` back to an in-document
    ``#/components/schemas/<Name>`` reference (filenames == schema names),

then runs structural validation (and ``openapi-spec-validator`` if available).

Run:
    python RestAPI/scripts/build_openapi.py
"""

from __future__ import annotations

from collections import OrderedDict
from pathlib import Path

import yaml

REST_DIR = Path(__file__).resolve().parent.parent
ROOT_IN = REST_DIR / "openapi.yaml"
BUNDLED_OUT = REST_DIR / "FX90-rest-api.yaml"


def _represent_ordereddict(dumper, data):
    return dumper.represent_mapping("tag:yaml.org,2002:map", data.items())


yaml.add_representer(OrderedDict, _represent_ordereddict)
yaml.SafeDumper.add_representer(OrderedDict, _represent_ordereddict)


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def schema_name_from_ref(ref: str) -> str:
    """`../../schemas/common/gpi.v1.yaml` -> `gpi.v1`."""
    return Path(ref).name[: -len(".yaml")] if ref.endswith(".yaml") else Path(ref).name


def to_internal_refs(node):
    """Convert external *.yaml schema refs back to #/components/schemas/NAME."""
    if isinstance(node, dict):
        new = {}
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str) and value.endswith(".yaml"):
                name = schema_name_from_ref(value)
                new[key] = f"#/components/schemas/{name}"
            else:
                new[key] = to_internal_refs(value)
        return new
    if isinstance(node, list):
        return [to_internal_refs(v) for v in node]
    return node


def collect_refs(node, out):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str) and value.startswith("#/components/schemas/"):
                out.add(value.split("/")[-1])
            else:
                collect_refs(value, out)
    elif isinstance(node, list):
        for v in node:
            collect_refs(v, out)


def main() -> None:
    root = load_yaml(ROOT_IN)

    bundled = OrderedDict()
    for key in ("openapi", "info", "externalDocs", "servers", "tags"):
        if key in root:
            bundled[key] = root[key]

    # ----- paths -----
    paths_out = OrderedDict()
    op_count = 0
    for path, ref_obj in root.get("paths", {}).items():
        ref = ref_obj["$ref"]
        item = load_yaml((ROOT_IN.parent / ref).resolve())
        item = to_internal_refs(item)
        paths_out[path] = item
        op_count += sum(
            1 for m in item if m in ("get", "put", "post", "delete", "patch", "head", "options")
        )
    bundled["paths"] = paths_out

    # ----- components -----
    components = OrderedDict()
    src_components = root.get("components", {})
    if "securitySchemes" in src_components:
        components["securitySchemes"] = src_components["securitySchemes"]

    schemas_out = OrderedDict()
    for name, ref_obj in src_components.get("schemas", {}).items():
        ref = ref_obj["$ref"]
        body = load_yaml((ROOT_IN.parent / ref).resolve())
        schemas_out[name] = to_internal_refs(body)
    components["schemas"] = schemas_out
    bundled["components"] = components

    with BUNDLED_OUT.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(
            bundled, fh, sort_keys=False, allow_unicode=True, default_flow_style=False, width=4096
        )

    # ----- validation -----
    declared = set(schemas_out.keys())
    used: set = set()
    collect_refs(paths_out, used)
    collect_refs(schemas_out, used)
    missing = sorted(used - declared)

    print(f"Root document : {ROOT_IN.name}")
    print(f"Paths         : {len(paths_out)}")
    print(f"Operations    : {op_count}")
    print(f"Schemas       : {len(schemas_out)}")
    print(f"Refs used      : {len(used)}")
    print(f"Bundled output : {BUNDLED_OUT.name}")

    if missing:
        print("\nBROKEN REFERENCES (no matching schema file):")
        for m in missing:
            print(f"  #/components/schemas/{m}")
    else:
        print("Reference check: OK (all $ref targets resolve)")

    try:
        from openapi_spec_validator import validate as _validate  # type: ignore

        _validate(load_yaml(BUNDLED_OUT))
        print("openapi-spec-validator: VALID")
    except ImportError:
        print("openapi-spec-validator: not installed (skipped optional deep validation)")
    except Exception as exc:  # noqa: BLE001
        print(f"openapi-spec-validator: ISSUES -> {exc}")

    if missing:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
