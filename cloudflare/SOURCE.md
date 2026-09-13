Based on https://github.com/leehyuk1108/Wayon commit 1870bfc9998e9bca6d379a3c266c5e9ce5f47a46, cloudflare/wayon-cloud.
Original D1/KV handlers and bearer upload/view authentication retained.
Changes: only telemetry/json/trips routes exposed; trip offset and include_route added; external Firebase disabled; author bindings removed.

v0.3: append-only telemetry_history with idempotent timestamps, authenticated cursor read API, reject older latest state overwrites.
