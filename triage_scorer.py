#!/usr/bin/env python3
"""
Sovereign Think-Tank — MSOU Triage Scorer
==========================================
Scores all 1,435 entity files on 4 dimensions:
  M — Market Size        (1-5)
  S — Speed to Revenue   (1-5)
  O — Operational Moat   (1-5)
  U — Unfair Advantage   (1-5)

Max score: 20
Cutoffs: 18-20 = Top 20 | 16-17 = Top 50 | <16 = Backlog

Output: wiki/concepts/triage-scoring-matrix.md
"""

import os
import re
from pathlib import Path
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ENTITIES_DIR = Path("/home/simian420/projects/wiki/entities")
OUTPUT_FILE  = Path("/home/simian420/projects/wiki/concepts/triage-scoring-matrix.md")
PREVIEW_CHARS = 800  # chars to read per file for scoring

# ---------------------------------------------------------------------------
# Scoring keyword maps
# ---------------------------------------------------------------------------

# M — Market Size: keywords that signal large addressable markets
MARKET_HIGH = [
    "maritime","ais","shipping","vessel","satellite","defense","military",
    "government","enterprise","b2b","saas","api","platform","cloud","fintech",
    "crypto","blockchain","zero-knowledge","zkp","snark","intelligence","osint",
    "surveillance","forensic","legal","ediscovery","discovery","arbitration",
    "customs","trade","supply chain","logistics","energy","grid","power",
    "water","infrastructure","telecom","iot","sensor","mesh","lora","rf",
    "radio","comms","5g","autonomous","ai","llm","gpt","neural","ml",
]
MARKET_MED = [
    "commercial","market","revenue","customer","client","product","service",
    "startup","venture","patent","ip","license","monetize","sell","deploy",
]

# S — Speed to Revenue: keywords indicating quick-to-ship products
SPEED_HIGH = [
    "api","webhook","script","cli","tool","utility","filter","parser",
    "dashboard","feed","alert","monitor","detector","scanner","analyzer",
    "report","export","pipeline","bot","agent","plugin","extension",
]
SPEED_LOW = [
    "hardware","chip","asic","pcb","firmware","fab","prototype","foundry",
    "antenna","satellite","rocket","drone","vehicle","construction","building",
]

# O — Operational Moat: keywords indicating defensible IP
MOAT_HIGH = [
    "patent","proprietary","novel","unique","algorithm","cryptographic",
    "zk","snark","stark","threshold","enclave","sgx","tee","hsm",
    "air-gap","airgap","sovereign","zero-trust","mesh","rns","residue",
    "wasm","sandbox","enclave","forensic","chain-of-custody","title 18",
    "zeroization","tamper","classified","confidential",
]
MOAT_LOW = [
    "standard","common","open source","open-source","generic","basic",
    "simple","wrapper","integration","connector","glue","helper",
]

# U — Unfair Advantage: keywords tied to your specific 3yr R&D history
UNFAIR_HIGH = [
    "peru","lima","sjl","pacific sentinel","ais","lora","js8call","hf","nvis",
    "andes","lifepo4","bms","mppt","solar","off-grid","rns-pulse","aegis",
    "dresos","posix-shm","avx","zfs","zeroization","simian","mcclaude",
    "gemini takeout","combinatorial","synthesis engine","wiki","entity",
    "simiandox","local llm","ollama","deepseek","qwen","whisper","enf",
    "audio waveform","deepfake","nara","title 18","maritime intel",
    "pacific","sentinel","andean","vantage",
]

# ---------------------------------------------------------------------------
# Scorer
# ---------------------------------------------------------------------------

class Score(NamedTuple):
    filename: str
    m: int
    s: int
    o: int
    u: int
    total: int
    preview: str


def score_keywords(text: str, high: list, low: list, med: list = None) -> int:
    tl = text.lower()
    high_hits = sum(1 for kw in high if kw in tl)
    low_hits  = sum(1 for kw in low  if kw in tl)
    med_hits  = sum(1 for kw in (med or []) if kw in tl) if med else 0

    if high_hits >= 3:
        return 5
    elif high_hits >= 1 and low_hits == 0:
        return 4 if med_hits >= 1 else 3
    elif high_hits >= 1 and low_hits >= 1:
        return 2
    elif med_hits >= 2:
        return 3
    elif low_hits >= 2:
        return 1
    else:
        return 2  # neutral default


def score_entity(filepath: Path) -> Score:
    try:
        text = filepath.read_text(encoding="utf-8", errors="ignore")[:PREVIEW_CHARS]
    except Exception:
        text = ""

    full_text = filepath.name + " " + text

    m = score_keywords(full_text, MARKET_HIGH, [], MARKET_MED)
    s = score_keywords(full_text, SPEED_HIGH, SPEED_LOW)
    o = score_keywords(full_text, MOAT_HIGH, MOAT_LOW)
    u = score_keywords(full_text, UNFAIR_HIGH, [])

    total = m + s + o + u
    preview = text[:120].replace("\n", " ").strip()

    return Score(
        filename=filepath.stem,
        m=m, s=s, o=o, u=u,
        total=total,
        preview=preview
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"[*] Scanning: {ENTITIES_DIR}")
    files = sorted(ENTITIES_DIR.glob("*.md"))
    print(f"[*] Found {len(files)} entity files")

    scores = []
    for f in files:
        scores.append(score_entity(f))

    scores.sort(key=lambda x: x.total, reverse=True)

    top20  = [s for s in scores if s.total >= 18]
    top50  = [s for s in scores if 16 <= s.total < 18]
    backlog = [s for s in scores if s.total < 16]

    # If top20 has fewer than 20, pull from top50
    if len(top20) < 20:
        needed = 20 - len(top20)
        top20 = top20 + top50[:needed]
        top50 = top50[needed:]

    # Cap top50 list at 50
    top50 = [s for s in scores if s not in top20][:50]

    print(f"[*] Top 20 candidates: {len(top20)}")
    print(f"[*] Top 50 (extended): {len(top50)}")
    print(f"[*] Backlog: {len(backlog)}")

    # Build markdown output
    lines = [
        "# Triage Scoring Matrix — MSOU Rubric",
        f"**Generated:** 2026-08-18 | **Model:** GPT-OSS 120B | **Entities Scored:** {len(files)}",
        "",
        "**Scoring:** M=Market(1-5) S=Speed(1-5) O=Moat(1-5) U=Unfair Advantage(1-5) | Max=20",
        "",
        "---",
        "",
        "## TOP 20 — Priority Targets (Score 18+)",
        "These are the immediate H100 burst synthesis targets.",
        "",
        "| Rank | Entity | M | S | O | U | Total | Preview |",
        "|------|--------|---|---|---|---|-------|---------|",
    ]
    for i, s in enumerate(top20, 1):
        preview = s.preview[:60].replace("|", "/")
        lines.append(f"| {i} | `{s.filename}` | {s.m} | {s.s} | {s.o} | {s.u} | **{s.total}** | {preview} |")

    lines += [
        "",
        "---",
        "",
        "## TOP 51-100 — High Potential Backlog (Score 16-17)",
        "Review after Top 20 are executed. Strong candidates for Phase 2 expansion.",
        "",
        "| Rank | Entity | M | S | O | U | Total |",
        "|------|--------|---|---|---|---|-------|",
    ]
    for i, s in enumerate(top50, 21):
        lines.append(f"| {i} | `{s.filename}` | {s.m} | {s.s} | {s.o} | {s.u} | {s.total} |")

    lines += [
        "",
        "---",
        "",
        f"## Full Corpus Tail ({len(backlog)} entities score < 16)",
        "Not prioritized for this cycle. Revisit post-funding.",
        "",
        "| Entity | Total |",
        "|--------|-------|",
    ]
    for s in backlog[:100]:  # show first 100 for readability
        lines.append(f"| `{s.filename}` | {s.total} |")
    if len(backlog) > 100:
        lines.append(f"| *(+{len(backlog)-100} more not shown)* | — |")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"[+] Written: {OUTPUT_FILE}")
    print(f"\n=== TOP 20 PREVIEW ===")
    for i, s in enumerate(top20, 1):
        print(f"  {i:2}. [{s.total}/20] {s.filename}")
    print("======================")


if __name__ == "__main__":
    main()
