# set_update_cert

## 1. Description

The `set_update_cert` command installs or updates a certificate on the reader, fetched from an FTPS URL or supplied inline as PFX content.

Use it to:

- Install a new TLS certificate for MQTT or HTTP endpoints
- Update an existing certificate before expiry
- Provision client, server, or application certificates

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Certificate Installation |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_certs](get_certs.md), [del_certs](del_certs.md), [refresh-cert](refresh-cert.md), [set_installCACertificate](set_installCACertificate.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Install or update a certificate |
| Supported API Versions | V1.0 |

> **Security Note:** Never hardcode FTPS passwords, PFX passwords, or certificate content in your payload. Supply credentials at runtime from a secrets manager or environment variable.

## 3. Before You Begin

Gather these details before sending the command. An invalid URL, wrong certificate type, or bad PFX password will cause installation to fail.

| What You Need | Details |
|---|---|
| Certificate name | Unique name for the certificate on the reader. |
| Certificate type | `server`, `client`, or `app`. |
| Source | FTPS `url` hosting the certificate/PFX, **or** inline `pfxFileName` + `pfxContent`. |
| FTPS authentication | `NONE` or `BASIC` (with `options.username` / `options.password`). |
| PFX password | Password for the PFX file, if applicable. |

## 4. Authentication Types

The `authenticationType` field controls FTPS server authentication.

| authenticationType | Description | Credentials Required |
|---|---|---|
| `NONE` | No FTPS authentication | None |
| `BASIC` | Username/password FTPS auth | `options.username`, `options.password` |

## 5. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.name` | string | Yes | Certificate name on the reader. |
| `payload.type` | string | Yes | Certificate role: `server`, `client`, or `app`. |
| `payload.url` | string | Yes | FTPS URL hosting the certificate or PFX file. |
| `payload.authenticationType` | string | No | FTPS auth: `NONE` or `BASIC`. |
| `payload.options.username` | string | If BASIC | FTPS username. |
| `payload.options.password` | string | If BASIC | FTPS password. |
| `payload.pfxPassword` | string | No | Password for the PFX file. |
| `payload.pfxFileName` | string | No | Inline PFX filename (alternative to URL). |
| `payload.pfxContent` | string | No | Inline Base64 PFX content (alternative to URL). |
| `payload.verifyHost` | boolean | No | Verify server hostname (TLS). |
| `payload.verifyPeer` | boolean | No | Verify server certificate (TLS). |

> **Note:** Use `get_certs` to confirm the certificate list before installing. MQTT command key in the payload is `set_updateCertificate`.
