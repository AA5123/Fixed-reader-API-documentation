#!/usr/bin/env python3
"""
group_master_command_list.py
----------------------------
Reads:
  - Command Schemas.json
  - Response Schemas.json
Writes:
  - docs/master_command_list_grouped.md

This script groups the "Master Command List by Category" provided by the user
and checks whether each Schema List Name exists in each JSON's
components.schemas keys.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CMD_SCHEMAS_JSON = ROOT / "Command Schemas.json"
RESP_SCHEMAS_JSON = ROOT / "Response Schemas.json"
OUT_MD = ROOT / "docs" / "master_command_list_grouped.md"


MASTER_ITEMS: list[dict] = [
    # Login
    {
        "category": "Login",
        "no": 52,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "localrest_login",
        "method": "GET",
        "path": "/cloud/localRestLogin",
        "desc": "Reader Login",
    },
    # App-led
    {
        "category": "App-led",
        "no": 20,
        "status": "Synced",
        "schema": "get_appled",
        "api": "get_appled",
        "method": "GET",
        "path": "/cloud/app-led",
        "desc": "Retrieves application LED state",
    },
    {
        "category": "App-led",
        "no": 21,
        "status": "Synced",
        "schema": "set_appled",
        "api": "set_appled",
        "method": "PUT",
        "path": "/cloud/app-led",
        "desc": "Updates application LED state",
    },
    # Stack-led
    {
        "category": "Stack-led",
        "no": 53,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "get_stackled",
        "method": "GET",
        "path": "/cloud/stack-led",
        "desc": "Retrieves stack LED state",
    },
    {
        "category": "Stack-led",
        "no": 54,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "set_stackled",
        "method": "PUT",
        "path": "/cloud/stack-led",
        "desc": "Updates stack LED state",
    },
    # Gpio
    {
        "category": "Gpio",
        "no": 22,
        "status": "Synced",
        "schema": "get_gpostatus",
        "api": "get_gpoStatus",
        "method": "GET",
        "path": "/cloud/gpo",
        "desc": "Retrieves the GPO status",
    },
    {
        "category": "Gpio",
        "no": 23,
        "status": "Synced",
        "schema": "set_gpo",
        "api": "set_gpo",
        "method": "PUT",
        "path": "/cloud/gpo",
        "desc": "Updates GPO port state",
    },
    {
        "category": "Gpio",
        "no": 24,
        "status": "Synced",
        "schema": "get_gpi_status",
        "api": "get_gpiStatus",
        "method": "GET",
        "path": "/cloud/gpi",
        "desc": "Get GPI Status",
    },
    # Region
    {
        "category": "Region",
        "no": 25,
        "status": "Synced",
        "schema": "get_region",
        "api": "get_region",
        "method": "GET",
        "path": "/cloud/region",
        "desc": "Retrieves reader region information",
    },
    {
        "category": "Region",
        "no": 26,
        "status": "Synced",
        "schema": "get_SupportedRegionList",
        "api": "get_SupportedRegionList",
        "method": "GET",
        "path": "/cloud/supportedRegionList",
        "desc": "Retrieves the supported region list",
    },
    {
        "category": "Region",
        "no": 27,
        "status": "Synced",
        "schema": "get_SupportedStandardlist",
        "api": "get_SupportedStandardList",
        "method": "GET",
        "path": "/cloud/supportedStandardList",
        "desc": "Retrieves the standard channels",
    },
    {
        "category": "Region",
        "no": 55,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "set_region",
        "method": "PUT",
        "path": "/cloud/region",
        "desc": "Update region information",
    },
    # Control
    {
        "category": "Control",
        "no": 4,
        "status": "Synced",
        "schema": "get_mode",
        "api": "get_mode",
        "method": "GET",
        "path": "/cloud/mode",
        "desc": "Retrieves the operating mode",
    },
    {
        "category": "Control",
        "no": 5,
        "status": "Synced",
        "schema": "set_mode",
        "api": "set_mode",
        "method": "PUT",
        "path": "/cloud/mode",
        "desc": "Updates the reader's operating mode",
    },
    {
        "category": "Control",
        "no": 28,
        "status": "Synced",
        "schema": "start",
        "api": "start",
        "method": "PUT",
        "path": "/cloud/start",
        "desc": "Start RFID Inventory or BLE scan",
    },
    {
        "category": "Control",
        "no": 29,
        "status": "Synced",
        "schema": "stop",
        "api": "stop",
        "method": "PUT",
        "path": "/cloud/stop",
        "desc": "Stop RFID Inventory or BLE scan",
    },
    {
        "category": "Control",
        "no": 57,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "get_preSelection",
        "method": "GET",
        "path": "/cloud/preSelection",
        "desc": "Returns rxSawFilter status",
    },
    {
        "category": "Control",
        "no": 58,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "set_preSelection",
        "method": "PUT",
        "path": "/cloud/preSelection",
        "desc": "Enables or disables the rxSawFilter",
    },
    # System
    {
        "category": "System",
        "no": 1,
        "status": "Synced",
        "schema": "get_version",
        "api": "get_version",
        "method": "GET",
        "path": "/cloud/version",
        "desc": "Retrieves reader component version",
    },
    {
        "category": "System",
        "no": 2,
        "status": "Synced",
        "schema": "get_status",
        "api": "get_status",
        "method": "GET",
        "path": "/cloud/status",
        "desc": "Retrieves reader operational statistics",
    },
    {
        "category": "System",
        "no": 3,
        "status": "Synced",
        "schema": "reboot",
        "api": "reboot",
        "method": "PUT",
        "path": "/cloud/reboot",
        "desc": "Restarts reader",
    },
    {
        "category": "System",
        "no": 6,
        "status": "Synced",
        "schema": "get_readerCapabilites",
        "api": "get_readerCapabilities",
        "method": "GET",
        "path": "/cloud/readerCapabilities",
        "desc": "Retrieves the Reader Capabilities",
    },
    {
        "category": "System",
        "no": 9,
        "status": "Synced",
        "schema": "get_config",
        "api": "get_config",
        "method": "GET",
        "path": "/cloud/config",
        "desc": "Retrieves reader configuration",
    },
    {
        "category": "System",
        "no": 10,
        "status": "Synced",
        "schema": "set_config",
        "api": "set_config",
        "method": "PUT",
        "path": "/cloud/config",
        "desc": "Updates reader configuration",
    },
    {
        "category": "System",
        "no": 13,
        "status": "Synced",
        "schema": "set_importCloudConfig",
        "api": "set_importCloudConfig",
        "method": "PUT",
        "path": "/cloud/cloudConfig",
        "desc": "Import cloud endpoint configuration",
    },
    {
        "category": "System",
        "no": 30,
        "status": "Synced",
        "schema": "set_cableLossCompensation",
        "api": "set_cableLossCompensation",
        "method": "PUT",
        "path": "/cloud/cableLossCompensation",
        "desc": "Sets the cable loss compensation",
    },
    {
        "category": "System",
        "no": 31,
        "status": "Synced",
        "schema": "get_cableLossCompensation",
        "api": "get_cableLossCompensation",
        "method": "GET",
        "path": "/cloud/cableLossCompensation",
        "desc": "Retrieves the cable loss compensation",
    },
    {
        "category": "System",
        "no": 56,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "set_passthru",
        "method": "PUT",
        "path": "/cloud/pass-through",
        "desc": "Pass-through command",
    },
    {
        "category": "System",
        "no": 59,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "set_password",
        "method": "PUT",
        "path": "/cloud/updatePassword",
        "desc": "Changes the password on the reader",
    },
    # Logs
    {
        "category": "Logs",
        "no": 32,
        "status": "Synced",
        "schema": "get_logs",
        "api": "get_logs",
        "method": "GET",
        "path": "/cloud/logs",
        "desc": "Log Configuration",
    },
    {
        "category": "Logs",
        "no": 33,
        "status": "Synced",
        "schema": "set_logs",
        "api": "set_logs",
        "method": "PUT",
        "path": "/cloud/logs",
        "desc": "Configures the logs",
    },
    {
        "category": "Logs",
        "no": 34,
        "status": "Synced",
        "schema": "get_logs_syslog",
        "api": "get_logs_syslog",
        "method": "GET",
        "path": "/cloud/logs/syslog",
        "desc": "Retrieve Syslog",
    },
    {
        "category": "Logs",
        "no": 35,
        "status": "Synced",
        "schema": "del_syslogs",
        "api": "del_logs_syslog",
        "method": "DELETE",
        "path": "/cloud/logs/syslog",
        "desc": "Purge Syslog",
    },
    {
        "category": "Logs",
        "no": 36,
        "status": "Synced",
        "schema": "get_radio_pkt_logs",
        "api": "get_logs_radioPacketLog",
        "method": "GET",
        "path": "/cloud/logs/radioPacketLog",
        "desc": "Retrieve radioPacketLog",
    },
    {
        "category": "Logs",
        "no": 37,
        "status": "Synced",
        "schema": "del_radio_pkt_logs",
        "api": "del_logs_radioPacketLog",
        "method": "DELETE",
        "path": "/cloud/logs/radioPacketLog",
        "desc": "Purge radioPacketLog",
    },
    {
        "category": "Logs",
        "no": 38,
        "status": "Synced",
        "schema": "get_rg_error_logs",
        "api": "get_logs_rgErrorLog",
        "method": "GET",
        "path": "/cloud/logs/RgErrorLog",
        "desc": "Retrieve RgErrorLog",
    },
    {
        "category": "Logs",
        "no": 39,
        "status": "Synced",
        "schema": "get_rg_warn_logs",
        "api": "get_logs_rgWarningLog",
        "method": "GET",
        "path": "/cloud/logs/RgWarningLog",
        "desc": "Retrieve RgWarningLog",
    },
    {
        "category": "Logs",
        "no": 40,
        "status": "Synced",
        "schema": "get_rc_log",
        "api": "get_logs_rcLog",
        "method": "GET",
        "path": "/cloud/logs/RcLog",
        "desc": "Retrieve RcInfoLog",
    },
    # Date&Time
    {
        "category": "Date&Time",
        "no": 16,
        "status": "Synced",
        "schema": "get_timeZone",
        "api": "get_timeZone",
        "method": "GET",
        "path": "/cloud/timeZone",
        "desc": "Retrieves the reader timezone",
    },
    {
        "category": "Date&Time",
        "no": 17,
        "status": "Synced",
        "schema": "set_timeZone",
        "api": "set_timeZone",
        "method": "PUT",
        "path": "/cloud/timeZone",
        "desc": "Sets the timezone",
    },
    {
        "category": "Date&Time",
        "no": 18,
        "status": "Synced",
        "schema": "get_ntpServer",
        "api": "get_ntpServer",
        "method": "GET",
        "path": "/cloud/ntpServer",
        "desc": "Retrieve the NTP server",
    },
    {
        "category": "Date&Time",
        "no": 19,
        "status": "Synced",
        "schema": "set_ntpServer",
        "api": "set_ntpServer",
        "method": "PUT",
        "path": "/cloud/ntpServer",
        "desc": "Set NTP server",
    },
    # Certificate
    {
        "category": "Certificate",
        "no": 48,
        "status": "Synced",
        "schema": "get_certs",
        "api": "get_certificates",
        "method": "GET",
        "path": "/cloud/certificates",
        "desc": "Retrieve certificate details",
    },
    {
        "category": "Certificate",
        "no": 49,
        "status": "Synced",
        "schema": "del_certs",
        "api": "del_certificate",
        "method": "DELETE",
        "path": "/cloud/certificates/{certname}",
        "desc": "Delete certificate",
    },
    {
        "category": "Certificate",
        "no": 50,
        "status": "Synced",
        "schema": "set_update_cert",
        "api": "set_updateCertificate",
        "method": "PUT",
        "path": "/cloud/certificates",
        "desc": "Install certificate",
    },
    {
        "category": "Certificate",
        "no": 51,
        "status": "Synced",
        "schema": "refresh-cert",
        "api": "set_refreshCertificate",
        "method": "PUT",
        "path": "/cloud/certificates/{certname}",
        "desc": "Refresh certificate",
    },
    {
        "category": "Certificate",
        "no": 71,
        "status": "Missing in API",
        "schema": "set_installCACertificate",
        "api": "---",
        "method": "---",
        "path": "---",
        "desc": "Install CA Certificate",
    },
    {
        "category": "Certificate",
        "no": 72,
        "status": "Missing in API",
        "schema": "get_CACertificates",
        "api": "---",
        "method": "---",
        "path": "---",
        "desc": "List Installed CA Certificates",
    },
    {
        "category": "Certificate",
        "no": 73,
        "status": "Missing in API",
        "schema": "del_CACertificate",
        "api": "---",
        "method": "---",
        "path": "---",
        "desc": "Delete CA Certificate",
    },
    # Network
    {
        "category": "Network",
        "no": 11,
        "status": "Synced",
        "schema": "get_network",
        "api": "get_network",
        "method": "GET",
        "path": "/cloud/network",
        "desc": "Retrieves reader network config",
    },
    {
        "category": "Network",
        "no": 12,
        "status": "Synced",
        "schema": "set_network",
        "api": "set_network",
        "method": "PUT",
        "path": "/cloud/network",
        "desc": "Updates reader network config",
    },
    {
        "category": "Network",
        "no": 14,
        "status": "Synced",
        "schema": "get_hostname",
        "api": "get_hostName",
        "method": "GET",
        "path": "/cloud/hostName",
        "desc": "Retrieves reader hostname",
    },
    {
        "category": "Network",
        "no": 15,
        "status": "Synced",
        "schema": "set_hostname",
        "api": "set_hostName",
        "method": "PUT",
        "path": "/cloud/hostName",
        "desc": "Sets reader hostname",
    },
    {
        "category": "Network",
        "no": 60,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "get_availableWifiNetworks",
        "method": "GET",
        "path": "/cloud/wifiNetworks",
        "desc": "Retrieves available Wi-Fi networks",
    },
    {
        "category": "Network",
        "no": 61,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "get_networkInterfaces",
        "method": "GET",
        "path": "/cloud/networkInterfaces",
        "desc": "Retrieves network interfaces",
    },
    {
        "category": "Network",
        "no": 62,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "get_readPoints",
        "method": "GET",
        "path": "/cloud/readPoints",
        "desc": "Gets the read points on the reader",
    },
    {
        "category": "Network",
        "no": 63,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "get_gpsCoordinates",
        "method": "GET",
        "path": "/cloud/readerLocation",
        "desc": "Gets the GPS coordinates",
    },
    {
        "category": "Network",
        "no": 64,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "get_eSimConfig",
        "method": "GET",
        "path": "/cloud/eSimConfig",
        "desc": "Gets the eSIM configuration",
    },
    {
        "category": "Network",
        "no": 65,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "set_eSimConfig",
        "method": "PUT",
        "path": "/cloud/eSimConfig",
        "desc": "Sets the eSIM configuration",
    },
    {
        "category": "Network",
        "no": 74,
        "status": "Missing in API",
        "schema": "set_nameAndDescription",
        "api": "---",
        "method": "---",
        "path": "---",
        "desc": "Set name and description of the reader",
    },
    {
        "category": "Network",
        "no": 75,
        "status": "Missing in API",
        "schema": "get_nameAndDescription",
        "api": "---",
        "method": "---",
        "path": "---",
        "desc": "Get name and description of the reader",
    },
    # Firmware
    {
        "category": "Firmware",
        "no": 7,
        "status": "Synced",
        "schema": "set_os",
        "api": "set_os",
        "method": "PUT",
        "path": "/cloud/os",
        "desc": "Updates OS software on device",
    },
    {
        "category": "Firmware",
        "no": 8,
        "status": "Synced",
        "schema": "revertback",
        "api": "set_revertbackOS",
        "method": "PUT",
        "path": "/cloud/revertbackOS",
        "desc": "Revert to previous OS version",
    },
    # userapp
    {
        "category": "userapp",
        "no": 41,
        "status": "Synced",
        "schema": "get_user_apps",
        "api": "get_userapps",
        "method": "GET",
        "path": "/cloud/apps",
        "desc": "List user applications",
    },
    {
        "category": "userapp",
        "no": 42,
        "status": "Synced",
        "schema": "install_user_app",
        "api": "set_installUserapp",
        "method": "PUT",
        "path": "/cloud/apps/install",
        "desc": "Install user application",
    },
    {
        "category": "userapp",
        "no": 43,
        "status": "Synced",
        "schema": "uninstall-user-app",
        "api": "set_uninstallUserapp",
        "method": "PUT",
        "path": "/cloud/apps/{appname}/uninstall",
        "desc": "Uninstall User Application",
    },
    {
        "category": "userapp",
        "no": 44,
        "status": "Synced",
        "schema": "start_user_app",
        "api": "set_startUserapp",
        "method": "PUT",
        "path": "/cloud/apps/{appname}/start",
        "desc": "Start user application",
    },
    {
        "category": "userapp",
        "no": 45,
        "status": "Synced",
        "schema": "stop_user_app",
        "api": "set_stopUserapp",
        "method": "PUT",
        "path": "/cloud/apps/{appname}/stop",
        "desc": "Stop user application",
    },
    {
        "category": "userapp",
        "no": 46,
        "status": "Synced",
        "schema": "autostart_user_app",
        "api": "set_autostartUserapp",
        "method": "PUT",
        "path": "/cloud/apps/{appname}/autostart",
        "desc": "Autostart user application",
    },
    {
        "category": "userapp",
        "no": 47,
        "status": "Synced",
        "schema": "set_req_usr_app",
        "api": "set_reqToUserapp",
        "method": "PUT",
        "path": "/cloud/apps/{appname}/pass-through",
        "desc": "Send Request to Userapp",
    },
    {
        "category": "userapp",
        "no": 66,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "set_dataToRG",
        "method": "PUT",
        "path": "/cloud/setdataToRG",
        "desc": "Set Data to RG",
    },
    # ImpinjGen2X
    {
        "category": "ImpinjGen2X",
        "no": 67,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "get_impinjGen2X",
        "method": "GET",
        "path": "/cloud/impinjGen2X",
        "desc": "Get Impinj Gen2X configuration",
    },
    {
        "category": "ImpinjGen2X",
        "no": 68,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "set_impinjGen2X",
        "method": "PUT",
        "path": "/cloud/impinjGen2X",
        "desc": "Set Impinj Gen2X configuration",
    },
    # Ble
    {
        "category": "Ble",
        "no": 69,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "set_bleConfig",
        "method": "PUT",
        "path": "/cloud/ble-config",
        "desc": "Set BLE configuration",
    },
    {
        "category": "Ble",
        "no": 70,
        "status": "Missing in Schema",
        "schema": "---",
        "api": "get_bleConfig",
        "method": "GET",
        "path": "/cloud/ble-config",
        "desc": "Get BLE configuration",
    },
]


def schema_keys(doc: dict) -> set[str]:
    return set(doc.get("components", {}).get("schemas", {}).keys())


def main() -> None:
    cmd_doc = json.loads(CMD_SCHEMAS_JSON.read_text(encoding="utf-8"))
    resp_doc = json.loads(RESP_SCHEMAS_JSON.read_text(encoding="utf-8"))

    cmd_keys = schema_keys(cmd_doc)
    resp_keys = schema_keys(resp_doc)

    for it in MASTER_ITEMS:
        schema = it["schema"]
        it["commandSchemaPresent"] = schema != "---" and schema in cmd_keys
        if schema == "---":
            it["responseSchemaPresent"] = False
        else:
            it["responseSchemaPresent"] = (schema + "_response" in resp_keys) or (
                schema in resp_keys
            )

    grouped: dict[str, list[dict]] = defaultdict(list)
    for it in MASTER_ITEMS:
        grouped[it["category"]].append(it)

    order = [
        "Login",
        "System",
        "Network",
        "Control",
        "Region",
        "Gpio",
        "App-led",
        "Stack-led",
        "Logs",
        "Date&Time",
        "Certificate",
        "Firmware",
        "userapp",
        "ImpinjGen2X",
        "Ble",
    ]

    lines: list[str] = []
    lines.append("# Master Command List (Grouped)")
    lines.append("")
    lines.append(
        "Grouped by your categories, with existence checks against `Command Schemas.json` and `Response Schemas.json`."
    )
    lines.append("")

    for category in order:
        if category not in grouped:
            continue
        lines.append(f"## {category}")
        lines.append("")
        lines.append(
            "| No. | Status | Schema List Name | In Command Schemas.json | In Response Schemas.json | API List Name | Method | Path | Description |"
        )
        lines.append("|---:|---|---|---|---|---|---|---|---|")
        for it in sorted(grouped[category], key=lambda x: x["no"]):
            lines.append(
                "| {no} | {status} | {schema} | {c} | {r} | {api} | {method} | {path} | {desc} |".format(
                    no=it["no"],
                    status=it["status"],
                    schema=it["schema"],
                    c="Yes" if it["commandSchemaPresent"] else "No",
                    r="Yes" if it["responseSchemaPresent"] else "No",
                    api=it["api"],
                    method=it["method"],
                    path=it["path"],
                    desc=it["desc"],
                )
            )
        lines.append("")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

