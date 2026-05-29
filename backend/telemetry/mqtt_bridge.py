import argparse
import json
import socket
import struct
from urllib.request import Request, urlopen


def route_mqtt_event(topic: str, payload: dict[str, object]) -> tuple[str, dict[str, object]] | None:
    if topic.endswith("/telemetry"):
        metrics = payload.get("metrics", {})
        if not isinstance(metrics, dict):
            return None
        return (
            "/api/telemetry/ingest",
            {
                "device_id": payload["device_id"],
                "cpu_percent": metrics["cpu_percent"],
                "memory_percent": metrics["memory_percent"],
                "temperature_celsius": metrics["temperature_celsius"],
                "uptime_seconds": metrics["uptime_seconds"],
            },
        )

    if topic.endswith("/diagnostics"):
        return (
            "/api/diagnostics/ingest",
            {
                "device_id": payload["device_id"],
                "health_state": payload["health_state"],
                "severity": payload["severity"],
                "reason_code": payload["reason_code"],
                "recommended_action": payload["recommended_action"],
            },
        )

    if topic.endswith("/recovery"):
        return (
            "/api/recovery/ingest",
            {
                "device_id": payload["device_id"],
                "action": payload["action"],
                "result": payload["result"],
                "attempt": payload["attempt"],
                "reason_code": payload["reason_code"],
            },
        )

    return None


def post_event(base_url: str, path: str, body: dict[str, object]) -> None:
    request = Request(
        f"{base_url.rstrip('/')}{path}",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=5) as response:
        response.read()


class MqttBridge:
    def __init__(self, broker_host: str, broker_port: int, backend_url: str, topic_filter: str) -> None:
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.backend_url = backend_url
        self.topic_filter = topic_filter

    def run(self) -> None:
        with socket.create_connection((self.broker_host, self.broker_port), timeout=10) as sock:
            self._send_connect(sock)
            self._expect_connack(sock)
            self._send_subscribe(sock)

            while True:
                topic, payload = self._read_publish(sock)
                routed = route_mqtt_event(topic, json.loads(payload.decode("utf-8")))
                if routed is None:
                    continue
                path, body = routed
                post_event(self.backend_url, path, body)
                print(f"forwarded {topic} -> {path}")

    def _send_connect(self, sock: socket.socket) -> None:
        variable = encode_string("MQTT") + bytes([0x04, 0x02, 0x00, 0x3C])
        payload = encode_string("backend-mqtt-bridge")
        packet = bytes([0x10]) + encode_remaining_length(len(variable) + len(payload)) + variable + payload
        sock.sendall(packet)

    def _expect_connack(self, sock: socket.socket) -> None:
        response = recv_exact(sock, 4)
        if response[0] != 0x20 or response[3] != 0x00:
            raise RuntimeError("MQTT broker rejected bridge connection")

    def _send_subscribe(self, sock: socket.socket) -> None:
        packet_id = b"\x00\x01"
        payload = encode_string(self.topic_filter) + b"\x00"
        variable = packet_id + payload
        packet = bytes([0x82]) + encode_remaining_length(len(variable)) + variable
        sock.sendall(packet)
        recv_exact(sock, 5)

    def _read_publish(self, sock: socket.socket) -> tuple[str, bytes]:
        fixed_header = recv_exact(sock, 1)[0]
        if fixed_header >> 4 != 3:
            raise RuntimeError(f"unsupported MQTT packet type {fixed_header >> 4}")
        remaining = decode_remaining_length(sock)
        packet = recv_exact(sock, remaining)
        topic_length = struct.unpack("!H", packet[:2])[0]
        topic = packet[2 : 2 + topic_length].decode("utf-8")
        payload = packet[2 + topic_length :]
        return topic, payload


def encode_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    return struct.pack("!H", len(encoded)) + encoded


def encode_remaining_length(length: int) -> bytes:
    output = bytearray()
    while True:
        encoded = length % 128
        length //= 128
        if length > 0:
            encoded |= 128
        output.append(encoded)
        if length == 0:
            return bytes(output)


def decode_remaining_length(sock: socket.socket) -> int:
    multiplier = 1
    value = 0
    while True:
        encoded = recv_exact(sock, 1)[0]
        value += (encoded & 127) * multiplier
        if (encoded & 128) == 0:
            return value
        multiplier *= 128


def recv_exact(sock: socket.socket, length: int) -> bytes:
    chunks = bytearray()
    while len(chunks) < length:
        chunk = sock.recv(length - len(chunks))
        if not chunk:
            raise RuntimeError("socket closed")
        chunks.extend(chunk)
    return bytes(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Forward MQTT device events into the backend API.")
    parser.add_argument("--broker-host", default="localhost")
    parser.add_argument("--broker-port", type=int, default=1883)
    parser.add_argument("--backend-url", default="http://127.0.0.1:8080")
    parser.add_argument("--topic", default="devices/#")
    args = parser.parse_args()

    MqttBridge(args.broker_host, args.broker_port, args.backend_url, args.topic).run()


if __name__ == "__main__":
    main()

