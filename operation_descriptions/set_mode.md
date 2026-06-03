# set_mode

## 1. Description

The `set_mode` command configures the reader's operating mode and the RF settings associated with that mode.

Use it to:

- Switch between SIMPLE, INVENTORY, PORTAL, CONVEYOR, CUSTOM, or DIRECTIONALITY modes
- Tune antennas, transmit power, and environment profile for the deployment
- Configure mode-specific settings (inventory interval, portal triggers, directionality zones)

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Operating Mode Configuration |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_mode](get_mode.md), [start](start.md), [stop](stop.md), [get_config](get_config.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Configure operating mode and RF parameters |
| Supported API Versions | V1.0 |

## 3. Before You Begin

Gather these details before sending the command. Changing mode while inventory is active can disrupt reads — call `stop` first if needed.

| What You Need | Details |
|---|---|
| Mode type | One of `SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`, `CUSTOM`, `DIRECTIONALITY`. |
| Antennas / power | Which antenna ports (or ATR beams) and TX power in dBm. |
| Mode-specific settings | Inventory interval, portal GPI triggers, or directionality zone plan — depends on `type`. |
| Environment | Optional RF environment profile (`LOW_INTERFERENCE`, `HIGH_INTERFERENCE`, `VERY_HIGH_INTERFERENCE`, `AUTO_DETECT`, `DEMO`). |

## 4. Operating Modes

The `type` field in the payload defines the operating mode.

| type | Description | modeSpecificSettings |
|---|---|---|
| `SIMPLE` | Basic continuous read | Not required |
| `INVENTORY` | Timed or triggered inventory | `interval` (unit + value) |
| `PORTAL` | Portal/dock read with GPI triggers | `startTrigger`, `stopInterval` |
| `CONVEYOR` | Conveyor-style read | Mode-specific conveyor settings |
| `CUSTOM` | Custom mode configuration | Custom settings object |
| `DIRECTIONALITY` | Zone-based direction detection | `basicConfig`, `beamConfig`, zone plan |

## 5. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.type` | string | Yes | Operating mode. Allowed: `SIMPLE`, `INVENTORY`, `PORTAL`, `CONVEYOR`, `CUSTOM`, `DIRECTIONALITY`. |
| `payload.modeSpecificSettings` | object | If mode requires | Settings object whose shape depends on `type`. |
| `payload.antennas` | array of integer | No | Antenna ports or ATR beam numbers to use. |
| `payload.transmitPower` | number or array | No | TX power in dBm (single value or per-antenna array). |
| `payload.environment` | string | No | RF environment profile. |
| `payload.filter` | object | No | Tag ID filter (`value`, `match`, `operation`). |
| `payload.antennaStopCondition` | object/array | No | Per-antenna stop condition (`type`, `value`). |
| `payload.query` | object/array | No | Gen2 query parameters (`sel`, `session`, `target`, `tagPopulation`). |
| `payload.tagMetaData` | array | No | Metadata fields to include in tag reports. |
| `payload.modeSpecificSettings.interval.unit` | string | If INVENTORY | Interval unit: `seconds`, `minutes`, `hours`, `days`. |
| `payload.modeSpecificSettings.interval.value` | integer | If INVENTORY | Interval value. |
| `payload.modeSpecificSettings.startTrigger.port` | integer | If PORTAL | GPI port (1–4) for start trigger. |
| `payload.modeSpecificSettings.startTrigger.signal` | string | If PORTAL | Trigger signal: `HIGH` or `LOW`. |

> **Note:** Use `get_mode` before `set_mode` to review the active configuration. The schema defines 20+ additional optional RF fields — see the **Schema** tab for the full list.
