# 發布前檢查清單

## 倉庫內容

- [ ] 根目錄包含 `SKILL.md` 與 `agents/openai.yaml`，可作為 agent skill 被正確識別。
- [ ] `raw/` 目錄包含完整的 270 篇古籍純文本 Markdown 語料。
- [ ] `allusions/INDEX.md` 與各主題分片 CSV 結構完整，每片小於 42 KB，可正常檢索。
- [ ] `prebuilt/` 包含單一總指南 `風格DNA.md` 與離線索引 `_meta/corpus_index.json`。
- [ ] `LICENSE` 為完整 GNU AGPL v3.0 原文，且 `README.md` 明確標示 `AGPL-3.0-or-later`。

## 內容一致性與自檢

- [ ] 執行 `python3 scripts/check_skill.py` 全數通過（路徑、索引、典故分片、原例比對與範例句律指標）。
- [ ] `SKILL.md`、`prebuilt/風格DNA.md`、`README.md` 與 `agents/openai.yaml` 的載入路徑與目錄結構一致。
- [ ] 明確說明對話與預設產物語體一致，且輸出四六文時須檢索 `allusions/` 並以純粹典雅漢語成文。
