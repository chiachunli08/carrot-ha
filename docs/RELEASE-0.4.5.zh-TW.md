# 0.4.5

修正了整合啟動時讀取版本資訊所引發的 `read_text` / `open` blocking call 警告。整個 manifest 讀取流程現在於 HA 的 executor 執行緒中處理。版本查詢 API 會重用啟動時已讀入的值。

Fixed the blocking `read_text` / `open` warning during integration startup. The complete manifest read now runs in HA's executor. Version requests reuse the value loaded at startup.
