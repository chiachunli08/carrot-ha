# 0.4.8

新增 Hyundai IONIQ 5 設定檔。在 comma 與 OVMS 能同時觀察同一條 BMC CAN 的環境下，收集器以**唯讀**方式重組 OVMS 既有的 `22 0101` 輪詢回應（`0x7EC`），並直接使用其 BMS SOC，不進行容量校正。實車上請於安裝後確認 `status.py` → `can_fields` 中有顯示 `soc_percent`。

Added the Hyundai IONIQ 5 profile. When comma and OVMS can see the same BMC CAN, the collector passively reassembles OVMS's existing `22 0101` response (`0x7EC`) and uses its direct BMS SOC without capacity calibration. Confirm `soc_percent` appears in `status.py` → `can_fields` on the vehicle.
