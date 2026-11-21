# 清流話風（tshiaengliu）

將本倉庫 `raw/` 目錄中的唐代與六朝名篇（四六駢文、文言散文、中古漢語口語公牘）蒸餾為可執行的風格 DNA，並結合 `allusions/`《初學記》典故庫，賦予 LLM agent 與 LLM chatbot 古雅而分層得體的**對話語言**與**默認產物語言**。

## 核心特點

- **開箱即用，亦可重蒸餾**：內置 `prebuilt/` 預蒸餾產物，安裝後即可直接啟用對話；若調整語料並重新蒸餾至 `distilled/`，則自動優先採用 `distilled/`。
- **對話與產物語言一致**：除非用戶額外指定其他語言或語體，模型生成的報告、總結、說明等產物，其語言風格默認與對話語言相同。
- **場合分層**：涵蓋四大唐代名家與《文選》共 270 篇語料，依對話用途自動切換三大語體層級。
- **四六文必用典故庫**：輸出四六文時檢索並運用 `allusions/` 目錄中的《初學記》典故與事對，確保對仗工整、用事有據。
- **只取文字，不取思維**：專注於古人的文字氣韻、結構章法與純文本排版；現代知識與問題解決邏輯仍由 LLM 自身承擔。

## 快速上手

### 1. 安裝即用

透過 `npx` 安裝本 skill：

```bash
npx skills add jiwei-y/tshiaengliu
```

安裝後直接喚起 `tshiaengliu`（或讓 agent 閱讀 `SKILL.md`）即可開始對話——agent 會讀取 `prebuilt/` 下的風格產物，並依 `_meta/corpus_index.json` 從 `raw/` 抽讀 5 篇原文校準語感，隨即按場合切換語體作答：

```text
請啟用 tshiaengliu 技能與我對話。
```

### 2. 重新蒸餾（可選）

若調整了 `raw/` 語料或需生成自訂版本，可讓 agent 按 [`SKILL.md`](SKILL.md) 第四節執行蒸餾並輸出至 `distilled/`（存在時自動優先於 `prebuilt/`）：

```text
請閱讀 SKILL.md，對本倉庫 raw/ 目錄下的全部文檔重新執行蒸餾，並將產物輸出至 distilled/ 目錄。
```

## 內置語料與語體分層

`raw/` 目錄收錄五組純文本 Markdown 文獻：

| 目錄 | 篇數 | 代表體裁與語體特徵 | 對應 LLM 對話場合 |
| - | - | - | - |
| `raw/文選/` | 14 | 六朝表、論，詞藻典麗，駢文典範 | 鄭重致辭、隆重論述、典雅四六文 |
| `raw/李商隱/` | 28 | 晚唐四六表狀，對仗精工、用典極密 | 正式賀慶、典雅總結、四六駢文 |
| `raw/崔致遠/` | 36 | 晚唐四六奏狀，駢儷工穩、公文格式嚴整 | 正式陳情、規範匯報、四六駢文 |
| `raw/陸贄/` | 56 | 中唐政論奏議，駢散兼行、條理縝密 | 深度分析、方案論證、利弊權衡 |
| `raw/李德裕/` | 136 | 兼含典雅讓表與大量邊防密狀，富含**中古漢語口語與唐代實務公牘** | 日常問答、即時匯報、工程排障等務實對話 |

三大語體層級：

1. **四六駢文**（典雅隆重場合，配合 `allusions/` 用典）
2. **駢散兼行**（深度分析與條陳論辯場合）
3. **中古口語公牘**（日常對話與務實協作場合）

## 內置典故庫（`allusions/`）

`allusions/` 目錄提供整理自《初學記》的兩份 CSV 數據表：

- `allusions/chuxueji_shidui.csv`（3,564 組對偶事對）：提供成對典故及雙方出處原文（如 `【轉蓋　倚杵】`、`【覆盆　轉轂】`），專供四六文駢句對仗檢索。
- `allusions/chuxueji_allusion.csv`（7,128 條單典）：提供單條典故名與出處原文，供單句嵌典與典意核驗。

## 蒸餾層次

| 層次 | 分析對象 | 產物文件 |
| - | - | - |
| **L1 表層語言** | 三大語體詞彙、稱謂與起訖套語、四六節律與對仗、聲律語氣、用典特徵、古文斷句標點 | `語言DNA.md` |
| **L2 篇章結構** | 起承轉合套式、三大語體結構模板、古文體裁至現代對話場合的映射 | `篇章結構模板.md` |
| **L3 排版格式** | 純文本 Markdown 的段落節奏、原生分條體例、引語與技術元素共存規範 | `排版格式指南.md` |

最終整合為總入口文檔 `風格DNA.md`，連同 `_meta/corpus_index.json` 元數據索引一併輸出。

## 目錄結構

```text
tshiaengliu/
├── SKILL.md                      # 技能規範
├── README.md                     # 本說明文檔
├── LICENSE
├── NOTICE
├── CONTRIBUTING.md
├── agents/
│   └── openai.yaml               # Agent 介面設定
├── prebuilt/                     # 內置預蒸餾風格產物
│   ├── _meta/
│   │   └── corpus_index.json
│   ├── 語言DNA.md
│   ├── 篇章結構模板.md
│   ├── 排版格式指南.md
│   └── 風格DNA.md
├── raw/                          # 內置古籍原始語料（270 篇純文本 Markdown）
│   ├── 崔致遠/
│   ├── 文選/
│   ├── 李商隱/
│   ├── 李德裕/
│   └── 陸贄/
├── allusions/                    # 內置《初學記》典故與事對庫
│   ├── chuxueji_allusion.csv
│   └── chuxueji_shidui.csv
├── templates/                    # 蒸餾產物與元數據模板
│   ├── README.md
│   ├── _meta/
│   │   └── example.schema.json
│   ├── 語言DNA.md
│   ├── 篇章結構模板.md
│   ├── 排版格式指南.md
│   └── 風格DNA.md
└── docs/
    ├── release-checklist.md
    └── usage-boundaries.md
```

## 授權協議

本項目採用 [GNU Affero General Public License v3.0 or later](LICENSE)（`AGPL-3.0-or-later`）授權，你可依自由軟體基金會發布的 GNU Affero 通用公共許可證第 3 版或（由你選擇的）任何更新版本之條款重新分發與修改本項目。`raw/` 與 `allusions/` 所收錄古籍文本均屬公有領域文獻。
