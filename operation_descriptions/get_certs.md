# get_certs

## 1. Description

The `get_certs` command retrieves the list of certificates installed on the reader.

This command returns:

- An array of installed certificates, each with name, type, serial, and validity dates

No additional payload fields are required to retrieve all installed certificates.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Certificate Inventory Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | set_update_cert, del_certs, refresh-cert, get_CACertificates |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve the list of installed certificates |
| Supported Response Sections | payload (array) |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_certs` to:

- Audit which certificates are installed and their types
- Check certificate validity windows before expiry
- Confirm a certificate was installed or removed
- Retrieve the full list of certificates on the device

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `name` | Certificate name | Identifies the certificate for update/delete |
| `type` | Certificate type (server / client / app) | Determines how the certificate is used |
| `validityStart` | Validity start date (DD/MM/YYYY) | Confirms the certificate is already active |
| `validityEnd` | Validity end date (DD/MM/YYYY) | Flags upcoming expiry that needs renewal |

> **Note:** Use `get_certs` before `set_update_cert` or `del_certs` to reference the exact certificate `name`.
