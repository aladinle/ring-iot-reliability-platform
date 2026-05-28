Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

docker compose -f .\docker\docker-compose.yml up mqtt-broker

