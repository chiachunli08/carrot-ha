# Automatic frontend version loading — 0.4.3

## 한국어

이번 한 번만 HACS 0.4.3 업데이트 후 HA를 재시작하고 기존 리소스 주소를 아래로 변경하세요. 새 리소스를 추가하지 않습니다.

`/carrot_ha_static/carrot-dashboard.js`

그다음부터는 HACS 업데이트 → HA 재시작 → 앱 또는 페이지 다시 열기로 충분합니다. 이미 열려 있는 화면을 실시간으로 교체하지는 않습니다. 앱이 화면을 계속 유지하면 페이지를 새로고침하세요.

고정 로더가 캐시 없이 설치 버전을 조회하고, 런타임·한국어·영어 모듈에 같은 버전 번호를 붙여 불러옵니다. 차량 데이터와 DB에는 변경이 없습니다. 버전 조회 실패 시 이전 버전을 조용히 표시하지 않고 로딩 오류를 냅니다. HA를 재시작하고 페이지를 다시 여세요.

## English

After installing 0.4.3 through HACS, restart HA and change the existing resource URL once to `/carrot_ha_static/carrot-dashboard.js`. Do not add a duplicate resource.

For subsequent releases: update through HACS, restart HA, and reload the dashboard. This does not hot-swap code in an already open page. The bootstrap fetches the installed version without caching and imports the runtime and both language modules with matching version URLs. Vehicle data and storage are unchanged. A failed version check raises a loading error rather than silently using an old release.

## Maintainers

Increase manifest.json version for every frontend release, commit all changed files, and publish the corresponding GitHub Release. There is no separate frontend version file to maintain. HACS still does not update comma or Cloudflare.
