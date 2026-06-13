# FX90 API Documentation

MQTT-based API for controlling Zebra fixed RFID readers (**FX7500**, **FX9600**, **ATR7000**).

## Overview

Each operation is an MQTT **command** sent as JSON with `command`, `command_id`, and `payload`. Responses use the same envelope shape. Use the **Example** tab for copy-ready payloads; use **Schema** for field types, enums, and constraints.

Paths shown in this reference (for example `/get_version`) are documentation aliases — they are **not** HTTP endpoints.

## Details

| Item | Value |
|------|-------|
| Transport | MQTT (RAW JSON payloads) |
| Reader families | FX7500,
