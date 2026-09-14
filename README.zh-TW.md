# Carrot HA — Volkswagen MEB / Hyundai IONIQ 5

[한국어](README.md) | [English](README.en.md) | 繁體中文

在執行 Carrotpilot 的 comma 裝置上收集車輛資料，存入您自己的 Cloudflare 帳號，並透過 Home Assistant（以下簡稱 HA）查看。功能包含行車路線、電池剩餘電量（SOC）、充電估算紀錄，以及近七日電池歷史圖表。**不提供車輛遠端控制功能。**

本專案提供 ID.4 上使用的 MEB 實作，以及共用同一 OVMS 輪詢流程的 IONIQ 5 設定檔。**ID. Buzz 與其他 MEB 車型、所有 Carrotpilot 分支均未經驗證。** 需要 Home Assistant 2026.3 以上版本。目前儀表板 API 僅限 HA 管理員帳號使用。

## 安裝步驟

1. 依照[安裝指南](docs/INSTALL.zh-TW.md)準備您的 Cloudflare 服務與 comma 上的收集器。
2. 在 HACS 中，開啟右上選單 → Custom repositories，加入 `https://github.com/helico717/carrot-ha`，類型選 **Integration**。
3. 下載 Carrot HA 後重新啟動 HA。
4. 進入 設定 → 裝置與服務 → 加入整合 → Carrot HA，輸入您自訂的裝置 ID 與專屬權杖。
5. 在整合選項中輸入 Worker 網址、讀取權杖、車輛型號與 SOC 計算容量。SOC 計算容量僅用於 MEB 能量推導的 SOC，**不會**套用於 IONIQ 5 直接讀取的 BMS SOC。
6. 將 `/carrot_ha_static/carrot-dashboard.js` 以 **JavaScript 模組** 方式加入儀表板資源。
7. 加入一張手動卡片，使用與收集器、整合相同的裝置 ID：

```yaml
type: custom:carrot-dashboard-card
device_id: my-meb
vehicle_name: ID. Buzz
# 若您有將自己的車輛圖片放到 HA /config/www/：
# vehicle_image: /local/my-car.png
```

預設圖示為 Carrot HA 圖示。請使用您有權使用的圖片，參考[車輛圖片規格](docs/VEHICLE-IMAGE.zh-TW.md)。車輛狀態的實體會自動偵測，不一定要以 `test_id4` 開頭。如有需要，可在卡片設定中以 `charging_entity`、`online_entity` 明確指定。

**儀表板語言：** 依 HA 使用者語言顯示（韓文 → 韓文；其他語言 → 英文）。可在卡片設定中以 `language: en` 或 `language: ko` 強制指定，`language: auto` 表示依 HA 設定。儀表板以外的實體名稱不會被修改。SOC 表示電池剩餘電量百分比。充電功率與分類仍為估算值。

```yaml
type: custom:carrot-dashboard-card
device_id: my-meb
language: en
```

## 其他 MEB 車輛

- 請先確認 Carrotpilot 已在您的車輛上正常運作。
- 必須具備 `vw_meb` DBC（用於解讀 CAN 訊息的定義檔）以及收集器所需的訊息。安裝程式只會檢查格式，**不會**驗證實車數值的正確性。
- 在停車狀態下，比對 SOC、總里程數與車外溫度是否與車輛實際顯示一致。正常使用後檢查行車與充電紀錄。
- 請勿預設 ID. Buzz 與 ID.4 有相同的電池容量，請依您的車輛設定 SOC 計算容量。
- 充電功率是依據電池能量增量估算，並非從充電樁電表讀取；慢充／快充的分類同樣為估算值。
- 收集但尚未上傳的紀錄會在網路恢復後自動重傳。但斷電或無 CAN 資料的區間無法重建。
- 部分計算與標籤仍以韓國為導向，包含以韓元（KRW）估算的充電成本，請勿將其視為當地的電費帳單。

## Hyundai IONIQ 5

- comma 與 OVMS 必須能同時觀察同一條 BMC CAN，且 OVMS 的 IONIQ 5 模組必須定期輪詢 `22 0101`。
- 在 `configure.py` 中選擇 `ioniq5` 作為車輛設定檔。收集器會被動地重組 OVMS 的 `0x7EC` ISO-TP 回應，且不會發送任何 CAN 訊框。
- 若為既有安裝，請執行 `python3 /data/id4-collector/configure.py --vehicle-profile ioniq5` 並重新啟動；原有認證資訊會保留。
- SOC 直接使用與 OVMS 相同的 0.5% 解析度 BMS SOC 位元組，**不會**依電池容量重新計算。
- BMS 電流、電壓與瞬時充電功率若包含在回應中會一併顯示。需要能量計數器的累計充電量與充電階段紀錄，**不會**在此設定檔中產生。
- 若 OVMS 輪詢回應在 Carrotpilot 的 `can` 服務中看不到，SOC 將不會更新。安裝後請確認 `status.py` 的 `can_fields` 中有列出 `soc_percent`。

## 隱私

每位使用者皆使用自己的 Cloudflare 帳號／服務。請勿將權杖、資料庫、行車路線、記錄檔、連線設定上傳至此儲存庫。本專案並未提供蒐集使用者車輛資料的共用伺服器。

## 來源致謝

Cloudflare 與 CAN 參考程式碼：[來源說明](cloudflare/SOURCE.md)、[Cloudflare 授權](cloudflare/LICENSE.upstream)、[收集器參考授權](collector/LICENSE.reference)、[OVMS 參考授權](collector/LICENSE.ovms-reference)。

地圖使用 Leaflet 與 OpenStreetMap，請保留地圖來源標示。品牌圖片由專案擁有者提供。本專案並非 Carrotpilot、Volkswagen 或 Home Assistant 的官方產品或官方認證整合。

維護者請參考[發佈與版本說明](docs/PUBLISH.zh-TW.md)。
