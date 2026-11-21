# 蒸餾產物示例

本目錄存放一份對本倉庫 `raw/` 全部 270 篇古籍語料執行蒸餾後的參考產物，供查閱格式或直接試用；倉庫根目錄下的 `distilled/` 保持空置，留供用戶自行執行蒸餾時輸出。

```text
examples/format-only/
├── _meta/
│   └── corpus_index.json     # 全量 270 篇元數據索引
├── 語言DNA.md                # L1 表層語言產物
├── 篇章結構模板.md            # L2 篇章與對話結構產物
├── 排版格式指南.md            # L3 純文本 Markdown 排版產物
└── 風格DNA.md                # 總入口整合文檔
```

自行重新蒸餾時，請參照 `SKILL.md` 與 `templates/`，將新產物輸出至根目錄下的 `distilled/`。
