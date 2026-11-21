# 內置預蒸餾產物（prebuilt）

本目錄存放對本倉庫 `raw/` 全部 270 篇古籍語料預先蒸餾完成的風格產物，隨 skill 一併安裝，供用戶**無需蒸餾、開箱即用**。

```text
prebuilt/
├── _meta/
│   └── corpus_index.json     # 全量 270 篇元數據索引
├── 語言DNA.md                # L1 表層語言產物
├── 篇章結構模板.md            # L2 篇章與對話結構產物
├── 排版格式指南.md            # L3 純文本 Markdown 排版產物
└── 風格DNA.md                # 總入口整合文檔
```

倉庫根目錄下的 `distilled/` 保持空置，留供用戶自行重新蒸餾時輸出；若 `distilled/` 存在，agent 會自動優先讀取 `distilled/`，否則讀取本目錄。
