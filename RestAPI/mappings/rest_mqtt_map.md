# REST ↔ MQTT mapping

Generated from `RestAPI/FX90.yaml` and `tag_config.json`.
Regenerate: `python scripts/generate_rest_mqtt_map.py`

## Summary

| Metric | Count |
|--------|------:|
| REST HTTP operations | 70 |
| MQTT operations (total) | 88 |
| Matched (REST has MQTT equivalent) | 70 |
| MQTT-only | 18 (5 commands, 13 events) |

## REST → MQTT (all 70 operations)

| Tag | Method | REST path | MQTT command | operationId |
|-----|--------|-----------|--------------|-------------|
| App-led | GET | `/cloud/app-led` | `get_appled` | getAppled |
| App-led | PUT | `/cloud/app-led` | `set_appled` | setAppled |
| userapp | GET | `/cloud/apps` | `get_user_apps` | getUserapps |
| userapp | PUT | `/cloud/apps/install` | `install_user_app` | setInstalluserapp |
| userapp | PUT | `/cloud/apps/{appname}/autostart` | `autostart_user_app` | setAutostartuserapp |
| userapp | PUT | `/cloud/apps/{appname}/pass-through` | `set_req_usr_app` | setReqtouserapp |
| userapp | PUT | `/cloud/apps/{appname}/start` | `start_user_app` | setStartuserapp |
| userapp | PUT | `/cloud/apps/{appname}/stop` | `stop_user_app` | setStopuserapp |
| userapp | PUT | `/cloud/apps/{appname}/uninstall` | `uninstall-user-app` | setUninstalluserapp |
| Ble | GET | `/cloud/ble-config` | `get_bleConfig` | getBleConfig |
| Ble | PUT | `/cloud/ble-config` | `set_bleConfig` | setBleConfig |
| System | GET | `/cloud/cableLossCompensation` | `get_cableLossCompensation` | getCablelosscompensation |
| System | PUT | `/cloud/cableLossCompensation` | `set_cableLossCompensation` | setCablelosscompensation |
| Certificate | GET | `/cloud/certificates` | `get_certs` | getCertificates |
| Certificate | PUT | `/cloud/certificates` | `set_update_cert` | setUpdatecertificate |
| Certificate | DELETE | `/cloud/certificates/{certname}` | `del_certs` | delCertificate |
| Certificate | PUT | `/cloud/certificates/{certname}` | `refresh-cert` | setRefreshcertificate |
| System | PUT | `/cloud/cloudConfig` | `set_importCloudConfig` | setImportcloudconfig |
| System | GET | `/cloud/config` | `get_config` | getConfig |
| System | PUT | `/cloud/config` | `set_config` | setConfigMqtt |
| Network | GET | `/cloud/eSimConfig` | `get_eSimConfig` |  |
| Network | PUT | `/cloud/eSimConfig` | `set_eSimConfig` | setEsimConfig |
| Gpio | GET | `/cloud/gpi` | `get_gpi_status` | getGPIStatus |
| Gpio | GET | `/cloud/gpo` | `get_gpostatus` |  |
| Gpio | PUT | `/cloud/gpo` | `set_gpo` | setGpo |
| Network | GET | `/cloud/hostName` | `get_hostname` | getHostName |
| Network | PUT | `/cloud/hostName` | `set_hostname` | setHostName |
| ImpinjGen2X | GET | `/cloud/impinjGen2X` | `get_impinjGen2X` | getImpinjGen2X |
| ImpinjGen2X | PUT | `/cloud/impinjGen2X` | `set_impinjGen2X` | setImpinjGen2X |
| Login | GET | `/cloud/localRestLogin` | `localrest_login` | localrestlogin |
| Logs | GET | `/cloud/logs` | `get_logs` | getLogs |
| Logs | PUT | `/cloud/logs` | `set_logs` | setLogs |
| Logs | GET | `/cloud/logs/RcLog` | `get_rc_log` |  |
| Logs | GET | `/cloud/logs/RgErrorLog` | `get_rg_error_logs` |  |
| Logs | GET | `/cloud/logs/RgWarningLog` | `get_rg_warn_logs` |  |
| Logs | DELETE | `/cloud/logs/radioPacketLog` | `del_radio_pkt_logs` |  |
| Logs | GET | `/cloud/logs/radioPacketLog` | `get_radio_pkt_logs` |  |
| Logs | DELETE | `/cloud/logs/syslog` | `del_syslogs` |  |
| Logs | GET | `/cloud/logs/syslog` | `get_logs_syslog` |  |
| Control | GET | `/cloud/mode` | `get_mode` | getMode |
| Control | PUT | `/cloud/mode` | `set_mode` | setMode |
| Network | GET | `/cloud/network` | `get_network` | getNetwork |
| Network | PUT | `/cloud/network` | `set_network` | updateNetwork |
| Network | GET | `/cloud/networkInterfaces` | `get_networkInterfaces` | getNetworkinterfaces |
| Date&Time | GET | `/cloud/ntpServer` | `get_ntpServer` |  |
| Date&Time | PUT | `/cloud/ntpServer` | `set_ntpServer` | updateNtpServer |
| Firmware | PUT | `/cloud/os` | `set_os` | setOs |
| System | PUT | `/cloud/pass-through` | `set_passthru` | status |
| Control | GET | `/cloud/preSelection` | `get_preSelection` |  |
| Control | PUT | `/cloud/preSelection` | `set_preSelection` |  |
| Network | GET | `/cloud/readPoints` | `get_readPoints` | getReadpoints |
| System | GET | `/cloud/readerCapabilities` | `get_readerCapabilites` | getReadercapabilities |
| Network | GET | `/cloud/readerLocation` | `get_gpsCoordinates` | getGpsCoordinates |
| System | PUT | `/cloud/reboot` | `reboot` | reboot |
| Region | GET | `/cloud/region` | `get_region` | getRegion |
| Region | PUT | `/cloud/region` | `set_region` | setRegion |
| Firmware | PUT | `/cloud/revertbackOS` | `revertback` | setRevertbackos |
| userapp | PUT | `/cloud/setdataToRG` | `set_dataToRG` | setDataToRG |
| Stack-led | GET | `/cloud/stack-led` | `get_stackled` | getStackled |
| Stack-led | PUT | `/cloud/stack-led` | `set_stackled` | setStackled |
| Control | PUT | `/cloud/start` | `start` | startInventory |
| System | GET | `/cloud/status` | `get_status` | getStatus |
| Control | PUT | `/cloud/stop` | `stop` | stopInventory |
| Region | GET | `/cloud/supportedRegionList` | `get_SupportedRegionList` | getSupportedregionlist |
| Region | GET | `/cloud/supportedStandardList` | `get_SupportedStandardlist` | getSupportedstandardlist |
| Date&Time | GET | `/cloud/timeZone` | `get_timeZone` | getTimezone |
| Date&Time | PUT | `/cloud/timeZone` | `set_timeZone` | setTimezone |
| System | PUT | `/cloud/updatePassword` | `set_password` |  |
| System | GET | `/cloud/version` | `get_version` | getVersion |
| Network | GET | `/cloud/wifiNetworks` | `get_availableWifiNetworks` | getAvailablewifinetworks |

## MQTT-only (no REST endpoint in FX90.yaml)

### Commands (5)

| MQTT command | Category |
|--------------|----------|
| `del_CACertificate` | certificate |
| `get_CACertificates` | certificate |
| `set_installCACertificate` | certificate |
| `get_nameAndDescription` | network |
| `set_nameAndDescription` | network |

### Events (13)

| MQTT event | Category |
|------------|----------|
| `async-events` | management-events |
| `error` | management-events |
| `firmwareUpdateProgress` | management-events |
| `gpi` | management-events |
| `gpo` | management-events |
| `heartbeat` | management-events |
| `userapp_event` | management-events |
| `warning` | management-events |
| `directionality_tag_data_events` | tag-data-events |
| `locationHistory` | tag-data-events |
| `mode_tag_data_events` | tag-data-events |
| `tagDataEvents` | tag-data-events |
| `zoneHistory` | tag-data-events |

## REST label aliases

FX90.yaml `description` uses alternate names; normalized to canonical MQTT commands:

| REST label in YAML | Canonical MQTT command |
|--------------------|------------------------|
| `del_certificate` | `del_certs` |
| `del_logs_radioPacketLog` | `del_radio_pkt_logs` |
| `del_logs_syslog` | `del_syslogs` |
| `get_SupportedStandardList` | `get_SupportedStandardlist` |
| `get_certificates` | `get_certs` |
| `get_gpiStatus` | `get_gpi_status` |
| `get_gpoStatus` | `get_gpostatus` |
| `get_hostName` | `get_hostname` |
| `get_logs_radioPacketLog` | `get_radio_pkt_logs` |
| `get_logs_rcLog` | `get_rc_log` |
| `get_logs_rgErrorLog` | `get_rg_error_logs` |
| `get_logs_rgWarningLog` | `get_rg_warn_logs` |
| `get_readerCapabilities` | `get_readerCapabilites` |
| `get_userapps` | `get_user_apps` |
| `localrestlogin` | `localrest_login` |
| `set_autostartUserapp` | `autostart_user_app` |
| `set_hostName` | `set_hostname` |
| `set_installUserapp` | `install_user_app` |
| `set_refreshCertificate` | `refresh-cert` |
| `set_reqToUserapp` | `set_req_usr_app` |
| `set_revertbackOS` | `revertback` |
| `set_startUserapp` | `start_user_app` |
| `set_stopUserapp` | `stop_user_app` |
| `set_uninstallUserapp` | `uninstall-user-app` |
| `set_updateCertificate` | `set_update_cert` |
