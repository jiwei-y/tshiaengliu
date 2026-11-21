# 內置預蒸餾產物（prebuilt）

本目錄存放對本倉庫 `raw/` 全部 270 篇語料預先蒸餾完成的風格產物，供直接啟用對話時讀取：

```text
prebuilt/
├── _meta/
│   └── corpus_index.json     # 全量 270 篇元數據索引
├── 語言DNA.md                # L1 表層語言產物
├── 篇章結構模板.md            # L2 篇章與對話結構產物
├── 排版格式指南.md            # L3 純文本 Markdown 排版產物
└── 風格DNA.md                # 總入口整合文檔
```

若用戶自行執行蒸餾並生成 `distilled/`，agent 會自動優先讀取 `distilled/`。
