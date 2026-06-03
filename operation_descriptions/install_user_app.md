# install_user_app

## Description

The `install_user_app` command installs a user application (`.deb` package) on the reader from an HTTP(S) file server.

Use this command to:

- Deploy custom on-reader applications
- Update user-app packages from a central repository
- Extend reader functionality with Zebra-approved `.deb` packages

## Command Details

| Property | Value |
|---|---|
| Pattern Name | User Application Installation |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_user_apps](get_user_apps.md), [uninstall-user-app](uninstall-user-app.md), [start_user_app](start_user_app.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Authentication Types | `NONE`, `BASIC` |
| Supported API Versions | V1.0 |

> **Security Note:** Never hardcode passwords or JWT tokens in your payload. Supply credentials at runtime from a secrets manager.

MQTT command key: `set_installUserapp`.

## Before You Begin

Gather download server details before sending. The reader must reach the URL from its network.

| What You Need | Details |
|---|---|
| File server URL | HTTP or HTTPS base URL hosting the `.deb` package. |
| Filename | Exact `.deb` filename on the server. |
| Authentication | `NONE` or `BASIC` (with `options.username` / `options.password`). |
| TLS verification | `verifyPeer`, `verifyHost`, and optional CA cert path or inline content. |

## Authentication Types

| authenticationType | Description | Credentials Required |
|---|---|---|
| `NONE` | No HTTP authentication | None |
| `BASIC` | Username/password auth | `options.username`, `options.password` |

## Sending the Command

### Example: Install user app

```json
{
  "command": "set_installUserapp",
  "command_id": "abcd123",
  "payload": {
    "url": "https://example.com/apps/",
    "filename": "sample_1.0.0.deb",
    "authenticationType": "NONE",
    "verifyPeer": true,
    "verifyHost": true
  }
}
```

## Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.url` | string | Yes | HTTP(S) file server URL. |
| `payload.filename` | string | Yes | User app `.deb` filename on the server. |
| `payload.authenticationType` | string | Yes | `NONE` or `BASIC`. |
| `payload.options.username` | string | If BASIC | HTTP username. |
| `payload.options.password` | string | If BASIC | HTTP password. |
| `payload.verifyPeer` | boolean | No | Verify server certificate (default `true`). |
| `payload.verifyHost` | boolean | No | Verify server hostname (default `true`). |
| `payload.headers.Authorization` | string | No | Bearer JWT for API authentication. |
| `payload.retry` | object | No | Retry policy (`type`, `policy.retries`, `wait.min/max`). |
| `payload.timeouts.connection` | integer | No | Connection timeout in seconds. |
| `payload.timeouts.read` | integer | No | Read timeout in seconds. |

## Reading the Response

The reader responds with `response: "success"` or `"failure"`. Confirm installation with `get_user_apps`.
