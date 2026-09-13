# Dashboard languages / 대시보드 언어

Version 0.4.2 adds Korean and English dashboard rendering. The default follows HA's user language. Other languages fall back to English. An individual card can set language: en, language: ko, or language: auto. Dates and weekdays use the selected language. Measurements, units, charging logic and stored records are unchanged. Preset KRW cost estimates are not converted into local tariffs.

0.4.2는 HA 언어에 따라 한국어·영어 화면을 제공합니다. 카드의 language 옵션으로 고정할 수도 있습니다. 메뉴·날짜·요일·그래프·오류 안내를 번역하며 실제 데이터와 엔터티 ID는 변경하지 않습니다.

## Updating / 업데이트

See [automatic update instructions](UPDATES.md). From 0.4.3, register only `/carrot_ha_static/carrot-dashboard.js`; the installed version is selected automatically. Do not register the runtime or language modules separately.

[자동 업데이트 안내](UPDATES.md)를 참고하세요. 0.4.3부터 고정 리소스 주소 하나만 등록하면 설치 버전을 자동으로 불러옵니다. 런타임이나 언어별 JS는 별도로 등록하지 않습니다.

## Source layout

- carrot-dashboard.js: stable bootstrap and installed-version lookup.
- carrot-dashboard-runtime.js: language selection and backwards-compatible card registration.
- carrot-dashboard-ko.js: Korean implementation.
- carrot-dashboard-en.js: English implementation with the same behavior.

Maintain functional changes in both language modules. Only visible text and locale formatting should differ. The modules have separate state so cards with different languages can coexist.
