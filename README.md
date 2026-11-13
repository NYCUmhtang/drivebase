# DRIVEBASE 🚗

**DRIVEBASE** 是以 **AGENTS.md 作為 AI 開發規則**的汽車百科與雙車規格比較靜態網站。第一版展示 Toyota GR86、Subaru BRZ、Mazda MX-5 三個車系，提供搜尋、篩選、詳細規格與並列比較。

## 網站功能

- 首頁：品牌形象、動態車款數量、精選車系。
- Explore：品牌／車系搜尋、品牌與車身型式篩選。
- Detail：一個 `car.html` 頁面依 ID 載入不同車系、版本與來源。
- Compare：任選兩個版本並列規格、顯示可比較欄位的差異。
- 關於頁：資料政策、照片授權、Agent 使用說明。

## 部署與本機預覽

本專案不需要 npm 或後端。請使用 Python 內建 HTTP server（避免 `file://` 禁止 `fetch` JSON）：

```bash
cd drivebase
python -m http.server 8000
```

瀏覽 `http://localhost:8000/`。在 GitHub 上傳所有專案檔案，進入 **Settings → Pages → Deploy from a branch → main / (root) → Save**。本專案 Repository： https://github.com/NYCUmhtang/drivebase ；公開網站： https://nycumhtang.github.io/drivebase/ 。部署後應另外確認公開網址及互動功能。

## 專案檔案

```text
drivebase/
├── AGENTS.md
├── README.md
├── index.html
├── explore.html
├── car.html
├── compare.html
├── about.html
├── css/style.css
├── js/app.js
├── data/brands.json
├── data/models.json
├── data/variants.json
├── assets/cars/*.svg
├── tests/validate.py
└── tests/smoke.js
```

## 實際資料與限制

- Toyota GR86：採用台灣 Toyota 官方 2026/7 起生產 **6MT Brembo** 版規格，確定數值才填入。
- Subaru BRZ：採台灣官網列示 **2.4 MT ES**；官網展示未明確標年式，因此 `year=null`；未逐項確認的規格保持空值。
- Mazda MX-5：採台灣 Mazda 官方 2025 年車型規配表作為版本來源；未逐項核對的數值保持空值。
- 所有跑車圖為原創 SVG 概念示意，**非真實車款照片**。
- 規格並非即時資料，請以官方最新公告及實車為準。

## 開發 AI 的規則

`AGENTS.md` 定義了資料 Schema、命名規則、UI 設計、資料驗證、修改保護及驗收 SOP。新增一台車通常只需更新 `data/`，共用頁面會自動更新。

**可重複使用測試範例：** 在新的 AI 專案對話中交辦「請閱讀 AGENTS.md，新增指定台灣市場年份及版本的 Honda Civic Type R，保留現有車款與 UI，驗證搜尋、詳細頁與比較功能，回報真實測試結果」。測試完成後，保留 GitHub Commit 紀錄與實際結果；若未執行，應明確標示「尚未測試」。


## 驗證方式

使用 `python tests/validate.py` 驗證資料關係及檔案路徑，並使用 `node --check js/app.js` 檢查 JavaScript 語法。`tests/smoke.js` 是供瀏覽器開發者工具 Console 執行的簡易檢查，**不能直接用 `node tests/smoke.js` 執行**，也不能代替完整的搜尋、篩選與雙車比較操作驗收。
