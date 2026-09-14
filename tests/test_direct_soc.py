import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "collector"))

from engine import Engine, Store


class DirectSocEngineTest(unittest.TestCase):
    def test_direct_soc_is_not_recalculated_and_marks_measurement_time(self):
        with tempfile.TemporaryDirectory() as directory:
            engine = Engine(Store(Path(directory) / "collector.sqlite3"), "ioniq5")
            events = engine.tick(1_800_000_000, False, sampled={
                "soc_percent": 66.0,
                "soc_source": "ovms_bms_pid_220101",
                "charging": True,
                "charge_power_w": 7450,
            })
            vehicle = events[0][1]["vehicle"]
            self.assertEqual(vehicle["soc_percent"], 66.0)
            self.assertEqual(vehicle["soc_source"], "ovms_bms_pid_220101")
            self.assertTrue(vehicle["charging"])
            self.assertEqual(vehicle["charge_power_w"], 7450)
            self.assertEqual(vehicle["measured_at"], vehicle["field_measured_at"]["soc_percent"])


if __name__ == "__main__":
    unittest.main()
