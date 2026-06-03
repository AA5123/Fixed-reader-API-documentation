Query reader version, health, and capabilities, manage configuration import/export, and perform system-level operations such as reboot, passthrough, and password changes. Some of these actions interrupt normal operation, so schedule them carefully to minimize downtime.

| Command | Description |
|---|---|
| [get_version](#op-get-version) | Retrieve firmware and component version information |
| [get_status](#op-get-status) | Retrieve the current reader health and operational status |
| [reboot](#op-reboot) | Restart the device and apply pending configuration changes |
| [get_readerCapabilites](#op-get-readercapabilites) | Retrieve the reader's supported capabilities and limits |
| [get_config](#op-get-config) | Export the reader's current configuration |
| [set_config](#op-set-config) | Apply a configuration to the reader |
| [set_importCloudConfig](#op-set-importcloudconfig) | Import a reader configuration from the cloud |
| [set_cableLossCompensation](#op-set-cablelosscompensation) | Set antenna cable loss compensation values |
| [get_cableLossCompensation](#op-get-cablelosscompensation) | Retrieve antenna cable loss compensation values |
| [set_passthru](#op-set-passthru) | Send a raw passthrough command to the radio |
| [set_password](#op-set-password) | Change the reader account password |
