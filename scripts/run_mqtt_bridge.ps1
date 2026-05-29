param(
    [int]$BackendPort = 8080,
    [string]$BrokerHost = "localhost",
    [int]$BrokerPort = 1883
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

python -m backend.telemetry.mqtt_bridge `
    --broker-host $BrokerHost `
    --broker-port $BrokerPort `
    --backend-url "http://127.0.0.1:$BackendPort" `
    --topic "devices/#"

