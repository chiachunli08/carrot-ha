# 차량 이미지 규격 (0.4.1)

일반 사진: 투명 PNG 또는 WebP 권장. 권장 캔버스 1600 × 1000 px (8:5), 최소 권장 800 × 500 px. 차량 전체(미러·타이어 포함)가 들어가도록 하고 차량 주변 여백은 각 방향 약 3~5%만 남깁니다. 정면 사진은 세로가 더 길어도 됩니다. 비율을 강제로 늘리지 마세요.

파일 픽셀 수보다 차량 주변의 빈 공간이 중요합니다. 이미지 전체를 contain으로 맞추므로 여백이 많으면 차량이 작아집니다. 데스크톱 표시 영역 높이는 250px, 모바일은 155px이며 카드 너비 안에 비율을 유지해 맞춥니다. 파일을 키워도 투명 여백 비율이 같으면 차량은 커지지 않습니다.

기존 4096 × 2729 ID.4 정면 이미지를 계속 쓰는 경우 아래 옵션을 추가합니다. 이전 대시보드와 같은 표시 영역을 사용하며 원본 파일은 수정하지 않습니다.

```yaml
type: custom:carrot-dashboard-card
device_id: 기존값을_유지
vehicle_name: ID.4 PRO
vehicle_image: /local/carrot-assets/id4.png
vehicle_image_layout: legacy_id4
```

다른 차량 사진은 vehicle_image_layout 줄을 생략하세요. 이 프리셋은 기존 ID.4 원본 전용이라 다른 사진에 적용하면 잘릴 수 있습니다.

GitHub 수정 파일: custom_components/carrot_ha/frontend/carrot-dashboard.js, custom_components/carrot_ha/manifest.json, 이 안내 문서.
Commit/Push 후 Release v0.4.1을 발행합니다. HACS 업데이트 후 HA 재시작, 기존 리소스를 /carrot_ha_static/carrot-dashboard.js?v=0.4.1 로 바꾸고 카드에 위 옵션을 추가합니다.
