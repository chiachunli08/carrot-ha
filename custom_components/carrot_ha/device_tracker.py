from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.components.device_tracker import SourceType
from .entity import VehicleEntity

async def async_setup_entry(hass,entry,async_add_entities):
    async_add_entities([Position(entry,False),Position(entry,True)])

class Position(VehicleEntity,TrackerEntity):
    def __init__(self,entry,parked):
        self.parked=parked
        self.configure(entry,'parking_position' if parked else 'vehicle_position','주차 위치' if parked else '차량 위치','mdi:parking' if parked else 'mdi:car-connected')
    @property
    def source_type(self):return SourceType.GPS
    @property
    def latitude(self):return self.data.get('parking_latitude' if self.parked else 'latitude')
    @property
    def longitude(self):return self.data.get('parking_longitude' if self.parked else 'longitude')
    @property
    def location_accuracy(self):return self.data.get('gps_accuracy_m') or 0
