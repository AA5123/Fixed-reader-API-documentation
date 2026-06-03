# refresh-cert

## Description

The `refresh-cert` command refreshes an already-installed certificate on the reader by re-fetching or re-applying it from its configured source.

Use this command to:

- Renew a certificate before expiry without a full reinstall
- Re-apply a certificate after upstream CA rotation
- Trigger certificate refresh as part of a credential rotation workflow

## Command Details

| Property | Value |
|---|---|
| Pattern Name | Certificate Refresh |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_certs](get_certs.md), [set_update_cert](set_update_cert.md), [del_certs](del_certs.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Certificate Types | `client`, `server`, `app` |
| Supported API Versions | V1.0 |

MQTT command key: `set_refreshCertificate`.

## Before You Begin

The certificate must already be installed. Use `get_certs` to confirm the `name` and `type`.

| What You Need | Details |
|---|---|
| Certificate name | Exact name of the installed certificate. |
| Certificate type | `client`, `server`, or `app`. |

## Sending the Command

### Example: Refresh certificate

```json
{
  "command": "set_refreshCertificate",
  "command_id": "abcd1324",
  "payload": {
    "name": "my_client_cert",
    "type": "client"
  }
}
```

## Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.name` | string | Yes | Certificate name to refresh. |
| `payload.type` | string | Yes | Certificate type: `client`, `server`, or `app`. |

## Reading the Response

The reader responds with `response: "success"` or `"failure"`. Verify the updated certificate with `get_certs`.
