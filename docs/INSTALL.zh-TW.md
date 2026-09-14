# 首次安裝

[한국어](INSTALL.md) | [English](INSTALL.en.md) | 繁體中文 | [總覽](../README.zh-TW.md)

本指南假設 HA 已在執行，且您可透過 SSH 連線至 comma 裝置。Carrotpilot 必須已在車輛上正常運作。若為原廠重置的裝置，請先依其維護者說明安裝 Carrotpilot。**僅有分支名稱相同並不代表相容。**

## 1. 在 Windows PC 上準備檔案

在 GitHub 上選擇 Code → Download ZIP 並解壓縮。下列 PC 指令請於解壓縮後的 `cloudflare` 資料夾中開啟 PowerShell 執行。本說明使用 Windows 指令語法。

請從 Node.js 官方網站安裝 Windows x64 版本。檢查 `node -p "process.arch"`：若回傳 `ia32` 表示為 32 位元安裝，必須重新安裝正確版本才能繼續設定。

```powershell
npm.cmd install
.\node_modules\.bin\wrangler.cmd login
.\node_modules\.bin\wrangler.cmd d1 create id4-ha-db
.\node_modules\.bin\wrangler.cmd kv namespace create SNAPSHOTS
```

請自行建立 Cloudflare 帳號。D1 用於儲存紀錄；KV 是服務所需的輔助儲存空間。請記下回傳的 `database_id` 與 KV `id`，並填入下方的設定腳本中。內部名稱中含 `id4` 是為了相容性而保留，ID. Buzz 安裝時也會使用相同名稱。

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
.\node_modules\.bin\wrangler.cmd d1 execute id4-ha-db --remote --file .\schema.sql
.\node_modules\.bin\wrangler.cmd deploy
```

請保存部署後顯示的完整 HTTPS Worker 網址（包含您帳號的子網域）。您**不需**額外的網域或 HA 對外連接埠。請自行於 Cloudflare 查看使用限制與費用。

產生三組專屬密碼（稱為權杖）：

```powershell
node -e "const c=require('node:crypto'); for(const k of ['UPLOAD','VIEW','HA_LOCAL']) console.log(k+': '+c.randomBytes(32).toString('hex'))"
.\node_modules\.bin\wrangler.cmd secret put WAYON_UPLOAD_TOKEN
.\node_modules\.bin\wrangler.cmd secret put WAYON_VIEW_TOKEN
```

請將三組密碼妥善保存於私人密碼管理工具中。第一個 secret 提示輸入 UPLOAD 的值，第二個輸入 VIEW 的值（**不含前綴標籤**）。HA_LOCAL 用於建立 HA 整合時的初次註冊。**請勿公開這些值。**

## 2. 設定 HA

依照[總覽](../README.zh-TW.md)的 HACS 步驟安裝。裝置 ID 由您自訂（例如 `my-buzz`）；它既不是 VIN 也不是 HA 實體 ID。初次註冊使用 HA_LOCAL，選項中的讀取權杖使用 VIEW。請依您的車輛設定車型與 SOC 計算容量。

## 3. 將收集器安裝到 comma

請先將車輛停妥。使用 SSH 檔案傳輸工具（例如 WinSCP）將 `collector` 資料夾的**內容**複製到 comma 的 `/data/id4-collector`。

在 comma SSH 中，新安裝請執行：

```bash
cd /data/id4-collector
python3 configure.py
```

輸入您的 Worker 網址、與 HA 相同的裝置 ID、UPLOAD 權杖，以及車輛設定檔（`vw_meb` 或 `ioniq5`），接著執行：

```bash
PYTHONPATH="/data/openpilot/pydeps:/data/openpilot${PYTHONPATH:+:$PYTHONPATH}" /usr/local/venv/bin/python3 install.py
python3 /data/id4-collector/status.py >&2
```

安裝程式會檢查啟動腳本，並在 MEB 設定檔下檢查 DBC 結構，再註冊為自動啟動。若回報不支援的啟動檔或缺少模組，請附上分支資訊回報問題，**不要**繞過檢查。收集器為獨立程序，會額外占用記憶體。

## 4. 驗證您的 MEB 車輛

1. 停車時，比對電池、里程數、溫度讀值是否與車輛一致。讀值為空並不代表支援成功。
2. 安裝後檢查 `tail -n 30 /data/id4-collector/collector.log >&2`。
3. 正常使用後，檢查行車路線與充電紀錄。收集器僅接收資料，**不會**發送 CAN 控制指令。
4. 網路斷線後恢復時，確認 `pending` 數量減少且 delivery 變為 `ok`。comma 關機或車輛休眠期間遺失的資料**無法**還原。
5. 若需停止收集，請執行 `python3 /data/id4-collector/disable.py`。已儲存的資料與 Git 工作複本會保留。

ID. Buzz 目前尚未在實車上驗證。回報相容性時請註明出廠年份、電池規格、Carrotpilot 分支與 commit，並排除個資與權杖。

## 5. 驗證 IONIQ 5

1. 先確認 OVMS 的 IONIQ 5 模組已啟用且 BMS SOC 有更新。
2. 此模式僅在 comma 與 OVMS 能同時觀察同一條 BMC CAN 時才能使用。
3. 既有安裝請執行 `python3 /data/id4-collector/configure.py --vehicle-profile ioniq5` 並重新啟動。指令會保留原有認證資訊。
4. 執行 `python3 /data/id4-collector/status.py`，確認 `vehicle_profile` 為 `ioniq5`，且 `can_fields` 中包含 `soc_percent`。
5. 顯示的 SOC 與 OVMS 相同，是直接的 BMS SOC，**並非**由容量推導的值。

## 已知範圍

MEB SOC、充電分類與充電功率皆為估算值。IONIQ 5 SOC 是直接的 BMS 數值，但僅在 OVMS 輪詢可見時才會更新。圖表在缺資料區間可能沿用最後一次已知值，但這些沿用值**不會**納入耗電計算。目前**未啟用**自動保留期限刪除。
