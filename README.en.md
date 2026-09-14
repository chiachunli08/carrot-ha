# Carrot HA — Volkswagen MEB / Hyundai IONIQ 5

[한국어](README.md) | English

Collect vehicle data on a comma device running Carrotpilot, store it in your own Cloudflare account, and view it in Home Assistant (HA). Features include trip routes, battery state of charge (SOC), estimated charging records, and a seven-day battery history chart. Remote vehicle control is not supported.

The project provides the MEB implementation used on an ID.4 plus an IONIQ 5 profile that observes an existing OVMS polling session. **ID. Buzz and other MEB models, and all Carrotpilot branches, have not been validated.** Home Assistant 2026.3 or later is required. The dashboard API currently requires an HA administrator account.

## Installation

1. Follow the [installation guide](docs/INSTALL.en.md) to prepare your Cloudflare service and comma collector.
2. In HACS, open the menu → Custom repositories. Add `https://github.com/helico717/carrot-ha` with type **Integration**.
3. Download Carrot HA and restart HA.
4. Open Settings → Devices & services → Add integration → Carrot HA. Enter your chosen device ID and dedicated token.
5. In the integration options, enter the Worker URL, read token, vehicle model, and SOC calculation capacity. The capacity setting is used only for energy-derived MEB SOC, not the IONIQ 5 direct BMS SOC.
6. Add `/carrot_ha_static/carrot-dashboard.js` as a **JavaScript module** dashboard resource.
7. Add a manual card using the same device ID as the collector and integration:

```yaml
type: custom:carrot-dashboard-card
device_id: my-meb
vehicle_name: ID. Buzz
# If you placed your own vehicle image in HA /config/www/:
# vehicle_image: /local/my-car.png
```

The default image is the Carrot HA icon. Use an image you have permission to use. See [image requirements](docs/VEHICLE-IMAGE.en.md). Vehicle entities are discovered automatically; their names do not need to start with `test_id4`. You can override them with `charging_entity` and `online_entity` in the card configuration.

**Dashboard language:** follows the HA user language (Korean → Korean; other languages → English). Set `language: en` or `language: ko` in the card to override it. `language: auto` follows HA. Entity names outside the dashboard are unchanged. SOC means battery state of charge. Charging power and classification remain estimates.

```yaml
type: custom:carrot-dashboard-card
device_id: my-meb
language: en
```


## Other MEB vehicles

- Start with Carrotpilot already working on your vehicle.
- The `vw_meb` DBC (the definitions used to interpret CAN messages) and the required messages must be available. Installer checks do not prove that the readings are correct on your vehicle.
- While parked, compare SOC, odometer, and outside temperature with the vehicle. Check trip and charging records after normal use.
- Do not assume an ID. Buzz has the same battery capacity as an ID.4. Configure the SOC calculation capacity for your vehicle.
- Charging power is estimated from battery energy increases, not read from the charger's meter. Slow/fast charging classification is also an estimate.
- Collected but unsent records are retried after connectivity returns. Periods without power or CAN data cannot be reconstructed.
- Some calculations and labels remain Korea-oriented, including charging cost estimates in KRW. Do not treat them as local electricity bills.

## Hyundai IONIQ 5

- The comma device and OVMS must both be able to observe the same BMC CAN, and the OVMS IONIQ 5 module must periodically poll `22 0101`.
- Select `ioniq5` as the vehicle profile in `configure.py`. The collector passively reassembles OVMS's `0x7EC` ISO-TP response and never transmits a CAN frame.
- For an existing collector, run `python3 /data/id4-collector/configure.py --vehicle-profile ioniq5` and reboot; credentials are preserved.
- SOC uses the same direct 0.5%-resolution BMS SOC byte as OVMS. It is not recalculated from battery capacity.
- BMS current, voltage, and instantaneous charge power are exposed when present. Energy-derived charge totals and charge-session records require an energy counter and are not generated for this profile.
- If the OVMS response is not visible on Carrotpilot's `can` service, SOC will not update. After installation, confirm that `status.py` lists `soc_percent` in `can_fields`.

## Privacy

Each user runs their own Cloudflare service. Never upload tokens, databases, routes, logs, or connection settings to this repository. The project does not provide a shared server collecting users' vehicle data.

## Credits

Cloudflare and CAN reference code: [source information](cloudflare/SOURCE.md), [Cloudflare license](cloudflare/LICENSE.upstream), [collector reference license](collector/LICENSE.reference), [OVMS reference license](collector/LICENSE.ovms-reference).
Maps use Leaflet and OpenStreetMap; keep map attribution visible. The project owner supplied the brand image. This is not an official or certified Carrotpilot, Volkswagen, or Home Assistant product.

Maintainers: see [publishing and releases](docs/PUBLISH.en.md).
