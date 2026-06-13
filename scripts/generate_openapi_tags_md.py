#!/usr/bin/env python3
"""
generate_openapi_tags_md.py
---------------------------
Builds docs/openapi_md.json from schemas/* with markdown-first descriptions.
Usage:
   python scripts/generate_openapi_tags_md.py
"""
import importlib
import json
import os
from collections import OrderedDict

import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SCHEMAS_DIR = os.path.join(PROJECT_ROOT, "schemas")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "docs", "openapi_md.json")
COMMANDS_DIR = os.path.join(SCHEMAS_DIR, "commands")
RESPONSE_DIR = os.path.join(SCHEMAS_DIR, "response")
EVENTS_DIR = os.path.join(SCHEMAS_DIR, "events")
TAG_EVENTS_DIR = os.path.join(SCHEMAS_DIR, "tag-events")
TAG_CONFIG_PATH = os.path.join(PROJECT_ROOT, "tag_config.json")
ERROR_CODES_PATH = os.path.join(PROJECT_ROOT, "error_codes.json")
OP_DESCRIPTIONS_DIR = os.path.join(PROJECT_ROOT, "operation_descriptions")
EXAMPLE_DESC_PATH = os.path.join(SCHEMAS_DIR, "example_description.json")
TAG_DESCRIPTIONS_DIR = os.path.join(PROJECT_ROOT, "tag_descriptions")
INFO_DESCRIPTION_PATH = os.path.join(PROJECT_ROOT, "info_description.md")
SKIP_FILES = set()
SCHEMA_EXTS = (".yaml", ".yml", ".json")
RESPONSE_CODE_MARKER = "Response codes:"


def is_schema_file(filename):
    return (
        os.path.splitext(filename)[1].lower() in SCHEMA_EXTS
        and filename not in SKIP_FILES
    )


def op_name_of(filename):
    return os.path.splitext(filename)[0]
UNSUPPORTED_DETAIL_ROWS = {
    "communication type",
    "supported response sections",
    "supported api versions",
}


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8-sig") as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def load_structured_file(filepath):
    _, ext = os.path.splitext(filepath)
    with open(filepath, "r", encoding="utf-8-sig") as f:
        if ext.lower() == ".json":
            return json.load(f, object_pairs_hook=OrderedDict)
        if ext.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(f)
    raise ValueError(f"Unsupported schema file type: {filepath}")


def load_tag_config():
    if os.path.exists(TAG_CONFIG_PATH):
        return load_json(TAG_CONFIG_PATH)
    print(f"  WARNING: {TAG_CONFIG_PATH} not found, using empty config")
    return {"tag_groups": {}, "tag_descriptions": {}}


def load_operation_descriptions():
    descriptions = {}
    if os.path.isdir(OP_DESCRIPTIONS_DIR):
        for filename in os.listdir(OP_DESCRIPTIONS_DIR):
            if filename.endswith(".md"):
                op_name = filename[:-3]
                filepath = os.path.join(OP_DESCRIPTIONS_DIR, filename)
                with open(filepath, "r", encoding="utf-8-sig") as f:
                    descriptions[op_name] = f.read().strip()
    return descriptions


def load_error_codes():
    if not os.path.exists(ERROR_CODES_PATH):
        print(f"  WARNING: {ERROR_CODES_PATH} not found, skipping error codes")
        return {}
    all_codes = load_json(ERROR_CODES_PATH).get("codes", [])
    cmd_map = {}
    for entry in all_codes:
        for cmd in entry.get("commands", []):
            if cmd == "*":
                continue
            cmd_map.setdefault(cmd, []).append(entry)
    code_zero = [e for e in all_codes if e.get("code") == 0]
    for cmd in cmd_map:
        cmd_map[cmd] = code_zero + cmd_map[cmd]
    return cmd_map


def load_example_descriptions():
    if os.path.exists(EXAMPLE_DESC_PATH):
        return load_json(EXAMPLE_DESC_PATH)
    return {}


def load_info_description():
    if os.path.isfile(INFO_DESCRIPTION_PATH):
        with open(INFO_DESCRIPTION_PATH, "r", encoding="utf-8-sig") as f:
            text = f.read().strip()
        print("  Loaded info description from info_description.md")
        return text
    return (
        "# Zebra Fixed Reader — RAW MQTT Payloads &nbsp; v1.0.0\n\n"
        "MQTT-based API for controlling Zebra fixed RFID readers "
        "(FX7500, FX9600, ATR7000)."
    )


def load_tag_descriptions_from_md():
    descriptions = {}
    if not os.path.isdir(TAG_DESCRIPTIONS_DIR):
        print(f"  WARNING: {TAG_DESCRIPTIONS_DIR} not found")
        return descriptions
    for filename in sorted(os.listdir(TAG_DESCRIPTIONS_DIR)):
        if filename.endswith(".md"):
            tag_name = os.path.splitext(filename)[0]
            filepath = os.path.join(TAG_DESCRIPTIONS_DIR, filename)
            with open(filepath, "r", encoding="utf-8-sig") as f:
                descriptions[tag_name] = f.read().strip()
            print(f"  Loaded tag description: '{tag_name}' from {filename}")
    return descriptions


def sanitize_operation_description(description):
    """Remove unsupported command detail rows from markdown tables."""
    if not description:
        return description

    cleaned_lines = []
    for line in description.splitlines():
        stripped = line.strip()
        if stripped.startswith("|"):
            parts = [p.strip().lower() for p in stripped.split("|") if p.strip()]
            if parts and parts[0] in UNSUPPORTED_DETAIL_ROWS:
                continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def discover_operations(operation_tags=None):
    if operation_tags is None:
        operation_tags = {}
    operations = []
    if os.path.isdir(COMMANDS_DIR):
        for subfolder in sorted(os.listdir(COMMANDS_DIR)):
            subfolder_path = os.path.join(COMMANDS_DIR, subfolder)
            if not os.path.isdir(subfolder_path):
                continue
            for filename in sorted(os.listdir(subfolder_path)):
                if not is_schema_file(filename):
                    continue
                filepath = os.path.join(subfolder_path, filename)
                op_name = op_name_of(filename)
                tag = operation_tags.get(op_name)
                if not tag:
                    continue
                operations.append((op_name, tag, subfolder, filepath))
    if os.path.isdir(EVENTS_DIR):
        for filename in sorted(os.listdir(EVENTS_DIR)):
            if not is_schema_file(filename):
                continue
            filepath = os.path.join(EVENTS_DIR, filename)
            op_name = op_name_of(filename)
            tag = operation_tags.get(op_name)
            if not tag:
                print(
                    f"  WARNING: '{op_name}' has no entry in operation_tags "
                    f"(tag_config.json), skipping"
                )
                continue
            operations.append((op_name, tag, "events", filepath))
    if os.path.isdir(TAG_EVENTS_DIR):
        for filename in sorted(os.listdir(TAG_EVENTS_DIR)):
            if not is_schema_file(filename):
                continue
            filepath = os.path.join(TAG_EVENTS_DIR, filename)
            op_name = op_name_of(filename)
            tag = operation_tags.get(op_name)
            if not tag:
                print(
                    f"  WARNING: '{op_name}' has no entry in operation_tags "
                    f"(tag_config.json), skipping"
                )
                continue
            operations.append((op_name, tag, "tag-events", filepath))
    return operations


def get_response_path(operation, source):
    """Resolve the response schema path for an operation.

    Response files follow the Zebra convention ``<command>_response.json`` and
    live under ``schemas/response/<category>/``. For backwards compatibility a
    plain ``<command>.json`` file is accepted as a fallback.
    """
    if source in ("events", "tag-events"):
        return None
    candidates = []
    for ext in SCHEMA_EXTS:
        candidates.append(os.path.join(RESPONSE_DIR, source, f"{operation}_response{ext}"))
        candidates.append(os.path.join(RESPONSE_DIR, source, f"{operation}{ext}"))
    for path in candidates:
        if os.path.exists(path):
            return path
    # Return the conventional path so callers can report it as "missing".
    return candidates[0]


def extract_examples(schema, title, example_data):
    if "examples" not in schema:
        return {}
    examples = schema["examples"]
    if not isinstance(examples, list) or not examples:
        return {}
    result = OrderedDict()
    descriptions = example_data.get(title, {})
    desc_keys = list(descriptions.keys()) if descriptions else []
    for idx, example in enumerate(examples):
        if idx < len(desc_keys):
            label = desc_keys[idx]
            desc = descriptions[label]
        else:
            label = f"example{idx + 1}"
            desc = None
        entry = OrderedDict()
        if desc:
            entry["description"] = desc
        entry["value"] = example
        result[label] = entry
    return result


def replace_const_with_enum(obj):
    """Recursively replace 'const': value with 'enum': [value] in dicts/lists."""
    if isinstance(obj, dict):
        obj = OrderedDict(obj)
        if "const" in obj:
            obj["enum"] = [obj.pop("const")]
        for k, v in obj.items():
            obj[k] = replace_const_with_enum(v)
        return obj
    elif isinstance(obj, list):
        return [replace_const_with_enum(i) for i in obj]
    else:
        return obj


def normalize_for_oas30(obj):
    """Down-convert JSON-Schema / OpenAPI-3.1 constructs to OpenAPI 3.0.

    - ``type: [..]`` arrays -> single ``type`` (+ ``nullable: true`` when the
      array contains "null"); multi-type arrays drop ``type`` (3.0 cannot
      express them) but keep ``nullable`` when applicable.
    - numeric ``exclusiveMinimum``/``exclusiveMaximum`` (draft 2020 style) ->
      the 3.0 boolean form paired with ``minimum``/``maximum``.
    """
    if isinstance(obj, dict):
        obj = OrderedDict(obj)

        type_val = obj.get("type")
        if isinstance(type_val, list):
            non_null = [t for t in type_val if t != "null"]
            has_null = "null" in type_val
            if len(non_null) == 1:
                obj["type"] = non_null[0]
            else:
                obj.pop("type", None)
            if has_null:
                obj["nullable"] = True

        enum_val = obj.get("enum")
        if isinstance(enum_val, list):
            deduped = []
            seen = []
            for item in enum_val:
                if item not in seen:
                    seen.append(item)
                    deduped.append(item)
            obj["enum"] = deduped

        for bound, limit in (("exclusiveMinimum", "minimum"),
                             ("exclusiveMaximum", "maximum")):
            val = obj.get(bound)
            if isinstance(val, bool):
                continue
            if isinstance(val, (int, float)):
                obj.setdefault(limit, val)
                obj[bound] = True

        for k, v in obj.items():
            obj[k] = normalize_for_oas30(v)
        return obj
    if isinstance(obj, list):
        return [normalize_for_oas30(i) for i in obj]
    return obj


def remove_examples(obj):
    """Recursively remove 'examples' keys from dicts/lists."""
    if isinstance(obj, dict):
        obj = OrderedDict((k, v) for k, v in obj.items() if k != "examples")
        for k, v in obj.items():
            obj[k] = remove_examples(v)
        return obj
    elif isinstance(obj, list):
        return [remove_examples(i) for i in obj]
    else:
        return obj


def resolve_refs(obj, base_dir, seen=None):
    if seen is None:
        seen = set()
    if isinstance(obj, dict):
        ref = obj.get("$ref")
        if ref:
            ref_path = os.path.normpath(os.path.join(base_dir, ref))
            if ref_path in seen:
                return OrderedDict([("description", f"Circular reference: {ref}")])
            if not os.path.exists(ref_path):
                raise FileNotFoundError(
                    f"Broken $ref '{ref}' -> '{ref_path}' (not found)"
                )
            resolved = load_structured_file(ref_path)
            merged = resolve_refs(resolved, os.path.dirname(ref_path), seen | {ref_path})
            sibling_keys = OrderedDict((k, v) for k, v in obj.items() if k != "$ref")
            if sibling_keys and isinstance(merged, dict):
                merged = OrderedDict(merged)
                for key, value in sibling_keys.items():
                    merged[key] = resolve_refs(value, base_dir, seen | {ref_path})
            return merged
        resolved_obj = OrderedDict()
        for key, value in obj.items():
            resolved_obj[key] = resolve_refs(value, base_dir, seen)
        return resolved_obj
    if isinstance(obj, list):
        return [resolve_refs(item, base_dir, seen) for item in obj]
    return obj


def extract_schema(raw_schema, source_path):
    skip_keys = {"title", "x-stoplight", "x-tag", "examples", "description"}
    schema = OrderedDict()
    for key, value in raw_schema.items():
        if key not in skip_keys:
            schema[key] = value
    if "type" not in schema:
        schema["type"] = "object"
    schema = replace_const_with_enum(schema)
    schema = resolve_refs(schema, os.path.dirname(source_path))
    schema = remove_examples(schema)
    schema = normalize_for_oas30(schema)
    return schema


def strip_inline_response_code_tables(obj):
    """Remove huge baked-in 'Response codes:' markdown tables from schema code fields."""
    if isinstance(obj, dict):
        code_node = obj.get("code")
        if isinstance(code_node, dict):
            desc = code_node.get("description")
            if isinstance(desc, str) and RESPONSE_CODE_MARKER in desc:
                code_node["description"] = (
                    "Command response status code. See x-error-codes for code meanings."
                )

        for key, value in obj.items():
            obj[key] = strip_inline_response_code_tables(value)
        return obj

    if isinstance(obj, list):
        return [strip_inline_response_code_tables(i) for i in obj]

    return obj


def enrich_response_code_description(schema_obj, error_codes_for_cmd):
    """Inject concise command-specific response code help into response.code."""
    if not error_codes_for_cmd or not isinstance(schema_obj, dict):
        return schema_obj

    code_entries = []
    for entry in error_codes_for_cmd:
        code_val = entry.get("code")
        desc_val = entry.get("description")
        if isinstance(code_val, int) and isinstance(desc_val, str) and desc_val.strip():
            code_entries.append((code_val, desc_val.strip()))

    if not code_entries:
        return schema_obj

    seen_codes = set()
    ordered_codes = []
    for code_val, desc_val in sorted(code_entries, key=lambda item: item[0]):
        if code_val in seen_codes:
            continue
        seen_codes.add(code_val)
        ordered_codes.append((code_val, desc_val))

    def walk(node):
        if isinstance(node, dict):
            properties = node.get("properties")
            if isinstance(properties, dict):
                code_node = properties.get("code")
                if isinstance(code_node, dict) and code_node.get("type") in {
                    "integer",
                    "number",
                }:
                    bullets = "\n".join(
                        [f"- {code_val} — {desc_val}" for code_val, desc_val in ordered_codes]
                    )
                    code_node["description"] = (
                        "Response code indicating success or failure.\n\n" + bullets
                    )
                    code_values = [code_val for code_val, _ in ordered_codes]
                    code_node["minimum"] = min(code_values)
                    code_node["maximum"] = max(code_values)

            for key, value in list(node.items()):
                node[key] = walk(value)
            return node

        if isinstance(node, list):
            return [walk(item) for item in node]

        return node

    return walk(schema_obj)


def sort_operations(operations, tag_config):
    tag_groups = tag_config.get("tag_groups", {})
    op_order = tag_config.get("operation_order", {})
    tag_order = {}
    for group_index, (_, tags) in enumerate(tag_groups.items()):
        for tag_index, tag_name in enumerate(tags):
            tag_order[tag_name] = (group_index, tag_index)

    def key_fn(op_tuple):
        op_name, tag, _, _ = op_tuple
        order = tag_order.get(tag, (999, 999))
        if tag in op_order:
            try:
                op_index = op_order[tag].index(op_name)
            except ValueError:
                op_index = 999
            return (order[0], order[1], op_index)
        return (order[0], order[1], op_name)

    return sorted(operations, key=key_fn)


def iter_schema_files():
    """Yield (kind, op_name, source, path) for every schema JSON on disk.

    kind is one of 'command', 'response', 'event'. source is the category
    subfolder (or 'events').
    """
    if os.path.isdir(COMMANDS_DIR):
        for sub in sorted(os.listdir(COMMANDS_DIR)):
            sub_path = os.path.join(COMMANDS_DIR, sub)
            if not os.path.isdir(sub_path):
                continue
            for fn in sorted(os.listdir(sub_path)):
                if is_schema_file(fn):
                    yield "command", op_name_of(fn), sub, os.path.join(sub_path, fn)
    if os.path.isdir(RESPONSE_DIR):
        for sub in sorted(os.listdir(RESPONSE_DIR)):
            sub_path = os.path.join(RESPONSE_DIR, sub)
            if not os.path.isdir(sub_path):
                continue
            for fn in sorted(os.listdir(sub_path)):
                if is_schema_file(fn):
                    yield "response", op_name_of(fn), sub, os.path.join(sub_path, fn)
    if os.path.isdir(EVENTS_DIR):
        for fn in sorted(os.listdir(EVENTS_DIR)):
            if is_schema_file(fn):
                yield "event", op_name_of(fn), "events", os.path.join(EVENTS_DIR, fn)
    if os.path.isdir(TAG_EVENTS_DIR):
        for fn in sorted(os.listdir(TAG_EVENTS_DIR)):
            if is_schema_file(fn):
                yield "event", op_name_of(fn), "tag-events", os.path.join(TAG_EVENTS_DIR, fn)


def _collect_broken_refs(path, errors):
    """Parse a schema file and verify every $ref target exists on disk.

    Returns the parsed document (or None on parse failure). Appends issues to
    the shared `errors` dict in place.
    """
    try:
        doc = load_structured_file(path)
    except Exception as exc:
        errors["invalid_files"].append(f"{rel(path)}: {exc}")
        return None

    base_dir = os.path.dirname(path)
    stack = [doc]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            ref = node.get("$ref")
            if isinstance(ref, str) and not ref.startswith("#"):
                target = os.path.normpath(os.path.join(base_dir, ref))
                if not os.path.exists(target):
                    errors["broken_refs"].append(f"{rel(path)} -> {ref}")
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
    return doc


def rel(path):
    try:
        return os.path.relpath(path, PROJECT_ROOT)
    except ValueError:
        return path


def validate_project(operation_tags):
    """Run static checks over the schema tree and config.

    Returns a dict with keys: missing_tag_mappings, missing_command_files,
    missing_response_files, broken_refs, invalid_files.
    """
    errors = {
        "missing_tag_mappings": [],
        "missing_command_files": [],
        "missing_response_files": [],
        "broken_refs": [],
        "invalid_files": [],
    }

    command_ops = {}  # op_name -> (source, path)
    event_ops = set()
    for kind, op_name, source, path in iter_schema_files():
        _collect_broken_refs(path, errors)
        if kind == "command":
            command_ops[op_name] = (source, path)
            if op_name not in operation_tags:
                errors["missing_tag_mappings"].append(f"command '{op_name}' ({rel(path)})")
        elif kind == "event":
            event_ops.add(op_name)
            if op_name not in operation_tags:
                errors["missing_tag_mappings"].append(f"event '{op_name}' ({rel(path)})")

    # operation_tags entries that have no command/event file on disk.
    for op_name in operation_tags:
        if op_name not in command_ops and op_name not in event_ops:
            errors["missing_command_files"].append(
                f"operation_tags maps '{op_name}' but no schema file exists"
            )

    # commands without a matching response file.
    for op_name, (source, _) in sorted(command_ops.items()):
        if op_name not in operation_tags:
            continue
        resp_path = get_response_path(op_name, source)
        if not resp_path or not os.path.exists(resp_path):
            errors["missing_response_files"].append(
                f"'{op_name}' -> expected {rel(resp_path)}"
            )

    return errors


def print_validation_report(errors):
    labels = {
        "invalid_files": "Invalid JSON/YAML files",
        "broken_refs": "Broken $ref references",
        "missing_tag_mappings": "Schema files without a tag mapping",
        "missing_command_files": "Tag mappings without a schema file",
        "missing_response_files": "Commands without a response file",
    }
    total = sum(len(v) for v in errors.values())
    print("\n=== Validation report ===")
    for key, label in labels.items():
        items = errors.get(key, [])
        print(f"  {label}: {len(items)}")
        for item in items:
            print(f"      - {item}")
    print(f"  TOTAL issues: {total}\n")
    return total


def validate_openapi_document(openapi):
    """Validate the generated document against the OpenAPI 3.0 schema.

    Returns (ok, message). Gracefully degrades if the validator package is
    not installed.
    """
    try:
        _validate = importlib.import_module("openapi_spec_validator").validate
    except Exception:
        return None, "openapi-spec-validator not installed; skipped compliance check"
    try:
        plain = json.loads(json.dumps(openapi))
        _validate(plain)
        return True, "OpenAPI 3.0 document is valid"
    except Exception as exc:
        first_line = str(exc).splitlines()[0]
        return False, f"OpenAPI validation failed: {first_line}"


def build_openapi():
    tag_config = load_tag_config()
    op_descriptions = load_operation_descriptions()
    example_data = load_example_descriptions()
    error_codes_map = load_error_codes()
    tag_groups = tag_config.get("tag_groups", {})
    tag_descriptions = load_tag_descriptions_from_md()
    operation_tags = tag_config.get("operation_tags", {})
    operations = discover_operations(operation_tags)
    operations = sort_operations(operations, tag_config)
    print(f"  Discovered {len(operations)} operations")
    used_tags = OrderedDict()
    for _, tag, _, _ in operations:
        if tag not in used_tags:
            used_tags[tag] = True
    openapi = OrderedDict()
    openapi["openapi"] = "3.0.0"
    openapi["info"] = OrderedDict(
        [
            ("title", "Zebra Fixed Reader MQTT API"),
            ("version", "1.0.0"),
            ("description", load_info_description()),
        ]
    )
    tags = []
    all_tag_names = set()
    for group_tags in tag_groups.values():
        for tag_name in group_tags:
            if tag_name in all_tag_names:
                continue
            all_tag_names.add(tag_name)
            tag_entry = OrderedDict()
            tag_entry["name"] = tag_name
            if tag_name in tag_descriptions:
                tag_entry["description"] = tag_descriptions[tag_name]
            tags.append(tag_entry)
    for tag_name in used_tags:
        if tag_name in all_tag_names:
            continue
        all_tag_names.add(tag_name)
        tags.append(OrderedDict([("name", tag_name)]))
        print(f"  NEW TAG discovered: '{tag_name}' (not in tag_config.json)")
    openapi["tags"] = tags
    x_tag_groups = []
    for group_name, group_tags in tag_groups.items():
        x_tag_groups.append(
            OrderedDict(
                [
                    ("name", group_name),
                    ("tags", list(group_tags)),
                ]
            )
        )
    all_grouped_tags = set()
    for group_tags in tag_groups.values():
        all_grouped_tags.update(group_tags)
    uncategorized = [tag for tag in used_tags if tag not in all_grouped_tags]
    if uncategorized:
        x_tag_groups.append(
            OrderedDict(
                [
                    ("name", "Other"),
                    ("tags", uncategorized),
                ]
            )
        )
        print(f"  NEW GROUP 'Other' created for tags: {uncategorized}")
    openapi["x-tagGroups"] = x_tag_groups
    openapi["x-operationOrder"] = tag_config.get("operation_order", {})
    paths = OrderedDict()
    skipped = []
    for op_name, tag_name, source, req_path in operations:
        error_codes_for_cmd = error_codes_map.get(op_name, [])
        try:
            req_schema = load_structured_file(req_path)
        except Exception as exc:
            skipped.append(f"  SKIP {op_name}: error reading {req_path}: {exc}")
            continue
        title = req_schema.get("title", op_name)
        description = op_descriptions.get(op_name) or req_schema.get("description", None)
        description = sanitize_operation_description(description)
        op = OrderedDict()
        op["tags"] = [tag_name]
        op["summary"] = op_name.replace("_", " ").title()
        if description:
            op["description"] = description
        if source in ("events", "tag-events"):
            evt_examples = extract_examples(req_schema, title, example_data)
            evt_schema_clean = extract_schema(req_schema, req_path)
            evt_content = OrderedDict()
            evt_content["application/json"] = OrderedDict()
            evt_content["application/json"]["schema"] = evt_schema_clean
            if evt_examples:
                evt_content["application/json"]["examples"] = evt_examples
            op["responses"] = OrderedDict(
                [
                    (
                        "default",
                        OrderedDict(
                            [
                                ("description", f"{op_name} event payload"),
                                ("content", evt_content),
                            ]
                        ),
                    )
                ]
            )
        else:
            req_examples = extract_examples(req_schema, title, example_data)
            req_schema_clean = extract_schema(req_schema, req_path)
            req_content = OrderedDict()
            req_content["application/json"] = OrderedDict()
            req_content["application/json"]["schema"] = req_schema_clean
            if req_examples:
                req_content["application/json"]["examples"] = req_examples
            op["requestBody"] = OrderedDict(
                [
                    ("required", True),
                    ("content", req_content),
                ]
            )
            resp_path = get_response_path(op_name, source)
            if resp_path and os.path.exists(resp_path):
                try:
                    resp_schema = load_structured_file(resp_path)
                    resp_title = resp_schema.get("title", op_name)
                    resp_examples = extract_examples(resp_schema, resp_title, example_data)
                    resp_schema_clean = extract_schema(resp_schema, resp_path)
                    resp_schema_clean = strip_inline_response_code_tables(resp_schema_clean)
                    resp_schema_clean = enrich_response_code_description(
                        resp_schema_clean, error_codes_for_cmd
                    )
                    resp_content = OrderedDict()
                    resp_content["application/json"] = OrderedDict()
                    resp_content["application/json"]["schema"] = resp_schema_clean
                    if resp_examples:
                        resp_content["application/json"]["examples"] = resp_examples
                    op["responses"] = OrderedDict(
                        [
                            (
                                "default",
                                OrderedDict(
                                    [
                                        ("description", f"{op_name} response"),
                                        ("content", resp_content),
                                    ]
                                ),
                            )
                        ]
                    )
                except Exception as exc:
                    skipped.append(
                        f"  WARN {op_name}: failed to build response from "
                        f"{resp_path}: {exc}; using generic 200 response"
                    )
                    op["responses"] = OrderedDict(
                        [("200", OrderedDict([("description", "Success")]))]
                    )
            else:
                skipped.append(
                    f"  WARN {op_name}: no response schema found at "
                    f"{resp_path}; using generic 200 response"
                )
                op["responses"] = OrderedDict(
                    [("200", OrderedDict([("description", "Success")]))]
                )
        if error_codes_for_cmd:
            op["x-error-codes"] = [
                OrderedDict(
                    [
                        ("code", e["code"]),
                        ("description", e["description"]),
                        ("iot_status_code", e["iot_status_code"]),
                        ("cause", e.get("cause", "")),
                        ("recommended_action", e.get("recommended_action", "")),
                    ]
                )
                for e in error_codes_for_cmd
            ]
        paths[f"/{op_name}"] = OrderedDict([("post", op)])
    openapi["paths"] = paths
    return openapi, skipped


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate docs/openapi_md.json from the schema tree."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with a non-zero status if validation finds any issue.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Run validation and exit without writing the output file.",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip the pre-flight validation pass.",
    )
    args = parser.parse_args()

    tag_config = load_tag_config()
    operation_tags = tag_config.get("operation_tags", {})

    issue_total = 0
    if not args.no_validate:
        print("Validating schema tree ...")
        errors = validate_project(operation_tags)
        issue_total = print_validation_report(errors)
        if args.validate_only:
            return 1 if (args.strict and issue_total) else 0
        if args.strict and issue_total:
            print("Strict mode: aborting due to validation issues.")
            return 1

    print("Generating OpenAPI spec (with tag descriptions from markdown) ...")
    openapi, skipped = build_openapi()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(openapi, f, indent=4, ensure_ascii=False)
    group_count = len(openapi.get("x-tagGroups", []))
    tag_count = len(openapi.get("tags", []))
    path_count = len(openapi.get("paths", {}))
    print(f"  {group_count} tag groups, {tag_count} tags, {path_count} endpoints")
    if skipped:
        for warning in skipped:
            print(warning)
    print(f"  Written to {OUTPUT_PATH}")

    ok, message = validate_openapi_document(openapi)
    prefix = {True: "  OK: ", False: "  ERROR: ", None: "  NOTE: "}[ok]
    print(prefix + message)

    print("\nDone!")
    if args.strict and (issue_total or ok is False):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
