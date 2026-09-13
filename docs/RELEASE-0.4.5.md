# 0.4.5

HA 시작 시 버전 정보를 읽으며 발생하던 `read_text` / `open` blocking call 경고를 수정했습니다. 파일 열기와 읽기 전체를 HA의 별도 작업 스레드에서 처리합니다. 버전 조회 API는 시작 시 읽은 값을 재사용합니다.

HACS 업데이트 후 HA를 재시작하고 대시보드를 새로고침하세요. 리소스 주소와 카드 설정은 그대로 사용하며 기존 기록에는 변경이 없습니다.

Fixed the blocking `read_text` / `open` warning during integration startup. The complete manifest read now runs in HA's executor. Version requests reuse the value loaded at startup.

Update through HACS, restart Home Assistant, and reload the dashboard. No resource URL or card configuration changes are required. Existing records are unchanged.
