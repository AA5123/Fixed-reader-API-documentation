#!/usr/bin/env python3
"""Generate RestAPI/rest_mqtt_map.json and RestAPI/rest_mqtt_map.md from FX90.yaml."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FX90 = ROOT / "RestAPI" / "FX90.yaml"
TAG_CONFIG = ROOT / "tag_config.json"
OUT_JSON = ROOT / "RestAPI" / "mappings" / "rest_mqtt_map.json"
OUT_MD = ROOT / "RestAPI" / "mappings" / "rest_mqtt_map.md"

ALIASES = {
    "localrestlogin": "localrest_login",
    "get_userapps": "get_user_apps",
    "set_installUserapp": "install_user_app",
    "set_uninstallUserapp": "uninstall-user-app",
    "set_startUserapp": "start_user_app",
    "set_stopUserapp": "stop_user_app",
    "set_autostartUserapp": "autostart_user_app",
    "set_reqToUserapp": "set_req_usr_app",
    "get_readerCapabilities": "get_readerCapabilites",
    "get_gpiStatus": "get_gpi_status",
    "get_gpoStatus": "get_gpostatus",
    "get_hostName": "get_hostname",
    "set_hostName": "set_hostname",
    "get_certificates": "get_certs",
    "del_certificate": "del_certs",
    "set_updateCertificate": "set_update_cert",
    "set_refreshCertificate": "refresh-cert",
    "set_revertbackOS": "revertback",
    "get_logs_rcLog": "get_rc_log",
    "get_logs_rgErrorLog": "get_rg_error_logs",
    "get_logs_rgWarningLog": "get_rg_warn_logs",
    "get_logs_radioPacketLog": "get_radio_pkt_logs",
    "del_logs_radioPacketLog": "del_radio_pkt_logs",
    "del_logs_syslog": "del_syslogs",
    "get_SupportedStandardList": "get_SupportedStandardlist",
}

EVENT_TAGS = frozenset({"management-events", "tag-data-events"})


def main() -> None:
    doc = yaml.safe_load(FX90.read_text(encoding="utf-8"))
    tag = json.loads(TAG_CONFIG.read_text(encoding="utf-8"))
    mqtt_ops = tag["operation_tags"]
    mqtt_commands = sorted(mqtt_ops.keys())

    rest_rows = []
    for path, item in sorted(doc["paths"].items()):
        for method, op in sorted(item.items()):
            if not isinstance(op, dict):
                continue
            desc = op.get("description") or ""
            match = re.search(r"MQTT API :-?\s*(\S+)", desc)
            rest_label = match.group(1) if match else ""
            mqtt_cmd = ALIASES.get(rest_label, rest_label)
            rest_rows.append(
                {
                    "restPath": path,
                    "httpMethod": method.upper(),
                    "operationId": op.get("operationId", ""),
                    "openApiTag": (op.get("tags") or [""])[0],
                    "summary": op.get("summary", ""),
                    "restMqttLabel": rest_label,
                    "mqttCommand": mqtt_cmd,
                    "mqttTag": mqtt_ops.get(mqtt_cmd),
                }
            )

    matched_mqtt = {r["mqttCommand"] for r in rest_rows if r["mqttCommand"] in mqtt_ops}
    unmapped_rest = [r for r in rest_rows if r["mqttCommand"] not in mqtt_ops]
    mqtt_only = sorted(set(mqtt_commands) - matched_mqtt)
    mqtt_only_detail = [
        {
            "mqttCommand": cmd,
            "mqttTag": mqtt_ops[cmd],
            "kind": "event" if mqtt_ops[cmd] in EVENT_TAGS else "command",
        }
        for cmd in mqtt_only
    ]

    out = {
        "source": "RestAPI/FX90.yaml",
        "mqttSource": "tag_config.json",
        "stats": {
            "restOperations": len(rest_rows),
            "mqttOperations": len(mqtt_commands),
            "mappedPairs": len(matched_mqtt),
            "restUnmappedLabels": len(unmapped_rest),
            "mqttOnly": len(mqtt_only),
            "mqttOnlyCommands": sum(1 for x in mqtt_only_detail if x["kind"] == "command"),
            "mqttOnlyEvents": sum(1 for x in mqtt_only_detail if x["kind"] == "event"),
        },
        "aliases": [{"restLabel": k, "mqttCommand": v} for k, v in sorted(ALIASES.items())],
        "restToMqtt": rest_rows,
        "mqttOnly": mqtt_only_detail,
        "restUnmapped": unmapped_rest,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    s = out["stats"]
    lines = [
        "# REST ↔ MQTT mapping",
        "",
        "Generated from `RestAPI/FX90.yaml` and `tag_config.json`.",
        "Regenerate: `python scripts/generate_rest_mqtt_map.py`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|--------|------:|",
        f"| REST HTTP operations | {s['restOperations']} |",
        f"| MQTT operations (total) | {s['mqttOperations']} |",
        f"| Matched (REST has MQTT equivalent) | {s['mappedPairs']} |",
        f"| MQTT-only | {s['mqttOnly']} ({s['mqttOnlyCommands']} commands, {s['mqttOnlyEvents']} events) |",
        "",
        "## REST → MQTT (all 70 operations)",
        "",
        "| Tag | Method | REST path | MQTT command | operationId |",
        "|-----|--------|-----------|--------------|-------------|",
    ]
    for r in rest_rows:
        lines.append(
            f"| {r['openApiTag']} | {r['httpMethod']} | `{r['restPath']}` | `{r['mqttCommand']}` | {r['operationId']} |"
        )
    lines.extend(
        [
            "",
            "## MQTT-only (no REST endpoint in FX90.yaml)",
            "",
            "### Commands (5)",
            "",
            "| MQTT command | Category |",
            "|--------------|----------|",
        ]
    )
    for x in sorted(mqtt_only_detail, key=lambda z: (z["kind"], z["mqttTag"], z["mqttCommand"])):
        if x["kind"] == "command":
            lines.append(f"| `{x['mqttCommand']}` | {x['mqttTag']} |")
    lines.extend(
        [
            "",
            "### Events (13)",
            "",
            "| MQTT event | Category |",
            "|------------|----------|",
        ]
    )
    for x in sorted(mqtt_only_detail, key=lambda z: (z["kind"], z["mqttTag"], z["mqttCommand"])):
        if x["kind"] == "event":
            lines.append(f"| `{x['mqttCommand']}` | {x['mqttTag']} |")
    lines.extend(
        [
            "",
            "## REST label aliases",
            "",
            "FX90.yaml `description` uses alternate names; normalized to canonical MQTT commands:",
            "",
            "| REST label in YAML | Canonical MQTT command |",
            "|--------------------|------------------------|",
        ]
    )
    for a, b in sorted(ALIASES.items()):
        lines.append(f"| `{a}` | `{b}` |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Written {OUT_JSON}")
    print(f"Written {OUT_MD}")
    print(json.dumps(s, indent=2))


if __name__ == "__main__":
    main()
