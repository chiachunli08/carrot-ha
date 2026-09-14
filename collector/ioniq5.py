"""Passive decoder for OVMS Hyundai IONIQ 5 BMC polling replies.

OVMS polls ECU 0x7e4 with UDS request 22 0101.  The response is an ISO-TP
message from 0x7ec.  Carrot HA only observes that existing exchange: it never
sends a CAN frame or flow-control frame of its own.
"""
from __future__ import annotations

import time

BMC_RESPONSE_ADDRESS = 0x7EC
BMC_RESPONSE_PREFIX = b"\x62\x01\x01"


def parse_bms_response(payload: bytes) -> dict:
    """Convert a reassembled 62 0101 response using the OVMS byte layout."""
    if not payload.startswith(BMC_RESPONSE_PREFIX):
        return {}
    data = payload[len(BMC_RESPONSE_PREFIX):]
    if len(data) < 14:
        return {}

    # OVMS vehicle_hyundai_ioniq5 IncomingBMC_Full(): data[4] / 2.
    soc = data[4] / 2.0
    if not 0 <= soc <= 100:
        return {}

    current_a = int.from_bytes(data[10:12], "big", signed=True) / 10.0
    voltage_v = int.from_bytes(data[12:14], "big") / 10.0
    # OVMS exposes charge power when BMS current is negative.  The collector
    # additionally suppresses this while on-road so regenerative braking is
    # not presented as a plugged-in charging session.
    charging = current_a < -0.3
    result = {
        "soc_percent": soc,
        "soc_source": "ovms_bms_pid_220101",
        "charging": charging,
        "battery_current_a": current_a,
    }
    if 100 <= voltage_v <= 1000:
        result["hv_voltage"] = round(voltage_v, 1)
        # OVMS treats negative battery current as charge current.
        result["charge_power_w"] = round(-current_a * voltage_v) if charging and current_a < 0 else 0
    return result


class Ioniq5OvmsDecoder:
    """Reassemble the standard 8-byte ISO-TP response independently per bus."""

    def __init__(self, stale_after_s: float = 2.0):
        self.stale_after_s = stale_after_s
        self._pending = {}

    def feed(self, address: int, frame: bytes, bus: int, now: float | None = None) -> dict:
        if address != BMC_RESPONSE_ADDRESS or not frame:
            return {}
        now = time.monotonic() if now is None else now
        self._pending = {
            key: value for key, value in self._pending.items()
            if now - value["at"] <= self.stale_after_s
        }
        pci_type = frame[0] >> 4

        if pci_type == 0:  # single frame
            length = frame[0] & 0x0F
            if length == 0 or length > len(frame) - 1:
                return {}
            return parse_bms_response(bytes(frame[1:1 + length]))

        if pci_type == 1:  # first frame
            if len(frame) < 2:
                return {}
            length = ((frame[0] & 0x0F) << 8) | frame[1]
            payload = bytearray(frame[2:])
            if length <= len(payload):
                return parse_bms_response(bytes(payload[:length]))
            if length > 4095 or not payload.startswith(BMC_RESPONSE_PREFIX):
                return {}
            self._pending[bus] = {"length": length, "payload": payload, "next": 1, "at": now}
            return {}

        if pci_type != 2 or bus not in self._pending:  # consecutive frame
            return {}
        pending = self._pending[bus]
        sequence = frame[0] & 0x0F
        if sequence != pending["next"]:
            self._pending.pop(bus, None)
            return {}
        pending["payload"].extend(frame[1:])
        pending["next"] = (sequence + 1) & 0x0F
        pending["at"] = now
        if len(pending["payload"]) < pending["length"]:
            return {}
        self._pending.pop(bus, None)
        return parse_bms_response(bytes(pending["payload"][:pending["length"]]))
