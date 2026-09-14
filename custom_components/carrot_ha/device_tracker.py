from homeassistant.components.device_tracker import TrackerEntity
from homeassistant.components.device_tracker import SourceType
from .entity import VehicleEntity

async def async_setup_entry(hass,entry,async_add_entities):
    async_add_entities([Position(entry,False),Position(entry,True)])

class Position(VehicleEntity,TrackerEntity):
    def __init__(self,entry,parked):
        self.parked=parked
        if parked:
            self.configure(entry,'parking_position','Parking Position','mdi:parking','parking_position')
        else:
            self.configure(entry,'vehicle_position','Vehicle Position','mdi:car-connected','vehicle_position')
    @property
    def source_type(self):return SourceType.GPS
    @property
    def latitude(self):return self.data.get('parking_latitude' if self.parked else 'latitude')
    @property
    def longitude(self):return self.data.get('parking_longitude' if self.parked else 'longitude')
    @property
    def location_accuracy(self):return self.data.get('gps_accuracy_m') or 0
