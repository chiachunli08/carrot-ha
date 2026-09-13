# Vehicle image requirements (0.4.1)

[한국어](VEHICLE-IMAGE.md) | English | [Overview](../README.en.md)

Use transparent PNG or WebP where possible. Recommended canvas: **1600 × 1000 px (8:5)**; recommended minimum: 800 × 500 px. Include the entire vehicle, mirrors and tires, with roughly 3–5% margin around it. Front views can use a taller aspect ratio. Do not stretch the vehicle.

Empty space matters more than pixel count. The whole image is fitted proportionally, so large transparent margins make the car look small. The image area is 250px high on desktop and 155px on mobile, constrained to the card width. Increasing resolution without reducing the relative margins will not enlarge the visible car.

For the original 4096 × 2729 ID.4 front image, add the following option. It uses the old dashboard's viewing area without modifying the image file:

```yaml
type: custom:carrot-dashboard-card
device_id: KEEP_YOUR_EXISTING_VALUE
vehicle_name: ID.4 PRO
vehicle_image: /local/carrot-assets/id4.png
vehicle_image_layout: legacy_id4
```

Replace the placeholder with your existing device ID. Omit `vehicle_image_layout` for other images: this preset is specific to the original ID.4 artwork and could crop another image incorrectly.

Maintainers: the image fix changes `custom_components/carrot_ha/frontend/carrot-dashboard.js`, `custom_components/carrot_ha/manifest.json`, and this documentation. Commit and push, then publish release `v0.4.1`. Users update through HACS, restart HA, change the resource to `/carrot_ha_static/carrot-dashboard.js?v=0.4.1`, and add the option above.
