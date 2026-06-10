# Status API Schema Follow-up Note

## Context
This note captures differences observed between the tested REST `/cloud/status` response and the current documented schema.

## Observed Gaps
1. `impinjGen2X.feature` returned value `none`, but the documented enum currently allows only:
   - `fastId`
   - `tagFocus`
   - `tagProtect`
   - `tagQuieting`
2. Tested payload uses `impinjGen2X.isActive`, while schema documents `impinjGen2X.active`.

## Decision Status
Pending developer confirmation.

## Proposed Resolution (After Developer Review)
1. If device payload is the source of truth, update schema and examples to include `feature: none` and align `isActive` vs `active`.
2. If schema is the source of truth, align firmware/output mapping to documented fields and enum values.

## Reference
- Endpoint: `GET /cloud/status`
- Schema file: `RestAPI/paths/system/status.yaml`

## MQTT Tested Result (June 3, 2026)

```json
{
   "command": "get_status",
   "command_id": "cmd_0_583763",
   "payload": {
      "antennas": {
         "1": "disconnected",
         "2": "disconnected",
         "3": "disconnected",
         "4": "disconnected",
         "5": "connected",
         "6": "connected"
      },
      "cpu": {
         "system": 0,
         "user": 15
      },
      "flash": {
         "platform": {
            "free": 0,
            "total": 0,
            "used": 0
         },
         "readerConfig": {
            "free": 0,
            "total": 0,
            "used": 0
         },
         "readerData": {
            "free": 0,
            "total": 0,
            "used": 0
         },
         "rootFileSystem": {
            "free": 0,
            "total": 0,
            "used": 0
         }
      },
      "impinjGen2X": {
         "feature": "none",
         "isActive": false
      },
      "interfaceConnectionStatus": {
         "data": [
            {
               "connectionError": "",
               "connectionStatus": "disconnected",
               "description": "TCP_TagData",
               "interface": "TCP_TagData"
            },
            {
               "connectionError": "",
               "connectionStatus": "disconnected",
               "description": "WEBSOCKET",
               "interface": "WEBSOCKET"
            }
         ]
      },
      "ntp": {
         "offset": 0.048848,
         "reach": 377
      },
      "powerNegotiation": "POE+",
      "powerSource": "PWR_BRICK",
      "radioActivity": "active",
      "radioConnection": "connected",
      "ram": {
         "free": 63,
         "total": 100,
         "used": 37
      },
      "systemTime": "03/06/2026 08:49",
      "temperature": 49,
      "uptime": "10D20H8M9S"
   },
   "response": "success",
   "requested_command": "get_status",
   "response_topic": "response"
}
```

## Validation Against Current Schema

Matches:
1. Core envelope fields are present: command, command_id, payload, response.
2. Most payload fields and value types align with current documentation.

Mismatches to review with developer:
1. impinjGen2X.feature value is none, but documented enum does not include none.
2. Payload uses impinjGen2X.isActive, while documented field is impinjGen2X.active.
3. Payload includes requested_command and response_topic, which are not declared in the current response schema.
