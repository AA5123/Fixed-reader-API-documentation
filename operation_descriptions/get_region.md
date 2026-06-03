# get_region

## 1. Description

The `get_region` command retrieves the reader's currently configured RF region and the regulatory parameters in effect.

This command returns:

- The active region and regulatory standard
- Listen-before-talk (LBT) state
- Enabled channels and minimum transmit power

No additional payload fields are required to retrieve the active region settings.

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Region Configuration Query |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | set_region, get_SupportedRegionList, get_SupportedStandardlist |
| Required Request Fields | command, command_id |
| Supported Operations | Retrieve active RF region and regulatory settings |
| Supported Response Sections | payload |
| Supported API Versions | V1.0 |

## 3. When to Use This Command

Use `get_region` to:

- Confirm the reader is set to the correct regulatory region
- Verify LBT and channel configuration before inventory
- Audit minimum transmit power for the region
- Validate region settings after deployment to a new country

Key fields to check in the response:

| Field | What to Check | Why It Matters |
|---|---|---|
| `region` | Active RF region of operation | Must match the country of deployment |
| `regulatoryStandard` | RF regulatory standard followed | Governs legal RF operation |
| `lbtEnabled` | Listen-before-talk enabled flag | Required in some regions |
| `channelData` | List of enabled channels | Determines usable RF spectrum |

> **Note:** Use `get_region` before `set_region`, and cross-check `get_SupportedRegionList` to ensure the target region is permitted on this reader.
