#!/usr/bin/env python3
"""Integrity, corpus measurement (--stats), and rhythm check (--style) for tshiaengliu."""

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALID_REGISTERS = ("中古口語公牘", "駢散兼行", "四六駢文")
FUNC_CHARS = tuple("之於以而則便即須緣望得却都合要恐只並也矣焉乎哉耳")
REGISTER_CONTRAST = (
    ("條件承接", ("苟", "儻", "則", "輒"), ("如", "若", "便", "即")),
    ("原因說明", ("因", "良以"), ("緣", "只緣", "所以")),
    ("請求處置", ("伏乞", "乞"), ("望", "伏望", "仍望")),
    ("動補處置", ("持", "反"), ("將", "却", "即得", "亦得", "即免")),
    ("限定判斷", ("唯", "惟", "非"), ("只", "只是", "不是")),
    ("助動禁止", ("欲", "當", "不宜", "勿", "莫"), ("須", "要", "合", "不合", "不得", "不要")),
    ("全稱追加", ("凡", "咸", "悉", "他", "餘", "復"), ("皆", "並", "都", "别", "更", "仍", "兼")),
    ("預判言說", ("懼", "曰", "言", "遽"), ("恐", "必恐", "云", "説", "速", "早", "商量")),
)
COURT_RE = re.compile(r"屏營|兢皇|兢越|頓首|懇切之至|感切之至|懇願之至|伏聽敕|伏候敕|伏侯敕|俯伏待罪|不勝懇|不任懇|丹懇|謹奉表")
KO_RE = re.compile(r"只緣|只是|只可|只合|却|都不|都無|都未|都似|商量|未審|穩便|處分|便須|即須|便令|即令|伏望|仍望|望付|望令|並是|並無|並不|更無|不要|切要|未要|似可")
ARG_RE = re.compile(r"是以|然則|何則|豈不|乎[？。]|也[，。]|矣[，。]|焉[，。]|哉[？！。]")


def rhythm_metrics(text: str) -> dict:
    # Normalize inline code / ASCII identifiers to 2-char placeholders for syntactic rhythm.
    norm = re.sub(r"`[^`]+`|[A-Za-z0-9_./@#<>:-]+", "某某", text)
    han = re.sub(r"[^\u4e00-\u9fff\u3400-\u4dbf]", "", norm)
    if not han:
        raise ValueError("no Chinese text to measure")
    clauses = [
        len(re.sub(r"[^\u4e00-\u9fff\u3400-\u4dbf]", "", p))
        for p in re.split(r"[，。；？！：、\n]+", norm)
    ]
    clauses = [c for c in clauses if c > 0]
    clauses_sorted = sorted(clauses)
    colon_headers = len(re.findall(r"(?m)^[一二三四五六七八九十]+、[^，。！？\n]{1,12}：", text))
    return {
        "han": len(han),
        "clauses": len(clauses),
        "avg_clause": sum(clauses) / len(clauses),
        "p90_clause": clauses_sorted[int(0.9 * (len(clauses_sorted) - 1))],
        "pct_4_6": sum(1 for c in clauses if c in (4, 6)) * 100 / len(clauses),
        "pct_9p": sum(1 for c in clauses if c >= 9) * 100 / len(clauses),
        "comma_1k": text.count("，") * 1000 / len(han),
        "period_1k": text.count("。") * 1000 / len(han),
        "semi_per_1k": text.count("；") * 1000 / len(han),
        "quest_1k": text.count("？") * 1000 / len(han),
        "dun_1k": text.count("、") * 1000 / len(han),
        "colon_headers": colon_headers,
    }


def load_index_groups(index_path: Path) -> tuple[dict[str, list[tuple[str, str]]], list[str]]:
    raw_map = {(p.parent.name, p.stem): p for p in sorted((ROOT / "raw").rglob("*.md"))}
    if not index_path.is_file():
        groups: dict[str, list[tuple[str, str]]] = {}
        for (grp, title), p in raw_map.items():
            groups.setdefault(grp, []).append((f"{grp}/{title}.md", p.read_text(encoding="utf-8")))
        return groups, ["no corpus_index.json found; grouped by raw/ folder"]

    index = json.loads(index_path.read_text(encoding="utf-8"))
    groups = {}
    seen = set()
    warnings = []
    for d in index:
        key = (d["source_group"], d["title"])
        if key not in raw_map:
            warnings.append(f"orphan index entry: {key[0]}/{key[1]}.md")
            continue
        seen.add(key)
        groups.setdefault(d["register"], []).append(
            (f"{key[0]}/{key[1]}.md", raw_map[key].read_text(encoding="utf-8"))
        )
    for missing in sorted(set(raw_map) - seen):
        warnings.append(f"unindexed raw file: {missing[0]}/{missing[1]}.md")
    return groups, warnings


def print_stats(target_dir: str) -> None:
    index_path = ROOT / target_dir / "_meta/corpus_index.json"
    groups, warnings = load_index_groups(index_path)
    for w in warnings:
        print(f"WARN: {w}")

    ordered = [g for g in VALID_REGISTERS if g in groups] + [g for g in groups if g not in VALID_REGISTERS]
    reg_blobs: dict[str, tuple[str, int]] = {}
    for reg in ordered:
        docs = groups[reg]
        joined = "\n".join(t for _, t in docs)
        m = rhythm_metrics(joined)
        reg_blobs[reg] = (joined, m["han"])
        print(
            f"\n=== {reg} ({len(docs)} 篇, {m['han']} 漢字) ===\n"
            f"句律: 均分句 {m['avg_clause']:.1f} 字 | P90 {m['p90_clause']} 字 | "
            f"四六句 {m['pct_4_6']:.1f}% | ≥9字 {m['pct_9p']:.1f}%\n"
            f"標點/千字: ，{m['comma_1k']:.1f} 。{m['period_1k']:.1f} ；{m['semi_per_1k']:.1f} "
            f"？{m['quest_1k']:.1f} 、{m['dun_1k']:.1f}"
        )
        # Openings, closings, high-frequency function chars & 2-char markers (by doc coverage).
        opens = Counter(t.lstrip()[:2] for _, t in docs if len(t.lstrip()) >= 2)
        closes = Counter(re.sub(r"[。？！\s]+$", "", t.rstrip())[-2:] for _, t in docs if t.strip())
        fn_top = sorted(
            ((ch, joined.count(ch) * 1000 / m["han"]) for ch in FUNC_CHARS),
            key=lambda x: -x[1],
        )[:10]
        bg_docs: Counter = Counter()
        for _, t in docs:
            bg_docs.update(set(re.findall(r"[\u4e00-\u9fff]{2}", t)))
        bg_top = [(w, c) for w, c in bg_docs.most_common(12) if c >= max(3, len(docs) // 6)]
        print("高頻開頭(篇數):", ", ".join(f"{k}:{v}" for k, v in opens.most_common(6)))
        print("高頻收尾(篇數):", ", ".join(f"{k}:{v}" for k, v in closes.most_common(6)))
        print("高頻虛詞(/千字):", ", ".join(f"{k}:{v:.1f}" for k, v in fn_top))
        print("高頻雙字(涵蓋篇數):", ", ".join(f"{k}:{v}/{len(docs)}" for k, v in bg_top[:10]))

        # Exemplar candidates: clean (no □), 120-450 Han chars, closest to register avg_clause & semi_per_1k.
        scored = []
        outliers = []
        for rel, t in docs:
            dm = rhythm_metrics(t)
            unquoted = re.sub(r"「[^」]*」", "", t)
            if reg == "中古口語公牘" and (COURT_RE.search(t) or (len(ARG_RE.findall(t)) >= 4 and len(KO_RE.findall(unquoted)) <= 2)):
                outliers.append(f"{rel} (court={len(COURT_RE.findall(t))}, arg={len(ARG_RE.findall(t))})")
            elif reg == "駢散兼行" and len(KO_RE.findall(unquoted)) >= 3 and len(ARG_RE.findall(t)) <= 2 and not COURT_RE.search(t):
                outliers.append(f"{rel} (ko={len(KO_RE.findall(unquoted))}, arg={len(ARG_RE.findall(t))})")
            if "□" not in t and 120 <= dm["han"] <= 450:
                dist = abs(dm["avg_clause"] - m["avg_clause"]) + abs(dm["semi_per_1k"] - m["semi_per_1k"]) / 3
                scored.append((dist, rel, dm["han"], dm["avg_clause"]))
        scored.sort()
        print("潔淨範文候選:", ", ".join(f"{rel}({h}字,均{a:.1f})" for _, rel, h, a in scored[:5]))
        if outliers:
            print("疑似跨體邊界篇(須複核):", "; ".join(outliers[:8]))

    if len(ordered) >= 2:
        hdr = " / ".join(ordered)
        print(f"\n=== 跨體語體傾向對照（/千字，序：{hdr}） ===")
        for label, lit_terms, col_terms in REGISTER_CONTRAST:
            fmt = lambda terms: " ".join(
                f"{w}({'/'.join(f'{reg_blobs[r][0].count(w) * 1000 / reg_blobs[r][1]:.1f}' for r in ordered)})"
                for w in terms
                if any(w in reg_blobs[r][0] for r in ordered)
            )
            print(f"{label}: 文言[{fmt(lit_terms)}] ↔ 口語[{fmt(col_terms)}]")


def check_repo(target_dir: str) -> None:
    guide_path = ROOT / target_dir / "風格DNA.md"
    index_path = ROOT / target_dir / "_meta/corpus_index.json"
    assert guide_path.is_file(), f"missing {guide_path.relative_to(ROOT)}"
    assert index_path.is_file(), f"missing {index_path.relative_to(ROOT)}"

    # 1. Local file paths cited in active docs exist on disk.
    path_re = re.compile(r"`((?:raw|prebuilt|allusions|scripts)/[^`]+?\.(?:md|json|csv|py))`")
    for doc in (ROOT / "SKILL.md", ROOT / "README.md", guide_path, *sorted((ROOT / "docs").glob("*.md"))):
        for rel in path_re.findall(doc.read_text(encoding="utf-8")):
            assert (ROOT / rel).is_file(), f"missing path {rel} referenced in {doc.relative_to(ROOT)}"

    # 2. corpus_index.json matches raw/**/*.md 1:1 with valid registers.
    raw_files = sorted((ROOT / "raw").rglob("*.md"))
    raw_keys = {(p.parent.name, p.stem) for p in raw_files}
    index = json.loads(index_path.read_text(encoding="utf-8"))
    idx_keys = {(d["source_group"], d["title"]) for d in index}
    assert len(index) == len(idx_keys) == len(raw_keys), "corpus_index count/duplicate mismatch"
    assert idx_keys == raw_keys, f"corpus_index diff: {idx_keys ^ raw_keys}"
    for d in index:
        assert d["register"] in VALID_REGISTERS, f"bad register: {d}"

    # 3. allusions/INDEX.md and thematic CSV shards parse cleanly and stay under 42 KB each.
    allusion_index = ROOT / "allusions/INDEX.md"
    assert allusion_index.is_file(), "missing allusions/INDEX.md"
    shards = sorted((ROOT / "allusions").glob("*.csv"))
    assert shards, "no allusion CSV shards found"
    indexed_shards = set(re.findall(r"`(allusions/[^`]+\.csv)`", allusion_index.read_text(encoding="utf-8")))
    disk_shards = {f"allusions/{p.name}" for p in shards}
    assert indexed_shards == disk_shards, f"allusions/INDEX.md mismatch: {indexed_shards ^ disk_shards}"
    pair_count = 0
    for p in shards:
        assert p.stat().st_size <= 42000, f"allusion shard too large ({p.stat().st_size}B): {p.name}"
        with p.open(encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        assert rows[0] == ["allusion", "source_text1", "source_text2"], f"bad header in {p.name}: {rows[0]}"
        assert all(len(r) == 3 for r in rows[1:]), f"malformed row in {p.name}"
        pair_count += len(rows) - 1
    assert pair_count == 3564, f"expected 3564 allusion pairs, got {pair_count}"

    # 4. All verbatim corpus quotes in tables exist in raw/ (skip schematic placeholders containing …).
    guide_text = guide_path.read_text(encoding="utf-8")
    raw_blob = "\n".join(p.read_text(encoding="utf-8") for p in raw_files)
    table_quotes = [
        q
        for line in guide_text.splitlines()
        if line.startswith("|") and "「" in line
        for q in re.findall(r"「([^」]+)」", line)
        if "…" not in q
    ]
    for q in table_quotes:
        assert q in raw_blob, f"table quote not found verbatim in raw/: 「{q}」"

    # 5. Embedded golden examples satisfy dynamically measured baseline rhythm of 中古口語公牘.
    max_avg, max_semi, max_9p = ldy_limits(index_path)
    examples = re.findall(r"```example-ldy\n(.*?)\n```", guide_text, flags=re.S)
    assert len(examples) >= 3, "expected at least 3 example-ldy blocks"
    for i, ex in enumerate(examples, 1):
        m = rhythm_metrics(ex)
        assert m["avg_clause"] <= max_avg, f"example {i} avg_clause {m['avg_clause']:.1f} > {max_avg}"
        assert m["semi_per_1k"] <= max_semi, f"example {i} semi/1k {m['semi_per_1k']:.1f} > {max_semi}"
        assert m["pct_9p"] <= max_9p, f"example {i} >=9-char ratio {m['pct_9p']:.1f}% > {max_9p}%"
        assert m["colon_headers"] == 0, f"example {i} uses colon-header list"

    print(
        f"OK ({target_dir}): {len(raw_keys)} raw docs, {len(shards)} allusion shards ({pair_count} pairs), "
        f"{len(table_quotes)} verbatim quotes, {len(examples)} golden examples "
        f"(limits: avg<={max_avg}, >=9<={max_9p}%, semi/1k<={max_semi})."
    )


def ldy_limits(index_path: Path) -> tuple[float, float, float]:
    groups, _ = load_index_groups(index_path)
    base_avg, base_semi, base_9p = 5.6, 1.1, 10.9
    if "中古口語公牘" in groups:
        bm = rhythm_metrics("\n".join(t for _, t in groups["中古口語公牘"]))
        base_avg, base_semi, base_9p = bm["avg_clause"], bm["semi_per_1k"], bm["pct_9p"]
    return (
        round(base_avg + 1.5, 1),
        round(max(2.0, base_semi * 2.0), 1),
        round(min(30.0, base_9p + 15.0), 1),
    )


def check_style(target: str) -> None:
    text = sys.stdin.read() if target == "-" else Path(target).read_text(encoding="utf-8")
    try:
        m = rhythm_metrics(text)
    except ValueError as exc:
        sys.exit(str(exc))
    idx_dir = "distilled" if (ROOT / "distilled/_meta/corpus_index.json").is_file() else "prebuilt"
    max_avg, max_semi, max_9p = ldy_limits(ROOT / idx_dir / "_meta/corpus_index.json")
    print(
        f"han={m['han']} avg_clause={m['avg_clause']:.1f} (<={max_avg}) "
        f">=9={m['pct_9p']:.1f}% (<={max_9p}%) p90={m['p90_clause']} "
        f"semi/1k={m['semi_per_1k']:.1f} (<={max_semi}) colon_headers={m['colon_headers']}"
    )
    if m["avg_clause"] > max_avg or m["semi_per_1k"] > max_semi or m["pct_9p"] > max_9p or m["colon_headers"] > 0:
        sys.exit(1)


def search_allusion(keyword: str, limit: int = 10) -> None:
    hits = []
    for p in sorted((ROOT / "allusions").glob("*.csv")):
        with p.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                s1, s2 = r["source_text1"].strip(), r["source_text2"].strip()
                if not s1 or not s2 or "見上" in s1 or "見上" in s2:
                    continue
                if keyword in r["allusion"] or keyword in s1 or keyword in s2:
                    hits.append((p.name, r["allusion"], s1, s2))
    for fname, name, s1, s2 in hits[:limit]:
        print(f"[{fname}] {name}\n  1: {s1}\n  2: {s2}")
    print(f"({min(len(hits), limit)}/{len(hits)} clean matches for '{keyword}')")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        check_repo("prebuilt")
    elif args[0] == "--target" and len(args) == 2:
        check_repo(args[1])
    elif args[0] == "--stats":
        target = args[2] if len(args) == 3 and args[1] == "--target" else "prebuilt"
        print_stats(target)
    elif args[0] == "--style" and len(args) == 2:
        check_style(args[1])
    elif args[0] == "--allusion" and len(args) == 2:
        search_allusion(args[1])
    else:
        sys.exit(
            "Usage: check_skill.py [--target prebuilt|distilled] | "
            "[--stats [--target DIR]] | [--allusion KEYWORD] | [--style <file|->]"
        )
