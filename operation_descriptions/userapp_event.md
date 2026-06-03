# userapp_event

## 1. Description

The `userapp_event` event delivers asynchronous custom events emitted by a user application running on the reader.

This event includes:

- A raw event string defined by the user application

Use this event to:

- Receive custom signals from on-reader applications
- Integrate application-specific logic with your backend
- Forward user-app state changes to external systems

## 2. Event Details

| Property | Value |
|---|---|
| Event Type | Userapp Event |
| Communication Type | Device to Cloud |
| Applies To | FX7500, FX9600, ATR7000 |
| Trigger Condition | Published when a user application emits a custom event (enable via `userappEvents`) |
| Related Events | async-events, heartbeat |
| Supported API Versions | V1.0 |

## 3. When This Event Is Published

The reader publishes `userapp_event` when an installed user application emits an event. The envelope `component` field carries the app name. No command is required.

| Field | Type | Description |
|---|---|---|
| `event` | string | Raw event string defined by the user application. |

> **Note:** The `event` payload is opaque to the reader — its structure is defined entirely by the user application that emits it.
