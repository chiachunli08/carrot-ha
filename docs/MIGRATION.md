# 기존 기록을 유지하면서 이전하기

1. HA 전체 백업을 만드세요. `/config/carrot_ha`는 실제 주행·충전·상태 DB입니다. 이것만이 아니라 HA 설정과 엔터티 등록 정보도 포함한 전체 백업을 권합니다.
2. 기존 Carrot HA **통합 항목은 그대로 둡니다**. 삭제 후 재등록하면 통합 항목 ID가 달라져 다른 DB 파일을 사용할 수 있습니다.
3. HACS Custom repositories에 저장소를 Integration으로 추가하고 다운로드합니다. 같은 `custom_components/carrot_ha` 프로그램 폴더를 관리하도록 합니다.
4. HA를 재시작합니다. 기존 장치 ID, 통합 항목 ID, 엔터티 unique_id, DB 경로를 그대로 사용합니다.
5. 기존 대시보드 JS 리소스 한 개의 URL을 `/carrot_ha_static/carrot-dashboard.js?v=0.4.0`으로 변경합니다. 예전 JS와 새 JS를 동시에 등록하지 마세요.
6. 카드는 기존 `device_id`를 그대로 사용합니다. 원래 ID.4 사진을 유지하려면 `vehicle_image: /local/carrot-assets/id4.png`, `vehicle_name: ID.4 PRO`를 지정합니다. 새 버전에서는 특정 차량 사진을 기본 배포하지 않습니다.
7. 배터리, 누적 거리, 주행/충전 목록과 기존 그래프를 확인하세요. 실패하면 통합 삭제 대신 백업 또는 이전 프로그램 버전으로 복구합니다.

## test_id4 → id4

**장치 ID나 unique_id를 바꾸는 작업이 아닙니다.** 표시용 엔터티 ID만 HA 화면에서 변경합니다.

설정 → 기기 및 서비스 → 엔터티 → 해당 엔터티 → 설정에서 예를 들어 `sensor.test_id4_recorded_distance_km`을 `sensor.id4_recorded_distance_km`으로 수정합니다. 대상 ID가 이미 있으면 덮어쓰지 마세요. binary_sensor와 device_tracker도 같은 방식입니다.

새 대시보드는 엔터티를 unique_id로 찾기 때문에 이름을 변경해도 연결됩니다. 사용자가 만든 자동화·템플릿·다른 카드에 적힌 문자열은 별도로 변경해야 합니다. HA Recorder 이력과 장기 통계의 이름 변경 결과는 HA 버전에 따라 확인이 필요하므로, 전체 백업 후 한 엔터티로 먼저 확인하세요. Carrot HA 자체 DB는 표시용 엔터티 ID를 기준으로 저장하지 않아 이 변경으로 삭제되지 않습니다.

이 배포본은 운영 중인 HA의 엔터티 이름을 자동으로 일괄 변경하지 않습니다.
