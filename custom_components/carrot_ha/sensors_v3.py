from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from .entity import VehicleEntity

FIELDS = {
 'soc_percent':('Battery SOC','battery_soc','%','mdi:battery','battery'),
 'odometer_km':('Total Odometer','total_odometer','km','mdi:counter','distance'),
 'outside_temp_c':('Outside Temperature','outside_temperature','°C','mdi:thermometer','temperature'),
 'aux_voltage':('12V Battery Voltage','aux_voltage','V','mdi:car-battery','voltage'),
 'charge_power_w':('Estimated Charging Power','estimated_charging_power','W','mdi:ev-station','power'),
 'battery_current_a':('High-Voltage Battery Current','battery_current','A','mdi:current-dc','current'),
 'battery_kwh':('Battery Stored Energy','battery_stored_energy','kWh','mdi:battery-high','energy'),
 'hv_voltage':('High-Voltage Battery Voltage','hv_voltage','V','mdi:lightning-bolt','voltage'),
 'measured_capacity_kwh':('BMS Capacity Estimate','measured_capacity','kWh','mdi:battery-heart-variant','energy'),
 'soc_capacity_kwh':('SOC Calculation Capacity','soc_capacity','kWh','mdi:battery-cog','energy'),
 'range_km':('Estimated Range','estimated_range','km','mdi:map-marker-distance','distance'),
 'blower_volt':('Blower Control Voltage','blower_voltage','V','mdi:fan','voltage'),
 'blower_level':('Blower Level','blower_level',None,'mdi:fan',None),
 'seat_heat_left':('Driver Seat Heater Level','driver_seat_heater',None,'mdi:car-seat-heater',None),
 'seat_heat_right':('Passenger Seat Heater Level','passenger_seat_heater',None,'mdi:car-seat-heater',None),
 'recirc':('Recirculation Signal','recirculation',None,'mdi:car-windshield',None),
 'speed_kph':('Current Speed','current_speed','km/h','mdi:speedometer','speed'),
 'gps_accuracy_m':('GPS Accuracy','gps_accuracy','m','mdi:crosshairs-gps','distance'),
 'bearing_deg':('Heading','heading','°','mdi:compass',None),
 'month_charge_kwh':('This Month Estimated Charge','month_charge_total','kWh','mdi:ev-station','energy'),
 'month_slow_kwh':('This Month Slow Charge','month_slow_charge','kWh','mdi:power-plug','energy'),
 'month_fast_kwh':('This Month Fast Charge','month_fast_charge','kWh','mdi:flash','energy'),
 'month_charge_cost':('This Month Estimated Cost','month_charge_cost','KRW','mdi:cash','monetary'),
 'trip_count':('Stored Trip Count','trip_count',None,'mdi:format-list-bulleted',None),
 'recorded_distance_km':('Recorded Cumulative Distance','recorded_distance','km','mdi:routes','distance'),
 'month_trip_count':('This Month Trip Count','month_trip_count',None,'mdi:calendar-check',None),
 'month_distance_km':('This Month Distance','month_distance','km','mdi:calendar-month','distance'),
 'last_trip_distance_km':('Last Trip Distance','last_trip_distance','km','mdi:map-marker-distance','distance'),
 'last_trip_duration_s':('Last Trip Duration','last_trip_duration','s','mdi:timer-outline','duration'),
 'last_trip_avg_kph':('Last Trip Average Speed','last_trip_avg_speed','km/h','mdi:speedometer-medium','speed'),
 'last_trip_max_kph':('Last Trip Max Speed','last_trip_max_speed','km/h','mdi:speedometer','speed'),
 'last_trip_at':('Last Trip End','last_trip_end',None,'mdi:clock-end','timestamp'),
 'parking_at':('Parking Position Recorded','parking_recorded_at',None,'mdi:parking','timestamp'),
 'measured_at':('Vehicle Measurement Time','measured_at',None,'mdi:clock-check-outline','timestamp'),
 'last_sync':('HA Sync Time','last_sync',None,'mdi:cloud-check','timestamp'),
 'measurement_age_s':('Vehicle Data Age','measurement_age','s','mdi:clock-alert-outline','duration'),
 'cloud_status':('Cloud Connection Status','cloud_status',None,'mdi:cloud-outline',None),
}

async def async_setup_entry(hass,entry,async_add_entities):
    async_add_entities([VehicleSensor(entry,key,*spec) for key,spec in FIELDS.items()])

class VehicleSensor(VehicleEntity,SensorEntity):
    def __init__(self,entry,key,name,translation_key,unit,icon,device_class):
        self.configure(entry,key,name,icon,translation_key)
        self._attr_native_unit_of_measurement=unit
        self._attr_device_class=device_class
        if unit is not None and device_class not in ('monetary','energy'): self._attr_state_class='measurement'
        if key in ('month_charge_kwh','month_slow_kwh','month_fast_kwh'):self._attr_state_class='total_increasing'
    @property
    def native_value(self):
        value=self.data.get(self.key)
        if self._attr_device_class=='timestamp' and value:
            try:return datetime.fromisoformat(value.replace('Z','+00:00'))
            except (ValueError,AttributeError):return None
        return value
    @property
    def extra_state_attributes(self):
        attrs=super().extra_state_attributes
        if self.key=='soc_percent':
            source=self.data.get('soc_source') or 'energy_based_calibration'
            attrs['soc_source']=source
            if source=='energy_based_calibration':
                attrs.update(nominal_net_kwh=78,nominal_gross_kwh=82,soc_capacity_kwh=self.entry.options.get('soc_capacity_kwh',78))
        return attrs
