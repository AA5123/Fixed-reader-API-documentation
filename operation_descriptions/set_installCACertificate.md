# set_installCACertificate

## 1. Description

The `set_installCACertificate` command installs a CA (Certificate Authority) root certificate on the reader.

Use it to:

- Trust a private CA for TLS connections to your MQTT or HTTP endpoints
- Add a CA certificate required for certificate validation
- Support mutual TLS with your organization's PKI

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | CA Certificate Installation |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_CACertificates](get_CACertificates.md), [del_CACertificate](del_CACertificate.md), [set_update_cert](set_update_cert.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Install a CA root certificate |
| Supported API Versions | V1.0 |

> **Security Note:** Never hardcode certificate PEM content in source code. Supply `content` at runtime from a secure store.

## 3. Before You Begin

Gather these details before sending the command. Invalid PEM content will be rejected.

| What You Need | Details |
|---|---|
| CA name | Unique name for the CA certificate on the reader. |
| PEM content | Full PEM-encoded CA certificate string. |

## 4. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.name` | string | Yes | CA certificate name. |
| `payload.content` | string | Yes | PEM-encoded CA certificate content. |

> **Note:** MQTT command key in the request envelope is `set_InstallCACertificate`.
