# Zebra Fixed Reader — MQTT API Reference

Schema-first documentation and modular JSON schemas for Zebra **RAW MQTT Payloads** (FX7500, FX9600, ATR7000).

## Folder structure

```
Fixed reader/
├── Command Schemas.json       # Authoritative command schemas (do not auto-edit)
├── Response Schemas.json      # Authoritative response schemas
├── Management Events.json     # Authoritative management event payloads (reader → cloud)
├── Tag Data Events.json       # Authoritative RFID tag read event payloads
├── schemas/                   # Generated schema tree (regenerated on build)
│   ├── commands/{category}/   # Per-command request schemas (*.json)
│   ├── response/{category}/   # Per-command response schemas (*_response.json)
│   ├── events/                # Management event schemas (flat, one file per type)
│   ├── tag-events/            # Tag data event schemas (flat, one file per type)
│   ├── references/            # Shared $ref targets — YAML, bucketed by source:
│   │   ├── request_payload/   #   only Command Schemas.json
│   │   ├── response_payload/  #   only Response Schemas.json
│   │   ├── events_payload/    #   only Management Events.json
│   │   ├── tag_payload/       #   only Tag Data Events.json
│   │   └── shared/            #   reached from two or more sources
│   └── example_description.json  # Hand-maintained (NOT regenerated)
├── docs/
│   ├── index.html             # Interactive API reference (browser)
│   ├── js/viewer-app.js
│   ├── css/custom-api.css
│   └── openapi_md.json        # Generated spec (inlined, no $ref)
├── tag_config.json            # Tag groups + operation → category mapping
├── tag_descriptions/          # Per-category markdown (sidebar + tag intro)
├── operation_descriptions/    # Per-command markdown overrides
├── info_description.md        # API overview on the docs home page
├── error_codes.json
└── scripts/
    ├── build_mqtt_schema_tree.py
    ├── generate_openapi_tags_md.py
    ├── group_master_command_list.py  # Category list (imported by build)
    └── validate_refs.py
```

## Workflow

### 1. Rebuild schema tree (after editing source JSON)

Rebuilds commands, responses, **management events**, **tag data events**, and shared references from the four Zebra source files. The script first deletes the generated subfolders (`commands/`, `response/`, `events/`, `tag-events/`, `references/`) so stale files never linger, then regenerates them:

```powershell
python scripts/build_mqtt_schema_tree.py
python scripts/validate_refs.py
```

> The command/response/event schema tree is **JSON**; only the shared `schemas/references/` fragments are **YAML**. Config files such as `tag_config.json` stay JSON, and `schemas/example_description.json` is hand-maintained (never deleted or overwritten).

Shared `$ref` targets are written to `schemas/references/<bucket>/` (as `.yaml`) where the bucket is the source document that introduces the fragment (`request_payload`, `response_payload`, `events_payload`, `tag_payload`); fragments reached from two or more sources go to `shared/`. The build prints a per-bucket count.

Event output in `schemas/events/`:

| File | Role |
|------|------|
| `async-events.json` | Envelope (`type`, `timestamp`, `component`, `eventNum`, `data`) |
| `heartbeat.json` | Periodic health snapshot |
| `firmwareUpdateProgress.json` | Firmware update status |
| `gpi.json` / `gpo.json` | GPIO pin events |
| `error.json` / `warning.json` | Diagnostic messages |
| `userapp_event.json` | User-application async events |

### 2. Regenerate documentation spec

```powershell
python scripts/generate_openapi_tags_md.py
```

Output: [`docs/openapi_md.json`](docs/openapi_md.json) — 88 MQTT operations, 17 categories, OpenAPI 3.0 (paths are doc aliases, not HTTP).

Optional root link for editors:

```powershell
# If openapi.json is missing, link to generated spec (Windows)
cmd /c mklink openapi.json docs\openapi_md.json
```

### 3. View in browser

```powershell
cd docs
python -m http.server 8080
```

Open [http://127.0.0.1:8080/index.html](http://127.0.0.1:8080/index.html).

Hard-refresh after JS/CSS changes (`Ctrl+F5`). Cache-bust query strings are on `viewer-app.js` and `custom-api.css` in `index.html`.

## Customize content

| File | Purpose |
|------|---------|
| [`tag_config.json`](tag_config.json) | Category tags, groups, operation order |
| [`tag_descriptions/<category>.md`](tag_descriptions/) | Category intro (e.g. `system.md`, `app-led.md`) |
| [`operation_descriptions/<command>.md`](operation_descriptions/) | Per-command description override |
| [`info_description.md`](info_description.md) | Top-of-page overview and details table |
| [`error_codes.json`](error_codes.json) | `x-error-codes` tables in the viewer |

After editing markdown or config, rerun `generate_openapi_tags_md.py`.

## Categories (17)

`login`, `system`, `network`, `control`, `region`, `gpio`, `app-led`, `stack-led`, `logs`, `date-time`, `certificate`, `firmware`, `userapp`, `impinjgen2x`, `ble`, `management-events`, `tag-data-events`

## Validation

```powershell
python scripts/validate_refs.py
python scripts/generate_openapi_tags_md.py --validate-only
```

## Source of truth

Authoritative payloads: the four root `*.json` files. Human-written docs: `tag_descriptions/`, `operation_descriptions/`, and `info_description.md`. The interactive viewer reads only `docs/openapi_md.json` (regenerated from the schema tree and markdown).
