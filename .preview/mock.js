// Mocked Carrot HA API data for the local preview (Korean dashboard)
function buildHistoryDay(date, used, hours, chargeHours) {
  return { date, used, hours, charge_hours: chargeHours || {}, received_samples: 24, valid_samples: 20, stale_samples: 2, covered_s: 81000, drive_s: 2400, charge_s: 28800 };
}

function makeHours(socs, opts) {
  const hours = socs.map((v, h) => {
    const o = opts && opts[h] ? opts[h] : {};
    const x = { soc: v };
    if (o.last_known) x.last_known = true;
    if (o.driving) x.driving = true;
    return x;
  });
  return hours;
}

const lastDayHours = makeHours(
  [42,45,50,57,63,70, 68,66,63,61,64,66, 68,69,70,71,71,71, 70,75,82,90,92,92],
  { 5:{last_known:true}, 6:{driving:true}, 7:{last_known:true}, 8:{last_known:true}, 9:{last_known:true}, 15:{last_known:true}, 16:{last_known:true}, 17:{last_known:true}, 18:{last_known:true} }
);

const battery_history = [
  buildHistoryDay('2026-09-08', 12, makeHours([80,80,80,80,80,78,72,70,69,68,68,67,66,66,65,64,64,63,63,62,62,62,61,61])),
  buildHistoryDay('2026-09-09', 22, makeHours([61,61,60,58,55,58,70,68,66,64,63,62,61,61,60,60,59,58,58,57,57,56,56,55])),
  buildHistoryDay('2026-09-10', 8,  makeHours([55,55,54,54,53,53,52,52,52,51,51,50,50,50,50,49,49,49,48,48,48,48,48,48])),
  buildHistoryDay('2026-09-11', 18, makeHours([48,48,47,45,44,46,60,58,56,54,53,52,51,51,50,50,49,49,48,48,47,47,46,46])),
  buildHistoryDay('2026-09-12', 31, makeHours([46,45,42,40,42,55,68,66,64,62,60,58,56,55,54,53,52,51,50,50,49,48,47,46])),
  buildHistoryDay('2026-09-13', 15, makeHours([46,46,45,44,43,45,58,56,55,54,53,52,52,51,51,50,50,49,49,48,48,47,47,46])),
  buildHistoryDay('2026-09-14', 25, lastDayHours, { 0:true,1:true,2:true,3:true,4:true, 10:true, 19:true,20:true,21:true }),
];

const dashValues = {
  vehicle_model: 'VW ID.4 Lounge',
  battery_history,
  soc_percent: 92,
  battery_kwh: 70.8,
  soc_capacity_kwh: 77,
  odometer_km: 12345,
  month_distance_km: 482,
  month_trip_count: 22,
  charge_power_w: null,
  charging: true,
  onroad: false,
  month_charge_kwh: 322.4,
  month_slow_kwh: 286.1,
  month_fast_kwh: 36.3,
  month_charge_cost: 61400,
  parking_latitude: 37.5665,
  parking_longitude: 126.978,
  parking_at: '2026-09-14T08:30:00+09:00',
  cloud_status: '연결됨',
  last_sync: '2026-09-14T00:45:00+09:00',
  measured_at: '2026-09-14T00:44:00+09:00',
  outside_temp_c: 24,
  aux_voltage: 12.4,
  ac_on: false,
  blower_level: 0,
  range_km: 438,
  hv_voltage: 392,
  entity_ids: { charging: 'switch.charger', comma_online: 'binary_sensor.comma_online' }
};

const tripEvents = [{
  data: {
    started_at: '2026-09-14T06:02:00+09:00',
    ended_at: '2026-09-14T06:42:00+09:00',
    duration_s: 2400,
    distance_m: 18500,
    route: []
  }
}];

const chargeEvents = [
  { data: { started_at: '2026-09-14T00:05:00+09:00', duration_s: 18000, energy_kwh: 25.3, partial: false } },
  { data: { started_at: '2026-09-13T19:02:00+09:00', duration_s: 10800, energy_kwh: 11.2, partial: false } }
];

window.CARROT_MOCK = {
  chargeHoursLabel: '0–4시, 10시, 19–21시 충전 기록',
  callApi(method, path) {
    if (path.includes('/v1/devices')) return Promise.resolve({ devices: [{ device_id: 'demo', entry_id: 'demo-entry', name: 'ID.4' }] });
    if (path.includes('/v1/dashboard/')) return Promise.resolve({ values: dashValues });
    if (path.includes('kind=trip')) return Promise.resolve({ events: tripEvents });
    if (path.includes('kind=charge')) return Promise.resolve({ events: chargeEvents });
    return Promise.resolve({ values: {}, events: [] });
  },
  states: {
    'switch.charger': { state: 'on' },
    'binary_sensor.comma_online': { state: 'on' }
  },
  themes: { darkMode: false }
};
