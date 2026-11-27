# 清流話風（tshiaengliu）

將本倉庫 `raw/` 目錄中的唐代與六朝名篇（中古口語公牘、駢散兼行、四六駢文）凝練為可執行的風格指南，並結合 `allusions/`《初學記》分門事對典故庫，賦予 LLM agent 與 chatbot 分層得體的**對話語言**與**默認產物語言**。

## 核心特點

- **按需載入、低上下文開銷**：日常對話預設讀入 `prebuilt/風格DNA.md` 與 5 篇精選李德裕密狀（約 13 KB），切換至駢散長論或四六駢文時才延遲載入對應範文與典故分片。
- **對話與產物語言一致**：除非用戶額外指定其他語言或格式，生成的報告、總結與說明皆沿用當前語體。
- **四六文必核典故**：依 `allusions/INDEX.md` 按主題取分片 CSV 或執行 `scripts/check_skill.py --allusion` 核對出處原文，全篇以純粹漢語成文。
- **只取文字，不取思維**：實務與論辨語體中，程式碼、命令、路徑、錯誤碼與技術事實原樣保留；四六駢文則以典雅漢語傳達真實事功。

## 快速上手

### 1. 安裝即用

- **Coding Agent（三體核心）**：

```bash
npx skills add jiwei-y/tshiaengliu
```

安裝後直接喚起 `tshiaengliu`（或讓 agent 閱讀 `SKILL.md`）即可開始對話：

```text
請啟用 tshiaengliu 技能與我對話。
```

- **Gemini Web App（網頁端四體：口語公牘、四六禮辭、四六論事、六朝駢論）**：直接自本倉庫 [GitHub Releases](https://github.com/jiwei-y/tshiaengliu/releases/latest) 下載最新的 `tshiaengliu-web-*.zip` 上傳為技能，或本機執行下方 `--pack-web` 一鍵打包（僅收實操精選範文與典故分片，符合網頁端檔案數上限）。

### 2. 自檢、打包與重新蒸餾（可選）

執行內置自檢腳本，驗證倉庫路徑、語料索引、典故表與黃金範例的句律節奏（亦可一鍵產出 Gemini Web App 技能包，或以 `--style` 檢驗任意輸出樣本的短句與分號指標）：

```bash
python3 scripts/check_skill.py                                 # 驗證 prebuilt/ 完整性、原例逐字比對與範例句律
python3 scripts/check_skill.py --pack-web dist/tshiaengliu-web.zip # 一鍵打包四體網頁端 Gemini Web App 技能 zip
python3 scripts/check_skill.py --stats                         # 輸出 raw/ 客觀句律、高頻詞、邊界篇與範文候選
python3 scripts/check_skill.py --target distilled              # 驗證重蒸餾產物 distilled/
python3 scripts/check_skill.py --allusion 規矩                  # 檢索《初學記》事對與完整出處（供四六駢文）
python3 scripts/check_skill.py --style sample.txt              # 檢測任意輸出樣本的短句、長句比與分號節奏
```

若調整了 `raw/` 語料，可依 [`SKILL.md`](SKILL.md) 第五節重新蒸餾並輸出至 `distilled/`（存在時自動優先於 `prebuilt/`）：

```text
請閱讀 SKILL.md，對 raw/ 語料重新蒸餾並輸出至 distilled/。
```

## 內置語料與分層語體

`raw/` 收錄五組共 270 篇純文本 Markdown 文獻：

| 目錄 | 篇數 | 代表體裁與語體特徵 | 對應對話場合 |
| - | - | - | - |
| `raw/李德裕/` | 136 | 99 篇中古口語公牘密狀（另有駢散奏議與四六表狀） | **日常預設**：問答、匯報、排障、分派 |
| `raw/陸贄/` | 56 | 中唐政論奏議，駢散兼行、善設問推論 | Coding Agent 深度分析、架構論證、利弊權衡 |
| `raw/崔致遠/` | 36 | 晚唐四六表狀，兼有賀慶禮辭與時務論事 | 四六禮辭；網頁端增補四六論事陳情 |
| `raw/李商隱/` | 28 | 晚唐四六表狀，對仗精工、用典極密 | 四六禮辭；網頁端增補四六諫論陳情 |
| `raw/文選/` | 14 | 六朝表、論，辭采典雅、宏議鋪張 | 四六禮辭；網頁端增補六朝駢論 |

## 內置典故庫（`allusions/`）

- `allusions/INDEX.md` 與 34 個主題分片 CSV（`allusions/01_天象日月.csv` 至 `allusions/34_鳥部鱗介.csv`）：收錄《初學記》3,564 組對偶事對（`allusion,source_text1,source_text2`），便於按主題直接讀取或由 `scripts/check_skill.py --allusion` 跨片檢索。

## 目錄結構

```text
tshiaengliu/
├── SKILL.md                          # Coding Agent 三體薄入口（按需載入與回錨規則）
├── README.md                         # 本說明文檔
├── LICENSE
├── NOTICE
├── CONTRIBUTING.md
├── .github/workflows/
│   └── release-web-skill.yml         # 合併至 main 後自動發布四體 Web App zip 至 Release
├── agents/
│   └── openai.yaml                   # Agent 介面設定
├── prebuilt/
│   ├── 風格DNA.md                    # 三體核心總指南（含句法核與現代工程範例）
│   ├── 擴充語體.md                    # 網頁端增補指南（四六論事陳情、六朝駢論）
│   └── _meta/
│       └── corpus_index.json         # 全庫 270 篇離線分類索引（供重蒸餾使用）
├── raw/                              # 270 篇唐與六朝純文本語料
│   ├── 崔致遠/
│   ├── 文選/
│   ├── 李商隱/
│   ├── 李德裕/
│   └── 陸贄/
├── allusions/
│   ├── INDEX.md                      # 《初學記》34 門主題分片目錄
│   └── 01_天象日月.csv … 34_鳥部鱗介.csv
├── scripts/
│   └── check_skill.py                # 倉庫自檢、語料統計、典故檢索、句律檢測與 Web zip 打包
└── docs/
    ├── release-checklist.md
    └── usage-boundaries.md
```

## 授權協議

本項目採用 [GNU Affero General Public License v3.0 or later](LICENSE)（`AGPL-3.0-or-later`）授權，你可依自由軟體基金會發布的 GNU Affero 通用公共許可證第 3 版或（由你選擇的）任何更新版本之條款重新分發與修改本項目。`raw/` 與 `allusions/` 所收錄古籍文本均屬公有領域文獻。
