# 儀表板語言

版本 0.4.2 新增韓文與英文儀表板畫面。預設依 HA 使用者語言顯示，其他語言則回退為英文。個別卡片可設定 `language: en`、`language: ko` 或 `language: auto`。日期與星期會使用所選語言。量測值、單位、充電邏輯與已儲存的紀錄**不會**變動。預設的韓元（KRW）充電成本估算**不會**轉換為當地電價。

## 資源註冊

請將 `/carrot_ha_static/carrot-dashboard.js` 註冊為 JavaScript 模組。**不要**另外單獨註冊執行階段或語言模組。

## 原始檔結構

- `carrot-dashboard.js`：穩定的 bootstrap 與已安裝版本的查詢。
- `carrot-dashboard-runtime.js`：語言選擇與向下相容的卡片註冊。
- `carrot-dashboard-ko.js`：韓文實作。
- `carrot-dashboard-en.js`：英文實作，行為相同。

功能變更需同時修改兩個語言模組，僅可變動可見文字與地區格式。模組各自擁有獨立狀態，因此不同語言的卡片可並存。
