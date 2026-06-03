Asynchronous management events the reader publishes to MQTT, HTTP, WebSocket, or cloud endpoints configured under `managementEventConfig`. These are not request/response commands — the reader pushes them when state changes.

| Event | Description |
|---|---|
| [async-events](#op-async-events) | Generic asynchronous management event envelope |
| [heartbeat](#op-heartbeat) | Periodic reader health and activity snapshot |
| [firmwareUpdateProgress](#op-firmwareupdateprogress) | Firmware update progress notifications |
| [gpi](#op-gpi) | General-purpose input state-change event |
| [gpo](#op-gpo) | General-purpose output state-change event |
| [error](#op-error) | Error event reported by the reader |
| [warning](#op-warning) | Warning event reported by the reader |
| [userapp_event](#op-userapp-event) | Event emitted by a user application |
