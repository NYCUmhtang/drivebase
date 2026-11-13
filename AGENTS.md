# DRIVEBASE — AGENTS.md

> Version 1.0 · 2026-11-12 · 專案 AI 開發與維護規則

## 1. Mission and scope

DRIVEBASE 是繁體中文汽車百科與雙車規格比較的純靜態網站。第一版有 Toyota GR86、Subaru BRZ、Mazda MX-5，**未來不限車廠、車種或國家**。AI 應在不破壞既有功能的前提下，持續新增品牌、車系與明確規格版本。使用者可搜尋、篩選、查看車型及比較兩個版本。

## 2. Read first; allowed stack

修改前先讀本檔、`README.md`、`data/*.json`、`js/app.js`。使用 HTML5、CSS、原生 JavaScript、JSON；不得自行引入框架、雲端服務、付費 API、API 密鑰或後端。網站從 GitHub Pages `main / (root)` 發布，資源應使用相對路徑（避免 `/assets/...` 這類網域根路徑）。本機瀏覽用 HTTP server，不可依賴 `file://` 讀取 JSON。

## 3. Required files and responsibilities

- `index.html` 首頁；`explore.html` 搜尋篩選；`car.html` 共用車系詳細頁；`compare.html` 比較；`about.html` 專案說明。
- `css/style.css` 唯一主設計系統。
- `js/app.js` 共用資料讀取、卡片、細節、比較邏輯。
- `data/brands.json`、`data/models.json`、`data/variants.json` 為唯一車款資料來源，不可把車款規格硬寫進頁面。
- `assets/cars/` 放經授權的圖片或專案原創 SVG；`tests/validate.py` 檢查資料。

## 4. Design contract

Dark Performance 汽車媒體風格。CSS 使用 `--bg:#090b0f`、`--surface:#171b23`、`--accent:#e63946`、`--text:#f5f5f5`、`--muted:#a1abb9`。卡片大圖、簡潔標籤、清楚數據及可見 Hover/Focus。桌機列表 3 欄、平板 2 欄、手機 1 欄；比較表可橫向捲動。保持語意化標題、表格、按鈕、替代文字及鍵盤可操作性。不得因新增車系而重做 UI。

## 5. Data schema and ID rules

`Brand`：`id` (kebab-case)、`name`、`country`。

`Model`：`id`、`brand_id`、`name`、`body_type`、`tagline`、`description`、`image_path`、`image_credit`、`featured`。`model.brand_id` 必須存在。

`Variant`：`id`、`model_id`、`year`、`market`、`trim`、`transmission`、`drivetrain`、`fuel_type`、`specs`、`sources`、`status`。`year` 若官方未標示，為 `null`，並在 `trim` 標示；不得自行猜測年份。**同一規格版本 ID 不變**，以市場、年式、等級、變速箱等識別。

`specs` 欄位：`displacement_cc`、`power_kw`、`power_ps`、`torque_nm`、`torque_kgm`、`length_mm`、`width_mm`、`height_mm`、`wheelbase_mm`、`weight_kg`、`fuel_economy_km_l`、`fuel_cycle`。數字一律原生 JSON number、缺漏一律 `null`。資料以官方原標示單位保留：PS 不可誤當 kW、kg-m 不可誤當 N·m；若需要轉換，必須使用明確係數及記錄。油耗必須標示測試標準；未確定標準不得作效率優劣判定。未查證值不能猜測。

`Source`：`name`、`url`、`accessed` (YYYY-MM-DD)。`status` 允許 `published` 或 `draft`。已發布版本至少需有一個真正可追溯來源。圖片路徑必須為本專案內合法素材；不得直接引用未獲授權圖片。

`Variant` 對應唯一 `Model`；`Model` 對應唯一 `Brand`。新品牌、車系、版本應只加到對應 JSON，頁面由資料自動呈現。

## 6. Research & integrity

1. 先選定市場、年式與特定版本。無法查明的年式可用 `null`，但要明確標示，避免假裝完整。
2. 優先用車廠官方頁面及型錄；其他來源需交叉核實。每筆查證資訊應與版本吻合。
3. 不得跨市場／年式拼規格。遇到衝突，保留空值與待查證說明。
4. 不造假規格、資料來源、圖片授權、執行過程或測試通過結果。
5. 專案現有 SVG 是原創*概念示意圖*，不可宣稱是實車照片。

## 7. Exact Agent workflow: add a vehicle

1. **Inspect** — 閱讀規則、現有三份 JSON、相關 JS 與驗證器。
2. **Deduplicate** — 檢查 brand/model/variant ID 與是否存在相同市場、年式、版本。
3. **Verify** — 確認官方來源、正確版本與圖片權利；不確定欄位用 `null`。
4. **Modify data only where possible** — 增加所需的品牌、車系、版本記錄，保留現有資料與 ID。
5. **Validate** — 執行 `python tests/validate.py`；不能通過就修正或回報阻礙。
6. **Browser acceptance** — 使用 HTTP server 驗證首頁、搜尋、篩選、共用詳細頁、加入比較、雙車比較、手機表格、來源連結；如未測試必須明示。
7. **Report** — 清楚列出變更檔案、查證來源、執行的檢查、未驗證項目。

## 8. Behavior and safeguards

- 不得隨意刪除舊車款、重置規格、改 ID、改全站配色或引入破壞性依賴。
- 儘量只修改最小必要檔案；如果資料結構變更，必須同步更新本文件與驗證器。
- 使用者交辦「新增車型」但未確定市場、年式、變速箱時，優先查官方來源並選擇明確標示的版本；仍不明確則詢問，不得想像。
- 安全呈現外來資料：使用 DOM `textContent`，不要將資料字串直接拼成不安全 HTML。
- 比較同一欄位須使用同單位；差異為絕對差值，不能以數據高低宣稱車輛整體優勝。

## 9. Acceptance criteria

- HTML/CSS/JS 能在 GitHub Pages 靜態環境正常載入，無重大主控台錯誤。
- Schema／引用關係／唯一 ID／素材路徑／來源 URL 皆通過 `tests/validate.py`。
- 三款初始車系在首頁或 Explore 可顯示，搜尋、篩選及無結果狀態正確。
- `car.html?id=<model-id>` 顯示正確的品牌、車系、版本、規格、來源。
- 比較可選兩個不同 Variant、交換、顯示差異與缺漏，手機可捲動。
- 新增第四車後，無需修改所有 HTML，新車即能出現在 Explore 與比較頁。
- 未實際執行的瀏覽器測試必須標「未測試」，不能寫 PASS。

## 10. Required completion report

每次 AI 任務回報：**(a)** 任務結果；**(b)** 新增或修改的檔案；**(c)** 資料來源及不確定資訊；**(d)** 已執行測試的結果；**(e)** 未解決的問題。跨對話驗證時應保留 GitHub Commit 與實際操作結果；不強制建立額外報告文件。
