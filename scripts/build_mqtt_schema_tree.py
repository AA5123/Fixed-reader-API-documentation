#!/usr/bin/env python3
"""
build_mqtt_schema_tree.py
=========================

Reorganizes the MQTT API schemas into a category-based folder structure.

Source (unchanged, authoritative):
  - Command Schemas.json
  - Response Schemas.json
  - Management Events.json
  - Tag Data Events.json

Generates:
  - schemas/commands/<category>/<command>.json
  - schemas/response/<category>/<command>_response.json
  - schemas/events/<event>.json                 (management event payloads)
  - schemas/tag-events/<event>.json             (tag read / directionality payloads)
  - schemas/references/<bucket>/<schema>.yaml   (shared $ref targets, bucketed, YAML)

Reference buckets group shared $ref targets by the source document that
introduces them:
  - request_payload/   only Command Schemas.json
  - response_payload/  only Response Schemas.json
  - events_payload/    only Management Events.json
  - tag_payload/       only Tag Data Events.json
  - shared/            reached from two or more of the above

Organization is driven by the Master Command List (category = source of truth),
NOT by REST endpoints. Commands present in the master list but absent from the
source schemas are emitted as explicit placeholders.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from collections import OrderedDict, defaultdict, deque
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from group_master_command_list import MASTER_ITEMS  # noqa: E402


ROOT = Path(__file__).resolve().parent.parent
CMD_SRC = ROOT / "Command Schemas.json"
RESP_SRC = ROOT / "Response Schemas.json"
EVENTS_SRC = ROOT / "Management Events.json"
TAG_DATA_SRC = ROOT / "Tag Data Events.json"

SCHEMAS_DIR = ROOT / "schemas"
COMMANDS_DIR = SCHEMAS_DIR / "commands"
RESPONSE_DIR = SCHEMAS_DIR / "response"
REFERENCES_DIR = SCHEMAS_DIR / "references"
EVENTS_DIR = SCHEMAS_DIR / "events"
TAG_EVENTS_DIR = SCHEMAS_DIR / "tag-events"

# Management event schemas exported to schemas/events/ (flat, one file per type).
EVENT_EXPORT_KEYS = (
    "async-events",
    "heartbeat",
    "firmwareUpdateProgress",
    "gpi",
    "gpo",
    "error",
    "warning",
    "userapp",
)
EVENT_EXPORT_SET = frozenset(EVENT_EXPORT_KEYS)

# On-disk filename when it must not collide with MQTT command schema names.
EVENT_FILE_NAMES = {
    "userapp": "userapp_event",
}


def event_file_name(schema_key: str, name_map: dict | None = None) -> str:
    mapping = name_map if name_map is not None else EVENT_FILE_NAMES
    return mapping.get(schema_key, schema_key)

# Tag data event schemas exported to schemas/tag-events/.
TAG_EVENT_EXPORT_KEYS = (
    "tagDataEvents",
    "modetagDataEvents",
    "directionalitytagDataEvents",
    "zoneHistory",
    "locationHistory",
)
TAG_EVENT_EXPORT_SET = frozenset(TAG_EVENT_EXPORT_KEYS)
TAG_EVENT_FILE_NAMES = {
    "modetagDataEvents": "mode_tag_data_events",
    "directionalitytagDataEvents": "directionality_tag_data_events",
}

REF_PREFIX = "#/components/schemas/"

# The command/response/event schema tree stays JSON; only the shared
# reference fragments are emitted as YAML (index files also stay JSON).
SCHEMA_EXT = ".json"
REF_EXT = ".yaml"

# Reference bucket folder names, keyed by the source document that introduces
# a shared $ref target. A target reached from more than one source -> "shared".
BUCKET_REQUEST = "request_payload"
BUCKET_RESPONSE = "response_payload"
BUCKET_EVENTS = "events_payload"
BUCKET_TAG = "tag_payload"
BUCKET_SHARED = "shared"

# Priority order when picking content for a multi-source (shared) reference.
SOURCE_PRIORITY = (BUCKET_REQUEST, BUCKET_RESPONSE, BUCKET_EVENTS, BUCKET_TAG)

# Master category label -> on-disk folder name (per requirement).
CATEGORY_FOLDER = {
    "Login": "login",
    "System": "system",
    "Network": "network",
    "Control": "control",
    "Region": "region",
    "Gpio": "gpio",
    "App-led": "app-led",
    "Stack-led": "stack-led",
    "Logs": "logs",
    "Date&Time": "date-time",
    "Certificate": "certificate",
    "Firmware": "firmware",
    "userapp": "userapp",
    "ImpinjGen2X": "impinjgen2x",
    "Ble": "ble",
}

CATEGORY_ORDER = list(CATEGORY_FOLDER.keys())


# ---------------------------------------------------------------------------
# Reference-file naming (global, stable, case-insensitively unique on Windows)
# ---------------------------------------------------------------------------
_ref_name_map: dict[str, str] = {}
_used_ref_names: set[str] = set()

# Bucket folder per reference key (populated by classify_reference_buckets()).
_ref_bucket: dict[str, str] = {}


def ref_filename(schema_key: str) -> str:
    """Return a stable, unique filename for a referenced schema key."""
    if schema_key in _ref_name_map:
        return _ref_name_map[schema_key]
    base = schema_key.replace("/", "_").replace("\\", "_").strip()
    candidate = f"{base}{REF_EXT}"
    lowered = candidate.lower()
    n = 2
    while lowered in _used_ref_names:
        candidate = f"{base}__{n}{REF_EXT}"
        lowered = candidate.lower()
        n += 1
    _used_ref_names.add(lowered)
    _ref_name_map[schema_key] = candidate
    return candidate


def bucket_of(schema_key: str) -> str:
    """Bucket folder for a reference key (default: shared)."""
    return _ref_bucket.get(schema_key, BUCKET_SHARED)


def ref_disk_path(schema_key: str) -> Path:
    """Absolute on-disk path of a reference file, inside its bucket folder."""
    return REFERENCES_DIR / bucket_of(schema_key) / ref_filename(schema_key)


def find_refs(node, found: set[str]) -> None:
    """Collect every #/components/schemas/* target name reachable in `node`."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str) and value.startswith(REF_PREFIX):
                found.add(value[len(REF_PREFIX):])
            else:
                find_refs(value, found)
    elif isinstance(node, list):
        for item in node:
            find_refs(item, found)


def _rel_ref(from_dir: Path, target_key: str) -> str:
    """Relative, POSIX-style $ref path from `from_dir` to a reference file."""
    rel = os.path.relpath(ref_disk_path(target_key), from_dir)
    return rel.replace(os.sep, "/")


def rewrite_refs(
    node,
    *,
    from_dir: Path,
    found: set[str],
    sibling_exports: frozenset | None = None,
    sibling_names: dict | None = None,
):
    """Deep-copy `node`, rewriting internal #/components/schemas/* refs.

    Every external ref is rewritten to a path relative to `from_dir` (the
    directory of the file being written), pointing into the target's bucket
    under schemas/references/. Refs whose target is an event/tag sibling export
    resolve to a bare sibling filename instead.
    """
    if isinstance(node, dict):
        out = {}
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str) and value.startswith(REF_PREFIX):
                target = value[len(REF_PREFIX):]
                found.add(target)
                if sibling_exports is not None and target in sibling_exports:
                    disk = event_file_name(target, sibling_names)
                    out[key] = f"{disk}{SCHEMA_EXT}"
                else:
                    out[key] = _rel_ref(from_dir, target)
            else:
                out[key] = rewrite_refs(
                    value,
                    from_dir=from_dir,
                    found=found,
                    sibling_exports=sibling_exports,
                    sibling_names=sibling_names,
                )
        return out
    if isinstance(node, list):
        return [
            rewrite_refs(
                v,
                from_dir=from_dir,
                found=found,
                sibling_exports=sibling_exports,
                sibling_names=sibling_names,
            )
            for v in node
        ]
    return node


def resolve_wrapper(schemas: dict, key: str):
    """Given a command/response key whose entry may be a thin {$ref, x-examples}
    wrapper, return (target_schema_dict, extra_examples)."""
    entry = schemas.get(key)
    if entry is None:
        return None, None
    if isinstance(entry, dict) and "$ref" in entry and entry["$ref"].startswith(REF_PREFIX):
        target_key = entry["$ref"][len(REF_PREFIX):]
        target = schemas.get(target_key, {})
        examples = entry.get("x-examples")
        return target, examples
    return entry, None


def _plain(data):
    """Convert OrderedDict (and nested) to plain types for clean YAML output."""
    if isinstance(data, dict):
        return {k: _plain(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_plain(v) for v in data]
    return data


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_yaml(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(
            _plain(data),
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
            width=4096,
        ),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Reference extraction queue: keys are resolved against whichever source doc
# introduced them, then written once to the flat references/ folder.
# ---------------------------------------------------------------------------
_ref_written: set[str] = set()
_ref_conflicts: list[str] = []


def queue_references(keys: set[str], source_schemas: dict, pending: deque) -> None:
    for k in keys:
        pending.append((k, source_schemas))


def flush_references(pending: deque) -> None:
    while pending:
        key, source_schemas = pending.popleft()
        if key in _ref_written:
            continue
        out_path = ref_disk_path(key)
        raw = source_schemas.get(key)
        if raw is None:
            # Referenced but undefined in this source: emit a stub so the
            # $ref still resolves to a real file.
            write_yaml(
                out_path,
                {"x-status": "unresolved-reference", "x-schema-key": key},
            )
            _ref_written.add(key)
            continue
        nested: set[str] = set()
        rewritten = rewrite_refs(raw, from_dir=out_path.parent, found=nested)
        write_yaml(out_path, rewritten)
        _ref_written.add(key)
        for nk in nested:
            if nk not in _ref_written:
                pending.append((nk, source_schemas))


def command_name_for(item: dict) -> str:
    schema = item["schema"]
    return schema if schema != "---" else item["api"]


def _reachable_refs(seeds: set[str], schemas: dict) -> set[str]:
    """All schema keys reachable from `seeds` via $ref within `schemas`."""
    seen: set[str] = set()
    dq: deque = deque(seeds)
    while dq:
        key = dq.popleft()
        if key in seen:
            continue
        seen.add(key)
        raw = schemas.get(key)
        if raw is None:
            continue
        nested: set[str] = set()
        find_refs(raw, nested)
        for nk in nested:
            if nk not in seen:
                dq.append(nk)
    return seen


def _seed_refs(keys, schemas) -> set[str]:
    """Top-level refs pulled in by a set of command/response/event bodies."""
    seeds: set[str] = set()
    for key in keys:
        target, _ = resolve_wrapper(schemas, key)
        find_refs(target or {}, seeds)
    return seeds


def classify_reference_buckets(
    cmd_schemas: dict,
    resp_schemas: dict,
    event_schema_sets: list[tuple[dict, tuple, str]],
) -> None:
    """Assign every shared $ref target to a bucket folder.

    A target reached from a single source uses that source's bucket; a target
    reached from two or more sources is placed in ``shared/``.
    """
    sources: dict[str, set[str]] = defaultdict(set)

    cmd_keys = [command_name_for(it) for it in MASTER_ITEMS
                if command_name_for(it) in cmd_schemas]
    for k in _reachable_refs(_seed_refs(cmd_keys, cmd_schemas), cmd_schemas):
        sources[k].add(BUCKET_REQUEST)

    resp_keys = []
    for it in MASTER_ITEMS:
        cmd = command_name_for(it)
        rkey = f"{cmd}_response"
        if rkey in resp_schemas:
            resp_keys.append(rkey)
        elif cmd in resp_schemas:
            resp_keys.append(cmd)
    for k in _reachable_refs(_seed_refs(resp_keys, resp_schemas), resp_schemas):
        sources[k].add(BUCKET_RESPONSE)

    for schemas, export_keys, tag in event_schema_sets:
        # Event/tag exports are inlined siblings; only their *external* refs
        # become reference files, tagged to the originating event source.
        present = [k for k in export_keys if k in schemas]
        for k in _reachable_refs(_seed_refs(present, schemas), schemas):
            if k in export_keys:
                continue
            sources[k].add(tag)

    for key, tags in sources.items():
        _ref_bucket[key] = next(iter(tags)) if len(tags) == 1 else BUCKET_SHARED


def _clean_generated_dirs() -> None:
    """Remove generated schema-tree folders so stale files never linger."""
    for d in (COMMANDS_DIR, RESPONSE_DIR, REFERENCES_DIR, EVENTS_DIR, TAG_EVENTS_DIR):
        if d.exists():
            shutil.rmtree(d)


def _event_schemas(src_path: Path) -> dict:
    if not src_path.exists():
        return {}
    doc = json.loads(src_path.read_text(encoding="utf-8"))
    return doc.get("components", {}).get("schemas", {})


def build() -> None:
    cmd_doc = json.loads(CMD_SRC.read_text(encoding="utf-8"))
    resp_doc = json.loads(RESP_SRC.read_text(encoding="utf-8"))
    cmd_schemas = cmd_doc.get("components", {}).get("schemas", {})
    resp_schemas = resp_doc.get("components", {}).get("schemas", {})

    _clean_generated_dirs()

    classify_reference_buckets(
        cmd_schemas,
        resp_schemas,
        [
            (_event_schemas(EVENTS_SRC), EVENT_EXPORT_KEYS, BUCKET_EVENTS),
            (_event_schemas(TAG_DATA_SRC), TAG_EVENT_EXPORT_KEYS, BUCKET_TAG),
        ],
    )

    pending: deque = deque()
    index_entries: list[dict] = []

    for item in MASTER_ITEMS:
        category = item["category"]
        folder = CATEGORY_FOLDER[category]
        command = command_name_for(item)
        resp_key_primary = f"{command}_response"

        request_present = command in cmd_schemas
        response_present = resp_key_primary in resp_schemas or command in resp_schemas

        # ----- command file -----
        cmd_path = COMMANDS_DIR / folder / f"{command}{SCHEMA_EXT}"
        if request_present:
            target, examples = resolve_wrapper(cmd_schemas, command)
            found: set[str] = set()
            body = rewrite_refs(target or {}, from_dir=cmd_path.parent, found=found)
            if examples and "x-examples" not in body:
                body["x-examples"] = examples
            write_json(cmd_path, body)
            queue_references(found, cmd_schemas, pending)
        else:
            write_json(
                cmd_path,
                {
                    "x-command": command,
                    "x-category": category,
                    "x-status": "Missing in Command Schema",
                    "description": item.get("desc", ""),
                },
            )

        # ----- response file -----
        resp_path = RESPONSE_DIR / folder / f"{command}_response{SCHEMA_EXT}"
        if response_present:
            rkey = resp_key_primary if resp_key_primary in resp_schemas else command
            target, examples = resolve_wrapper(resp_schemas, rkey)
            found = set()
            body = rewrite_refs(target or {}, from_dir=resp_path.parent, found=found)
            if examples and "x-examples" not in body:
                body["x-examples"] = examples
            write_json(resp_path, body)
            queue_references(found, resp_schemas, pending)
        else:
            write_json(
                resp_path,
                {
                    "x-command": command,
                    "x-category": category,
                    "x-status": "Missing in Response Schema",
                    "description": item.get("desc", ""),
                },
            )

        # ----- status + index -----
        if request_present and response_present:
            status = "synced"
        elif not request_present and not response_present:
            status = "missing_in_command_and_response_schema"
        elif not request_present:
            status = "missing_in_command_schema"
        else:
            status = "missing_in_response_schema"

        entry = OrderedDict(
            command=command,
            category=folder,
            request=str(cmd_path.relative_to(ROOT)).replace("\\", "/"),
            response=str(resp_path.relative_to(ROOT)).replace("\\", "/"),
            status=status,
            apiAlias=item.get("api", "---"),
            description=item.get("desc", ""),
        )
        index_entries.append(entry)

    flush_references(pending)

    mgmt_index = build_management_events()
    tag_index = build_tag_data_events()

    print(f"commands written : {sum(1 for _ in COMMANDS_DIR.rglob('*' + SCHEMA_EXT))}")
    print(f"responses written: {sum(1 for _ in RESPONSE_DIR.rglob('*' + SCHEMA_EXT))}")
    print(f"mgmt events      : {len(mgmt_index)}")
    print(f"tag-data events  : {len(tag_index)}")
    print(f"references written: {len(_ref_written)}")
    bucket_counts: dict[str, int] = defaultdict(int)
    for key in _ref_written:
        bucket_counts[bucket_of(key)] += 1
    for bucket in (BUCKET_REQUEST, BUCKET_RESPONSE, BUCKET_EVENTS, BUCKET_TAG, BUCKET_SHARED):
        print(f"  {bucket:<16}: {bucket_counts.get(bucket, 0)}")
    print(f"index entries    : {len(index_entries)}")


def build_schema_exports(
    src_path: Path,
    out_dir: Path,
    export_keys: tuple,
    export_set: frozenset,
    file_names: dict,
    missing_status: str,
    envelope_key: str | None = None,
) -> list[dict]:
    """Extract event/tag schemas from a Zebra OpenAPI components bundle."""
    if not src_path.exists():
        print(f"  WARNING: {src_path.name} not found — skipping {out_dir.name}/")
        return []

    doc = json.loads(src_path.read_text(encoding="utf-8"))
    schemas = doc.get("components", {}).get("schemas", {})
    pending: deque = deque()
    index_entries: list[dict] = []

    out_dir.mkdir(parents=True, exist_ok=True)
    gitkeep = out_dir / ".gitkeep"
    if gitkeep.exists():
        gitkeep.unlink()

    rel_prefix = str(out_dir.relative_to(ROOT)).replace("\\", "/")

    for key in export_keys:
        raw = schemas.get(key)
        disk_name = event_file_name(key, file_names)
        if raw is None:
            write_json(
                out_dir / f"{disk_name}{SCHEMA_EXT}",
                {"x-event": key, "x-status": missing_status},
            )
            index_entries.append(
                OrderedDict(
                    event=key,
                    file=disk_name,
                    path=f"{rel_prefix}/{disk_name}{SCHEMA_EXT}",
                    status="missing",
                    title=key,
                    description="",
                )
            )
            continue

        target, examples = resolve_wrapper(schemas, key)
        found: set[str] = set()
        out_path = out_dir / f"{disk_name}{SCHEMA_EXT}"
        body = rewrite_refs(
            target or {},
            from_dir=out_path.parent,
            found=found,
            sibling_exports=export_set,
            sibling_names=file_names,
        )
        if examples and "x-examples" not in body:
            body["x-examples"] = examples
        write_json(out_path, body)
        queue_references(found, schemas, pending)

        payload_types = []
        if envelope_key and key == envelope_key:
            data_prop = (target or {}).get("properties", {}).get("data", {})
            for item in data_prop.get("oneOf", []):
                if isinstance(item, dict) and "$ref" in item:
                    ref_key = item["$ref"].split("/")[-1]
                    payload_types.append(event_file_name(ref_key, file_names))

        index_entries.append(
            OrderedDict(
                event=key,
                file=disk_name,
                path=str(out_path.relative_to(ROOT)).replace("\\", "/"),
                status="synced",
                title=(target or {}).get("title", key),
                description=(target or {}).get("description", ""),
                payloadTypes=payload_types,
            )
        )

    flush_references(pending)
    return index_entries


def build_management_events() -> list[dict]:
    return build_schema_exports(
        EVENTS_SRC,
        EVENTS_DIR,
        EVENT_EXPORT_KEYS,
        EVENT_EXPORT_SET,
        EVENT_FILE_NAMES,
        "Missing in Management Events.json",
        envelope_key="async-events",
    )


def build_tag_data_events() -> list[dict]:
    return build_schema_exports(
        TAG_DATA_SRC,
        TAG_EVENTS_DIR,
        TAG_EVENT_EXPORT_KEYS,
        TAG_EVENT_EXPORT_SET,
        TAG_EVENT_FILE_NAMES,
        "Missing in Tag Data Events.json",
        envelope_key="tagDataEvents",
    )


if __name__ == "__main__":
    build()
