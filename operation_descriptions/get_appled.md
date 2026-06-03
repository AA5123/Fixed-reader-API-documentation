# get_appled

## 1. Description

The `get_appled` command retrieves the current state of the application LED on the reader.

This command returns:

- The application LED status (DEFAULT or NOT_DEFAULT)

No additional payload fields are required to retrieve the LED state.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Application LED Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | set_appled, get_stackled |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve current application LED state |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_appled` to:

- Confirm whether the app LED is in its default state
- Verify the effect of a prior `set_appled` call
- Audit LED state as part of a device health check

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `status` | App LED status (DEFAULT / NOT_DEFAULT) | Indicates whether an application has overridden the LED |

> **Note:** Use `get_appled` before `set_appled` to confirm the current state before changing LED behavior.
