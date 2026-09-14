# 發佈

[한국어](PUBLISH.md) | [English](PUBLISH.en.md) | 繁體中文 | [總覽](../README.zh-TW.md)

請上傳儲存庫的原始碼，**不要**上傳本機整個 outputs 目錄或您的資料庫。

## 首次發佈（維護者）

1. 以 `helico717` 帳號登入 GitHub。
2. 若儲存庫尚未建立，請選擇 + → New repository → `carrot-ha` → Public → Create repository。
3. 登入 GitHub Desktop，使用 File → Clone repository 複製儲存庫。
4. 將發佈資料夾的**內容**複製到工作複本中。`README.md`、`hacs.json`、`custom_components` 必須位於儲存庫根目錄，不可放在另一個發佈資料夾內。
5. 檢視變更檔案清單。應排除 `connection.json`、`wrangler.json`、資料庫、記錄檔、權杖，以及個人車輛圖片或路線。
6. 輸入 commit 摘要、提交至 main，然後 Push origin。
7. 若有 workflow，請檢查儲存庫 Actions 的結果，發佈前先解決失敗項。
8. 開啟 Releases → Draft a new release。使用與 `manifest.json` 對應的 tag（例如版本 `0.4.1` 對應 `v0.4.1`）。說明變更內容與未驗證的車輛支援。首次建置請以 pre-release 測試後再發佈為穩定版本。

使用者需自行將儲存庫網址加入 HACS Custom repositories。這與是否列入 HACS 預設清單是分開的。
