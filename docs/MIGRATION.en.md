# Migrate without losing records

[한국어](MIGRATION.md) | English | [Overview](../README.en.md)

1. Create a full HA backup, including configuration, entity registry, and `/config/carrot_ha`, which holds trip, charge, and state records.
2. **Keep the existing Carrot HA integration entry.** Deleting and recreating it may create a new entry ID and use a different database file.
3. Add the repository to HACS as an Integration and download it. HACS manages the same `custom_components/carrot_ha` program directory.
4. Restart HA. Keep the existing device ID, integration entry ID, entity unique IDs, and DB path.
5. Edit the existing dashboard resource URL to `/carrot_ha_static/carrot-dashboard.js`. Do not load both the old and new JavaScript resources.
6. Keep the card's existing `device_id`. To retain your old ID.4 image, use `vehicle_image: /local/carrot-assets/id4.png` and `vehicle_name: ID.4 PRO`. For the original image with large margins, see the [legacy image option](VEHICLE-IMAGE.en.md).
7. Check battery readings, recorded distance, trip/charge lists, and history charts. If something fails, restore the backup or previous program version instead of deleting the integration.

## Rename test_id4 to id4

This changes the **entity ID only**, not the device ID or unique ID. In Settings → Devices & services → Entities, open the entity's settings and change, for example, `sensor.test_id4_recorded_distance_km` to `sensor.id4_recorded_distance_km`. Do not overwrite an existing target ID. The same applies to binary sensors and device trackers.

The dashboard discovers entities using their unique IDs. Update explicit old entity references in your own automations, templates, and other cards separately. Check HA Recorder history and long-term statistics after renaming one entity before proceeding with the rest. Carrot HA's own database is not keyed by these display entity IDs and is not deleted by this rename.

This release does not automatically rename existing entities.
