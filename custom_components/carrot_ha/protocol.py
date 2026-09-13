"""Versioned, bounded telemetry envelopes. No Home Assistant dependency."""
import json
from datetime import datetime, timezone

MAX_BYTES = 262144

def validate(data):
    if not isinstance(data, dict) or type(data.get('schema')) is not int or data.get('schema') != 1:
        raise ValueError('Unsupported schema')
    for key in ('event_id', 'device_id'):
        if not isinstance(data.get(key), str) or not 1 <= len(data[key]) <= 128:
            raise ValueError('Invalid identity')
    if data.get('kind') not in ('state', 'trip', 'charge'):
        raise ValueError('Invalid kind')
    if not isinstance(data.get('observed_at'), str):
        raise ValueError('Timestamp required')
    stamp = datetime.fromisoformat(data['observed_at'].replace('Z', '+00:00'))
    if stamp.tzinfo is None:
        raise ValueError('Timezone required')
    if not isinstance(data.get('data'), dict):
        raise ValueError('Object payload required')
    bounds = {'soc_percent': (0, 100), 'odometer_km': (0, 1048573),
              'outside_temp_c': (-80, 80), 'aux_voltage': (0, 30),
              'charge_power_w': (0, 500000), 'latitude': (-90, 90),
              'longitude': (-180, 180), 'duration_s': (0, 31536000),
              'distance_m': (0, 100000000), 'energy_kwh': (0, 1000)}
    for key, (low, high) in bounds.items():
        value = data['data'].get(key)
        if value is not None and (type(value) not in (int, float) or not low <= value <= high):
            raise ValueError('Invalid measurement: ' + key)
    encoded = json.dumps(data, allow_nan=False, sort_keys=True, separators=(',', ':'))
    if len(encoded.encode()) > MAX_BYTES:
        raise ValueError('Payload too large')
    return encoded
