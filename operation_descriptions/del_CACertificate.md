# del_CACertificate

## Description

The `del_CACertificate` command removes an installed CA (Certificate Authority) root certificate from the reader.

Use this command to:

- Remove a CA certificate that is no longer trusted
- Clean up CA entries before installing a replacement with `set_installCACertificate`
- Rotate PKI trust anchors on the device

## Command Details

| Property | Value |
|---|---|
| Pattern Name | CA Certificate Deletion |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_CACertificates](get_CACertificates.md), [set_installCACertificate](set_installCACertificate.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported API Versions | V1.0 |

## Before You Begin

Deleting a CA certificate used for TLS verification on active endpoints will cause connection failures.

| What You Need | Details |
|---|---|
| CA name | Exact `name` of the CA certificate to delete. |

## Sending the Command

### Example: Delete CA certificate

```json
{
  "command": "del_CACertificate",
  "command_id": "abcd1324",
  "payload": {
    "name": "cacert"
  }
}
```

## Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.name` | string | Yes | Name of the CA certificate to delete. |

## Reading the Response

The reader responds with `response: "success"` or `"failure"`. Match `command_id` in the response.
