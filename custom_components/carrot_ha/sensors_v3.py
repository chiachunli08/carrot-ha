from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from .entity import VehicleEntity

FIELDS = {
 'soc_percent':('배터리 잔량','%','mdi:battery','battery'),
 'odometer_km':('총 주행거리','km','mdi:counter','distance'),
 'outside_temp_c':('외기 온도','°C','mdi:thermometer','temperature'),
 'aux_voltage':('12V 배터리 전압','V','mdi:car-battery','voltage'),
 'charge_power_w':('충전 전력 추정','W','mdi:ev-station','power'),
 'battery_kwh':('배터리 저장 에너지','kWh','mdi:battery-high','energy'),
 'hv_voltage':('고전압 배터리 전압','V','mdi:lightning-bolt','voltage'),
 'measured_capacity_kwh':('BMS 용량 추정','kWh','mdi:battery-heart-variant','energy'),
 'soc_capacity_kwh':('SOC 계산 용량','kWh','mdi:battery-cog','energy'),
 'range_km':('주행가능거리','km','mdi:map-marker-distance','distance'),
 'blower_volt':('송풍 제어 전압','V','mdi:fan','voltage'),
 'blower_level':('송풍 단계',None,'mdi:fan',None),
 'seat_heat_left':('운전석 열선 단계',None,'mdi:car-seat-heater',None),
 'seat_heat_right':('조수석 열선 단계',None,'mdi:car-seat-heater',None),
 'recirc':('내기순환 신호',None,'mdi:car-windshield',None),
 'speed_kph':('현재 속도','km/h','mdi:speedometer','speed'),
 'gps_accuracy_m':('GPS 정확도','m','mdi:crosshairs-gps','distance'),
 'bearing_deg':('진행 방향','°','mdi:compass',None),
 'month_charge_kwh':('이번 달 충전량 추정','kWh','mdi:ev-station','energy'),
 'month_slow_kwh':('이번 달 완속 분류 충전량','kWh','mdi:power-plug','energy'),
 'month_fast_kwh':('이번 달 급속 분류 충전량','kWh','mdi:flash','energy'),
 'month_charge_cost':('이번 달 충전요금 추정','KRW','mdi:cash','monetary'),
 'trip_count':('저장된 주행 횟수',None,'mdi:format-list-bulleted',None),
 'recorded_distance_km':('기록된 누적 거리','km','mdi:routes','distance'),
 'month_trip_count':('이번 달 주행 횟수',None,'mdi:calendar-check',None),
 'month_distance_km':('이번 달 주행거리','km','mdi:calendar-month','distance'),
 'last_trip_distance_km':('최근 주행거리','km','mdi:map-marker-distance','distance'),
 'last_trip_duration_s':('최근 주행시간','s','mdi:timer-outline','duration'),
 'last_trip_avg_kph':('최근 평균속도','km/h','mdi:speedometer-medium','speed'),
 'last_trip_max_kph':('최근 최고속도','km/h','mdi:speedometer','speed'),
 'last_trip_at':('최근 주행 종료',None,'mdi:clock-end','timestamp'),
 'parking_at':('주차 위치 기록 시각',None,'mdi:parking','timestamp'),
 'measured_at':('차량 측정 시각',None,'mdi:clock-check-outline','timestamp'),
 'last_sync':('HA 동기화 시각',None,'mdi:cloud-check','timestamp'),
 'measurement_age_s':('차량 데이터 경과시간','s','mdi:clock-alert-outline','duration'),
 'cloud_status':('클라우드 연결 상태',None,'mdi:cloud-outline',None),
}

async def async_setup_entry(hass,entry,async_add_entities):
    async_add_entities([VehicleSensor(entry,key,*spec) for key,spec in FIELDS.items()])

class VehicleSensor(VehicleEntity,SensorEntity):
    def __init__(self,entry,key,name,unit,icon,device_class):
        self.configure(entry,key,name,icon)
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
        if self.key=='soc_percent': attrs.update(nominal_net_kwh=78,nominal_gross_kwh=82,soc_capacity_kwh=self.entry.options.get('soc_capacity_kwh',78),soc_source='energy_based_calibration')
        return attrs
