# Dashboard languages / 대시보드 언어

Version 0.4.2 adds Korean and English dashboard rendering. The default follows HA's user language. Other languages fall back to English. An individual card can set language: en, language: ko, or language: auto. Dates and weekdays use the selected language. Measurements, units, charging logic and stored records are unchanged. Preset KRW cost estimates are not converted into local tariffs.

0.4.2는 HA 언어에 따라 한국어·영어 화면을 제공합니다. 카드의 language 옵션으로 고정할 수도 있습니다. 메뉴·날짜·요일·그래프·오류 안내를 번역하며 실제 데이터와 엔터티 ID는 변경하지 않습니다.

## Resource setup / 리소스 등록

Register `/carrot_ha_static/carrot-dashboard.js` as a JavaScript module. Do not register the runtime or language modules separately.

`/carrot_ha_static/carrot-dashboard.js`를 JavaScript 모듈로 등록하세요. 런타임과 언어별 파일은 별도로 등록하지 않습니다.

## Source layout

- carrot-dashboard.js: stable bootstrap and installed-version lookup.
- carrot-dashboard-runtime.js: language selection and backwards-compatible card registration.
- carrot-dashboard-ko.js: Korean implementation.
- carrot-dashboard-en.js: English implementation with the same behavior.

Maintain functional changes in both language modules. Only visible text and locale formatting should differ. The modules have separate state so cards with different languages can coexist.
