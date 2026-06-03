# set_importCloudConfig

## 1. Description

The `set_importCloudConfig` command imports a cloud endpoint configuration onto the reader, defining how tag data, control responses, and management events are delivered.

Use it to:

- Provision MQTT, HTTP, WebSocket, or cloud-specific (Azure/AWS) data endpoints
- Configure control and management command-response channels
- Set batching and retention options per connection

## 2. Command Details

| Property | Value |
|---|---|
| Pattern Name | Cloud Endpoint Configuration Import |
| Communication Type | Bidirectional (Cloud to Device, Device to Cloud) |
| Applies To | FX7500, FX9600, ATR7000 |
| Related Commands | [get_config](get_config.md), [set_config](set_config.md), [get_certs](get_certs.md) |
| Required Request Fields | `command`, `command_id`, `payload` |
| Supported Operations | Import cloud endpoint configuration |
| Supported API Versions | V1.0 |

> **Security Note:** Endpoint connections include TLS certificates, usernames, and passwords. Never hardcode sensitive values in your payload. Supply them at runtime from a secrets manager or environment variable.

## 3. Before You Begin

Gather these details before sending the command. An incorrect hostname, port, or certificate reference will prevent the reader from connecting to your cloud backend.

| What You Need | Details |
|---|---|
| Endpoint channels | Which channels to configure: `data.event`, `control.commandResponse`, `management.event`, `management.commandResponse`. |
| Connection type | Per connection: `mqtt`, `httpPost`, `tcpip-server`, `WEBSOCKET`, `mqtt-AZURE`, `mqtt-AWS`, etc. |
| Host / port / topics | MQTT: `hostName`, `port`, `protocol`, `publishTopic`, `subscribeTopic` (for cmdResp). |
| Certificates / auth | TLS cert name/type or inline PEM; `basicAuthentication` username/password if used. |

## 4. Connection Types

The `type` field in each `connections[]` entry defines the transport.

| type | Description | Authentication |
|---|---|---|
| `mqtt` | Standard MQTT broker | TLS + optional basic auth |
| `httpPost` | HTTP POST data delivery | TLS + basic auth |
| `tcpip-server` | TCP/IP server socket | TLS optional |
| `WEBSOCKET` | WebSocket connection | TLS optional |
| `mqtt-AZURE` | Azure IoT Hub MQTT | Azure-specific options |
| `mqtt-AWS` | AWS IoT Core MQTT | AWS-specific options |
| `keyboard-emulation` | Keyboard emulation output | N/A |

## 5. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `payload.endpointConfig` | object | No | Root object for all endpoint channels. |
| `payload.endpointConfig.data.event` | object | No | Tag data event channel with `connections[]`. |
| `payload.endpointConfig.control.commandResponse` | object | No | Control command-response channel. |
| `payload.endpointConfig.management.event` | object | No | Management event channel. |
| `payload.endpointConfig.management.commandResponse` | object | No | Management command-response channel. |
| `payload.endpointConfig.*.connections[].type` | string | No | Transport type (see table above). |
| `payload.endpointConfig.*.connections[].name` | string | No | Endpoint display name. |
| `payload.endpointConfig.*.connections[].options` | object | No | Type-specific options (host, port, security, topics). |
| `payload.endpointConfig.*.connections[].options.endpoint.hostName` | string | If mqtt | Broker hostname or IP. |
| `payload.endpointConfig.*.connections[].options.endpoint.port` | integer | If mqtt | Broker port. |
| `payload.endpointConfig.*.connections[].options.publishTopic` | string[] | If mqtt | Topics to publish tag data / responses. |
| `payload.endpointConfig.*.connections[].additionalOptions.batching` | object | No | `reportingInterval`, `maxPayloadSizePerReport`. |
| `payload.endpointConfig.*.connections[].additionalOptions.retention` | object | No | `throttle`, `maxNumEvents`, `maxEventRetentionTimeInMin`. |

> **Note:** Review `get_config` first to see existing endpoint settings before importing a new cloud configuration.
