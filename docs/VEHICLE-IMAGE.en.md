# Vehicle image requirements

[한국어](VEHICLE-IMAGE.md) | English | [繁體中文](VEHICLE-IMAGE.zh-TW.md) | [Overview](../README.en.md)

Use transparent PNG or WebP where possible. Recommended canvas: **1600 × 1000 px (8:5)**; recommended minimum: 800 × 500 px. Include the entire vehicle, mirrors and tires, with roughly 3–5% margin around it. Front views can use a taller aspect ratio. Do not stretch the vehicle.

Empty space matters more than pixel count. The whole image is fitted proportionally, so large transparent margins make the car look small. The image area is 250px high on desktop and 155px on mobile, constrained to the card width. Increasing resolution without reducing the relative margins will not enlarge the visible car.

```yaml
type: custom:carrot-dashboard-card
device_id: my-meb
vehicle_name: ID. Buzz
vehicle_image: /local/my-car.png
```

Save the image as `/config/www/my-car.png`. Use the device ID chosen during installation.
