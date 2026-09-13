"""Display calibration; does not claim to measure battery SOH."""
import math

NET_CAPACITY_KWH = 78.0
GROSS_CAPACITY_KWH = 82.0

def calibrated_soc(energy_wh, capacity_kwh):
    if type(energy_wh) not in (float, int) or type(capacity_kwh) not in (float, int):
        return None
    if not math.isfinite(energy_wh) or not math.isfinite(capacity_kwh) or energy_wh < 0 or not 20 <= capacity_kwh <= 150:
        return None
    return round(min(100, energy_wh / (capacity_kwh * 1000) * 100), 1)
