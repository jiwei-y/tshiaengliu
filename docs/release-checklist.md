# 發布前檢查清單

## 倉庫內容

- [ ] 根目錄包含 `SKILL.md` 與 `agents/openai.yaml`，可作為 agent skill 被正確識別。
- [ ] `raw/` 目錄包含完整的古籍純文本 Markdown 語料。
- [ ] `allusions/` 目錄包含 `chuxueji_allusion.csv` 與 `chuxueji_shidui.csv`。
- [ ] `prebuilt/` 包含完整的預蒸餾開箱即用產物（`_meta/corpus_index.json`、`語言DNA.md`、`篇章結構模板.md`、`排版格式指南.md`、`風格DNA.md`），根目錄 `distilled/` 保持空置。
- [ ] `templates/` 包含完整的繁體中文蒸餾產物模板（`語言DNA.md`、`篇章結構模板.md`、`排版格式指南.md`、`風格DNA.md` 與 `_meta/example.schema.json`）。
- [ ] `LICENSE` 為完整 GNU AGPL v3.0 原文，且 `README.md` 明確標示 `AGPL-3.0-or-later`。

## 內容一致性

- [ ] 全倉庫核心文檔與模板統一使用繁體中文。
- [ ] 蒸餾層次統一為 L1（表層語言）、L2（篇章結構）、L3（純文本 Markdown 排版格式）。
- [ ] 明確說明本項目直接用於 LLM 對話語言，且產物語言默認與對話語言一致。
- [ ] 明確規範輸出四六文時必須檢索並使用 `allusions/` 中的典故與事對。
