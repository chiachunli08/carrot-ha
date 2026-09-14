import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "collector"))

from ioniq5 import Ioniq5OvmsDecoder, parse_bms_response


def frames(payload):
    first = bytes([0x10 | (len(payload) >> 8), len(payload) & 0xFF]) + payload[:6]
    result = [first.ljust(8, b"\0")]
    sequence = 1
    for offset in range(6, len(payload), 7):
        result.append((bytes([0x20 | sequence]) + payload[offset:offset + 7]).ljust(8, b"\0"))
        sequence = (sequence + 1) & 0x0F
    return result


class Ioniq5DecoderTest(unittest.TestCase):
    def response(self, soc_raw=132):
        data = bytearray(14)
        data[4] = soc_raw
        data[10:12] = (-100).to_bytes(2, "big", signed=True)  # -10.0 A
        data[12:14] = (7450).to_bytes(2, "big")              # 745.0 V
        return b"\x62\x01\x01" + data

    def test_parses_direct_bms_soc_and_charge_power(self):
        self.assertEqual(parse_bms_response(self.response()), {
            "soc_percent": 66.0,
            "soc_source": "ovms_bms_pid_220101",
            "charging": True,
            "battery_current_a": -10.0,
            "hv_voltage": 745.0,
            "charge_power_w": 7450,
        })

    def test_reassembles_ovms_isotp_response(self):
        decoder = Ioniq5OvmsDecoder()
        result = {}
        for frame in frames(self.response()):
            result = decoder.feed(0x7EC, frame, bus=1, now=1.0) or result
        self.assertEqual(result["soc_percent"], 66.0)

    def test_rejects_invalid_soc_and_broken_sequence(self):
        self.assertEqual(parse_bms_response(self.response(soc_raw=255)), {})
        decoder = Ioniq5OvmsDecoder()
        parts = frames(self.response())
        self.assertEqual(decoder.feed(0x7EC, parts[0], 0, now=1.0), {})
        broken = bytes([0x22]) + parts[1][1:]
        self.assertEqual(decoder.feed(0x7EC, broken, 0, now=1.1), {})
        self.assertEqual(decoder.feed(0x7EC, parts[1], 0, now=1.2), {})


if __name__ == "__main__":
    unittest.main()
