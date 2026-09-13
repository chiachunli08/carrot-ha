# Dashboard languages / 대시보드 언어

Version 0.4.2 adds Korean and English dashboard rendering. The default follows HA's user language. Other languages fall back to English. An individual card can set language: en, language: ko, or language: auto. Dates and weekdays use the selected language. Measurements, units, charging logic and stored records are unchanged. Preset KRW cost estimates are not converted into local tariffs.

0.4.2는 HA 언어에 따라 한국어·영어 화면을 제공합니다. 카드의 language 옵션으로 고정할 수도 있습니다. 메뉴·날짜·요일·그래프·오류 안내를 번역하며 실제 데이터와 엔터티 ID는 변경하지 않습니다.

## Updating / 업데이트

Commit and push all three frontend JS files, manifest.json, and the documentation. Publish v0.4.2. Install the HACS update, restart HA, then change the existing resource URL to /carrot_ha_static/carrot-dashboard.js?v=0.4.2. Do not register the language modules separately.

GitHub Desktop에서 변경된 JS 3개와 manifest.json, 문서를 함께 Commit/Push하고 v0.4.2 릴리스를 발행합니다. HACS 업데이트 후 HA 재시작, 기존 리소스의 v 값을 0.4.2로 변경하세요. 언어별 JS를 별도 리소스로 추가하지 마세요.

## Source layout

- carrot-dashboard.js: language selection and backwards-compatible card registration.
- carrot-dashboard-ko.js: Korean implementation.
- carrot-dashboard-en.js: English implementation with the same behavior.

Maintain functional changes in both language modules. Only visible text and locale formatting should differ. The modules have separate state so cards with different languages can coexist.
