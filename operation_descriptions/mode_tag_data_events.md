# mode_tag_data_events

## 1. Description

The `mode_tag_data_events` payload carries RFID tag read data during SIMPLE, INVENTORY, PORTAL, CONVEYOR, or CUSTOM operating modes.

This event includes:

- Tag identity (`idHex`, `format`) and read metadata (antenna, RSSI, channel, phase)
- Read count and optional memory-bank fields (CRC, PC, TID, USER, XPC)

Use this event to:

- Process individual tag reads in inventory workflows
- Filter and deduplicate tags using `idHex` and `reads`
- Build read-quality metrics from RSSI, antenna, and phase data

## 2. Event Details

| Property | Value |
|---|---|
| Event Type | Mode Tag Data |
| Communication Type | Device to Cloud |
| Applies To | FX7500, FX9600, ATR7000 |
| Trigger Condition | Published when a tag is inventoried/reported in a non-directionality mode |
| Related Events | tagDataEvents, directionality_tag_data_events |
| Supported API Versions | V1.0 |

## 3. When This Event Is Published

The reader publishes this payload inside the `tagDataEvents` envelope when a tag is read during SIMPLE, INVENTORY, PORTAL, CONVEYOR, or CUSTOM mode. No command is required beyond starting inventory (`start`).

| Field | Type | Description |
|---|---|---|
| `eventNum` | number | Event sequence number. |
| `idHex` | string | EPC bank contents as a hex string. |
| `format` | string | ID format (e.g. `EPC`). |
| `antenna` | integer | Antenna port that read the tag. |
| `peakRssi` | number | Peak RSSI in dBm. |
| `reads` | number | Times tag seen since last report. |
| `channel` | number | RF channel in MHz. |
| `phase` | number | Tag phase in degrees. |
| `CRC` / `PC` / `TID` / `USER` / `XPC` | varies | Optional memory-bank fields when configured. |

> **Note:** Which optional fields appear depends on `tagMetaData` configuration in `set_mode`. See the **Schema** tab for the full field list.
