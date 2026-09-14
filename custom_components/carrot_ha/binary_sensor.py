from homeassistant.components.binary_sensor import BinarySensorEntity
from .entity import VehicleEntity
from .connectivity import connection_status
from datetime import timedelta
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_time_interval

FLAGS = [
    ('onroad','On Road','on_road','mdi:car'),
    ('charging','Estimated Charging','estimated_charging','mdi:ev-station'),
    ('ac_on','Air Conditioner On','ac_on','mdi:snowflake'),
    ('stale','Vehicle Data Stale','stale','mdi:clock-alert'),
    ('enabled','Driver Assist Active','driver_assist','mdi:steering'),
]

async def async_setup_entry(hass,entry,async_add_entities):
    async_add_entities([Flag(entry,*spec) for spec in FLAGS])
    async_add_entities([CommaConnection(entry)])

class CommaConnection(VehicleEntity, BinarySensorEntity):
    _attr_device_class = 'connectivity'

    def __init__(self, entry):
        self.configure(entry, 'comma_online', 'Comma Connection Status', 'mdi:access-point-network', 'comma_connection')

    @property
    def is_on(self):
        return connection_status(self.runtime)['online']

    @property
    def extra_state_attributes(self):
        state = connection_status(self.runtime)
        return {key: value for key, value in state.items() if key != 'online'}

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        @callback
        def refresh(now):
            self.async_write_ha_state()
        self.async_on_remove(async_track_time_interval(self.hass, refresh, timedelta(seconds=30)))

class Flag(VehicleEntity,BinarySensorEntity):
    def __init__(self,entry,key,name,translation_key,icon):self.configure(entry,key,name,icon,translation_key)
    @property
    def is_on(self):
        value=self.data.get(self.key)
        return None if value is None else bool(value)
