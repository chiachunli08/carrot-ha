# 0.4.8

Hyundai IONIQ 5 프로필을 추가했습니다. 콤마와 OVMS가 같은 BMC CAN을 볼 수 있는 구성에서 OVMS의 기존 `22 0101` 폴링 응답(`0x7EC`)을 읽기 전용으로 재조립하고 BMS SOC를 직접 표시합니다. IONIQ 5 SOC에는 용량 보정을 적용하지 않습니다. 실차에서는 설치 후 `status.py`의 `can_fields`에 `soc_percent`가 표시되는지 확인해야 합니다.

Added the Hyundai IONIQ 5 profile. When comma and OVMS can see the same BMC CAN, the collector passively reassembles OVMS's existing `22 0101` response (`0x7EC`) and uses its direct BMS SOC without capacity calibration. Confirm `soc_percent` appears in `status.py` → `can_fields` on the vehicle.
