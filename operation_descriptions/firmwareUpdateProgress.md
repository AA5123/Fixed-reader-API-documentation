# firmwareUpdateProgress

## 1. Description

The `firmwareUpdateProgress` event reports the status and progress of an in-flight firmware update.

This event includes:

- The current update `status`
- Per-image and overall progress percentages
- Failure reason or per-partition progress details

Use this event to:

- Track an OS update started with `set_os`
- Surface update progress in an operator dashboard
- Detect and react to update failures

## 2. Event Details

| Property | Value |
|---|---|
| Event Type | Firmware Update Progress |
| Communication Type | Device to Cloud |
| Applies To | FX7500, FX9600, ATR7000 |
| Trigger Condition | Published while a firmware update is in progress, on status/progress changes |
| Related Events | async-events, error |
| Supported API Versions | V1.0 |

## 3. When This Event Is Published

The reader publishes `firmwareUpdateProgress` automatically after `set_os` begins, as the update transitions through states. No command is required.

| `status` | Meaning |
|---|---|
| `started` | Update has begun |
| `downloading-<image>` | Downloading an image partition |
| `erasing-<image>` | Erasing an image partition |
| `writing-<image>` | Writing an image partition |
| `rebooting` | Reader rebooting to apply the update |
| `failed` | Update failed (see `updateProgressDetails`) |

### Key Fields

| Field | Type | Description |
|---|---|---|
| `status` | string | Current update status (see table). |
| `imageDownloadProgress` | number | Current partition progress (0–100). |
| `overallUpdateProgress` | number | Overall update progress (0–100). |
| `updateProgressDetails` | string or object | Failure reason, or per-partition progress (`os`, `radioFirmware`, `platform`). |

> **Note:** A `failed` status includes a reason in `updateProgressDetails`; a `rebooting` status means the reader will briefly disconnect.
