# 整理原則詳解

需要語意分類、抽出個人產出、判斷版本或日期時閱讀此檔。

## 目錄
1. 進行中工作 vs 參考資料
2. 個人產出（output）
3. 日期
4. 重複檔與版本
5. 暫存檔
6. 歸檔策略
7. 各檔案類型的檢視方式
8. Git 儲存庫
9. 信心度

## 1. 進行中工作 vs 參考資料

```
Projects/Website/
  architecture.md
  roadmap.md
  meetings/

References/Standards/
  accessibility-guidelines.pdf
  api-style-guide.pdf
```

通用規格文件不因為某專案使用它，就算是該專案的文件。

## 2. 個人產出（output）

使用者自己產出的東西：簡報、報告、論文、海報、圖表、插圖、影片、音訊、修過的照片、產生的資料集、匯出的 PDF、對外網頁素材、最終交付物。

要和這些區分：來源/參考資料、原始資料、會議記錄、草稿、下載的文件、相依套件、暫時匯出。

### 放在專案內
優先用專案內的 `output/`，保留專案脈絡：

```
Projects/Website/
├── src/
├── docs/
├── data/
├── meetings/
└── output/
    ├── presentations/
    ├── posters/
    ├── reports/
    └── media/
```

而不是一個全域的 `Output/Website/`、`Output/ClientA/`——除非使用者明確想要全域集合。需要全域總覽時，用 `OUTPUT.md` 連結到各專案內的檔案：

```markdown
# Outputs
## 2026
### Website
- [上線簡報](Projects/Website/output/presentations/2026-09-website-launch-presentation.pdf)
- 專案海報
```

### 產出 vs 內部技術產物
- 產出：`presentation.pdf`、`paper.pdf`、`poster.pdf`、`edited-video.mp4`
- 內部產物（留在功能性資料夾，不放 output/）：`database-schema.sql`、`API-spec.yaml`、`migration.sql`、`test-data.csv`

### 草稿 vs 定稿
只有在證據足夠且區分有用時才用 `output/draft/`、`output/final/`；否則依類型分 `presentations/`、`reports/`。

### 產出命名
好：`2026-09-website-launch-presentation.pdf`、`2025-conference-poster.pdf`
避免：`final.pdf`、`presentation-final2.pptx`、`poster-new-new.pdf`

### 「幫我抽出我的產出」流程
1. 找出候選產出
2. 依專案分組
3. 區分草稿、來源素材、最終交付物
4. 提出目的地
5. 列出模稜兩可的檔案
6. 經授權才搬移
7. 視需要更新 `OUTPUT.md`

## 3. 日期

區分：檔案系統修改時間、文件日期、事件日期、發表日期。
重新命名時用**語意上有意義的日期**，格式 `YYYY-MM-DD`。檔案修改時間常因複製、下載而改變，不可靠。

## 4. 重複檔與版本

### 完全重複
SHA-256 相同 = 位元組完全相同（`scan.py` 已處理）。

### 疑似重複（不可自動處理）
- 同文件但中繼資料不同
- 匯出的副本
- 縮圖/改尺寸的圖片
- 修訂過的文件
- 改了名的副本

完全重複與疑似重複要分開回報。

### 版本判斷
看到 `v1/v2`、`final/final2/final-final`、`draft`、`old`、`backup`、`copy` 時，不要假設 `final` 就是權威版本。參考：修改時間、文件中繼資料、內文中的版本資訊、Git 歷史、周圍的專案結構。不確定就回報疑點。

## 5. 暫存檔

`~$document.docx`、`.DS_Store`、`Thumbs.db`、`*.tmp`、`*.swp`、`*.bak`
只有在明確可丟棄**且**使用者授權時才處理，而且仍是移到 `_待刪除/`。

## 6. 歸檔策略

依「不活躍」與意義歸檔，不是只看年齡。考慮：專案狀態、是否被現行工作引用、未來是否會用到、保存要求、歷史價值。不要因為很久沒修改就歸檔一個專案。

## 7. 各檔案類型的檢視方式

- **Markdown / TXT**：讀內容，找專案、標題、狀態、TODO、日期、連結、相關檔案。
- **PDF**：取中繼資料與文字；文字抽取不完整或亂碼時，看相關頁面的畫面。
- **DOCX**：標題、章節、中繼資料、日期、內容。
- **XLSX / CSV**：工作表名稱、欄位名稱、列數、代表性數值；大檔只取樣，不整個載入。
- **圖片**：檔名、EXIF、時間戳、尺寸、所在資料夾；只有在明顯改善分類時才看圖。
- **原始碼**：尊重 repo 邊界，不懂其建置/執行結構前不重組。

可擷取的語意欄位：標題、作者、組織、日期、專案、主題、文件類型、版本、狀態、引用的檔案/專案。

常用語意類型：proposal、meeting-notes、report、presentation、specification、dataset、documentation、source-code、research-paper、invoice、contract、reference、archive、temporary。

## 8. Git 儲存庫

含 `.git/` 的資料夾視為 repo：保留相對路徑、改名時檢查引用、不為了美觀重組內部。要整理就在專案層級（整個 repo 搬到 `Projects/Website/`），不動內部。

## 9. 信心度

語意推斷的分類要標：
- **HIGH**：多項證據一致（標題 + 內容 + 相鄰檔案）
- **MEDIUM**：有合理證據但不完整（例如只有檔名與資料夾）
- **LOW**：猜測 → 列入「待決定」，不直接搬

```
report.pdf → Projects/ClientA/
confidence: HIGH
evidence: 標題 + 內容 + 相鄰檔案
```
