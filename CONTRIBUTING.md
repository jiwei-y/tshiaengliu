# 貢獻指南

歡迎改進 `tshiaengliu`（清流話風）的風格指南、語料校訂、分類索引與自檢腳本。

## 可以貢獻

- 校訂 `raw/` 古籍文本與 `allusions/` 典故分片表中的訛字、標點或格式問題
- 改進 `prebuilt/風格DNA.md` 的實測句法歸納與現代場景對照範例
- 完善 `prebuilt/_meta/corpus_index.json` 的語體分類準確度與 `scripts/check_skill.py` 的結構化檢核

## 撰寫規範

- 本倉庫文檔統一使用**繁體中文**，規則說明採中性現代白話。
- 修改載入流程、檔案結構或典故檢索規則時，請同步檢查 `SKILL.md`、`README.md`、`prebuilt/風格DNA.md` 與 `agents/openai.yaml`，並執行 `python3 scripts/check_skill.py` 驗證通過。

## 請勿提交

- 未經授權的現代版權文本或私密聊天記錄
- 帶有圖片二進制文件或 HTML 樣式標記的語料

貢獻者保留自己貢獻內容的著作權。
