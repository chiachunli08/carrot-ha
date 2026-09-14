# 車輛圖片規格

[한국어](VEHICLE-IMAGE.md) | [English](VEHICLE-IMAGE.en.md) | 繁體中文 | [總覽](../README.zh-TW.md)

請盡量使用透明背景的 PNG 或 WebP。建議畫布：**1600 × 1000 px（8:5）**；建議最小尺寸：800 × 500 px。圖片中需包含車輛完整外觀（含後照鏡與輪胎），四周保留約 3～5% 的邊距。正面視角可使用更直立的長寬比。請勿將車輛拉伸變形。

相較於像素數，**車輛周圍的留白**更為重要。整張圖片會以 contain 等比縮放，因此透明邊距過大會使車輛顯得較小。圖片區域在桌面版高度為 250 px、行動版為 155 px，並維持卡片寬度內的比例。即使提高解析度，若相對邊距不變，車輛的視覺大小**不會**放大。

```yaml
type: custom:carrot-dashboard-card
device_id: my-meb
vehicle_name: ID. Buzz
vehicle_image: /local/my-car.png
```

請將圖片儲存為 `/config/www/my-car.png`。裝置 ID 請使用安裝時自訂的值。
