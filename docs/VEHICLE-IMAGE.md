# 차량 이미지 규격

한국어 | [English](VEHICLE-IMAGE.en.md)

일반 사진: 투명 PNG 또는 WebP 권장. 권장 캔버스 1600 × 1000 px (8:5), 최소 권장 800 × 500 px. 차량 전체(미러·타이어 포함)가 들어가도록 하고 차량 주변 여백은 각 방향 약 3~5%만 남깁니다. 정면 사진은 세로가 더 길어도 됩니다. 비율을 강제로 늘리지 마세요.

파일 픽셀 수보다 차량 주변의 빈 공간이 중요합니다. 이미지 전체를 contain으로 맞추므로 여백이 많으면 차량이 작아집니다. 데스크톱 표시 영역 높이는 250px, 모바일은 155px이며 카드 너비 안에 비율을 유지해 맞춥니다. 파일을 키워도 투명 여백 비율이 같으면 차량은 커지지 않습니다.

```yaml
type: custom:carrot-dashboard-card
device_id: my-meb
vehicle_name: ID. Buzz
vehicle_image: /local/my-car.png
```

이미지를 `/config/www/my-car.png`에 저장하세요. 장치 ID는 설치 시 정한 값으로 입력합니다.
