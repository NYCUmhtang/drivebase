# DRIVEBASE V1.0 驗證紀錄（2026-11-12）

## 已執行

| 檢查 | 結果 | 說明 |
|---|---|---|
| `python tests/validate.py` | PASS | 3 brands、3 models、3 variants，檢查唯一 ID、資料關聯、來源網址、素材存在與型別 |
| `node --check js/app.js` | PASS | JavaScript 語法可解析 |
| Headless Chromium DOM 測試：首頁 | PASS | 用實際 HTML/JS 與模擬 `fetch` 的本地 JSON，渲染 3 款車系 |
| Explore 搜尋／品牌篩選／空結果 | PASS | 搜尋 BRZ、選 Mazda、找不到結果 |
| Car Detail | PASS | GR86 詳細頁及 2,387 cm³ 正確渲染；加入比較操作 |
| Compare | PASS | 並列規格、交換、相同版本警告 |
| JavaScript 例外 | PASS | DOM 測試無 uncaught page error |

## 尚未完成的驗證

- 受目前測試環境限制，無法從 Chromium 直接瀏覽 `localhost` 或 `file://`；因此沒有通過實際 HTTP URL 的完整端對端瀏覽器驗收。
- 尚未實際部署 GitHub Pages，故未驗證公開網址。
- 尚未完成手機實際網頁運行及視覺回歸測試。
- 尚未在全新 AI 工作階段新增第四車；請參閱 `docs/agent-validation.md`。

## 資料誠信

- Toyota GR86 已依 Toyota Taiwan 官網指定規配版本填入有直接依據的數值；官方提供 PS 與 kg-m，保留原單位，未自行換算。
- Subaru BRZ 目前僅保存官網有明確列出的傳動、驅動與車系資訊，未確認的數值為 null。
- Mazda MX-5 已記錄官方 2025 規配表來源，未逐一重新核對的規格值為 null。
- 三張車輛圖像均為專案自行產生的通用向量示意圖，非原車型照片。
