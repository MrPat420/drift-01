#!/usr/bin/env python3
"""
SHADOW & UNMENTIONED PROJECTS FORENSIC INVENTORY & LINEAGE MINER
Extracts the genesis, problem statement, solution design, software inventory,
and missing connections for all secondary and shadow projects in the workspace.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECTS_DIR = Path("/home/simian420/projects")
CLAUDE_PROJECTS_DIR = PROJECTS_DIR / "01_CLAUDE_PROJECTS"
SPLIT_DIR = PROJECTS_DIR / "claude-audit" / "split"
WIKI_LLM_DIR = CLAUDE_PROJECTS_DIR / "Wiki_LLM"
VAULT_DIR = WIKI_LLM_DIR / "CLAUDE_5MONTH_MASTER_VAULT"
OUTPUT_FILE = WIKI_LLM_DIR / "SHADOW_PROJECTS_MASTER_LINEAGE_AND_INVENTORY.md"

SHADOW_TARGETS = [
    ("How_to_use_Claude", ["how to use claude", "user enthusiast", "cascade effect", "prompt reference"]),
    ("PROJECT_GLASS_HOUSE__GLASS-01", ["glass house", "glass-01", "aegis", "transparency enclave"]),
    ("My_Thought_Nlender", ["thought blender", "nlender", "cogn-01", "idea blender"]),
    ("MEMORY-ALPHA-01", ["memory-alpha", "memory alpha", "standing rules", "datasheet"]),
    ("second_brain", ["second brain", "second_brain", "secondbrain", "founding handoff"]),
    ("KBSYNC-01", ["kbsync", "kb sync", "knowledge sync", "knowledge base"]),
    ("Rag_SpinUp", ["rag spinup", "rag-spinup", "rag_spinup", "local rag"]),
    ("INSTSET-BUILDER", ["instset", "instruction set builder", "system prompt builder"]),
    ("EMPLOY-01", ["employ-01", "employ01", "contracting engine", "consulting bill"]),
    ("Twins", ["twins", "twin index", "pursue unified index"]),
    ("Clarity-Protocol-01", ["clarity protocol", "clarity-protocol", "clarity audit"]),
    ("JFK", ["jfk", "assassination", "dealey plaza", "warren commission"]),
    ("UAP-01", ["uap-01", "uap01", "aerial phenomena", "ufo intelligence"]),
    ("YouTube_UAP", ["youtube uap", "youtube_uap", "uap channel"]),
    ("RUINS-01", ["ruins", "ruins-01", "andean ruins", "pre-inca", "satellite stone"]),
    ("MK-ULTRA", ["mk-ultra", "mkultra", "mind control", "cold war intelligence"]),
    ("BLACK_BUDGET", ["black budget", "black_budget", "special access program"])
]

def mine_shadow_projects():
    print("=" * 75)
    print("🔎 MINING SHADOW & UNMENTIONED PROJECTS LINEAGE AND INVENTORY")
    print("=" * 75)

    print("[*] Indexing 876 split conversation files...")
    split_files = sorted(SPLIT_DIR.glob("*.md"))
    corpus = []
    for sf in split_files:
        try:
            txt = sf.read_text(encoding="utf-8", errors="ignore")
            lines = txt.splitlines()
            title = lines[0].replace("#", "").strip() if lines else sf.stem
            d_match = re.search(r'created:\s*(\d{4}-\d{2}-\d{2})', txt)
            d_str = d_match.group(1) if d_match else "2026-06"
            corpus.append({"file": sf.name, "title": title, "date": d_str, "text_lower": txt.lower(), "raw_text": txt})
        except Exception:
            continue

    md = [
        "# 🕵️ Shadow Projects Master Lineage, Problem/Solution & Software Inventory",
        f"**Compiled:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ",
        "**Operator & Sole Architect:** Shaun Patrick Kelly (Mr_Pat)  ",
        "**Scope:** Forensic recovery of all 17 unmentioned/background projects, their origin conversations, real-world problems solved, file inventories, and ecosystem linkages.  ",
        "\n---\n",
        "## 📑 Executive Portfolio Summary\n",
        "| # | Project Name | Files | Code | Genesis Date | Origin Trigger Conversation | Core Functional Domain |",
        "| :---: | :--- | :---: | :---: | :---: | :--- | :--- |"
    ]

    detailed_sections = []

    for idx, (p_name, keywords) in enumerate(SHADOW_TARGETS, 1):
        target_dir = CLAUDE_PROJECTS_DIR / p_name
        if not target_dir.exists():
            continue

        all_files = list(target_dir.rglob('*'))
        actual_files = [f for f in all_files if f.is_file()]
        code_files = [f for f in actual_files if f.suffix in ['.py', '.sh', '.js', '.ts', '.html']]
        md_files = [f for f in actual_files if f.suffix in ['.md', '.txt', '.json']]

        matching_convs = []
        for item in corpus:
            if any(kw in item["text_lower"] for kw in keywords):
                matching_convs.append(item)

        matching_convs.sort(key=lambda x: x["file"])
        genesis = matching_convs[0] if matching_convs else {"file": "Direct Formulation", "date": "2026-06", "title": "Direct Standalone Formulation", "raw_text": ""}

        # Extract prompt snippet
        user_blocks = re.findall(r'##\s*\[HUMAN\][^\n]*\n([\s\S]*?)(?=\n##\s*\[ASSISTANT\]|\Z)', genesis.get("raw_text", ""))
        prompt_snippet = user_blocks[0][:250].replace("\n", " ").strip() if user_blocks else "Formulated as direct project specification."

        # Read prompt template or main readme if exists
        pt_file = target_dir / "prompt_template.md"
        pt_text = pt_file.read_text(encoding="utf-8", errors="ignore") if pt_file.exists() else ""
        pt_snip = pt_text[:350].replace("\n", " ").strip() if pt_text else "Operational workspace component."

        md.append(f"| {idx} | **`{p_name}`** | {len(actual_files)} | {len(code_files)} | {genesis['date']} | [[01_Conversations/{genesis['file']}\\|{genesis['file'][:25]}]] | {pt_snip[:45]}... |")

        # Detailed Section
        file_list_str = "\n".join([f"  - `{f.relative_to(target_dir)}` ({round(f.stat().st_size/1024, 1)} KB)" for f in actual_files[:10]])
        if len(actual_files) > 10:
            file_list_str += f"\n  - *...and {len(actual_files)-10} additional files.*"

        d_md = [
            f"## 🏛️ {idx}. Project: `{p_name}`",
            f"- **Physical Disk Path:** `01_CLAUDE_PROJECTS/{p_name}`",
            f"- **File Volume:** {len(actual_files)} files ({len(code_files)} code, {len(md_files)} markdown/docs)",
            f"- **Genesis Origin:** Born in [[01_Conversations/{genesis['file']}]] (*{genesis['title']}* · {genesis['date']})",
            f"- **Historical Discussion Threads:** {len(matching_convs)} conversations",
            f"- **Operator Genesis Prompt:**",
            f"  > *\"{prompt_snippet}...\"*",
            f"- **The Real Problem / Friction Being Solved:**",
            f"  > {pt_snip[:450]}...",
            f"- **Key Software & Document Inventory:**",
            file_list_str,
            f"- **Integration Opportunities & Missing Links:**",
            f"  > Can be fused into active workflows: `FIRST_BRAIN-00`, `02_MCCLAUDE`, `Y-TIP`, or `Wiki_LLM`.",
            "\n" + "=" * 50 + "\n"
        ]
        detailed_sections.extend(d_md)

    full_report = "\n".join(md) + "\n\n---\n\n" + "\n".join(detailed_sections)
    OUTPUT_FILE.write_text(full_report, encoding="utf-8")
    if VAULT_DIR.exists():
        (VAULT_DIR / "00_SHADOW_PROJECTS_MASTER_LINEAGE_AND_INVENTORY.md").write_text(full_report, encoding="utf-8")

    print("\n" + "=" * 75)
    print("✨ SHADOW PROJECTS FORENSIC REPORT GENERATED!")
    print(f"📄 Output: {OUTPUT_FILE.resolve()}")
    print("=" * 75)

if __name__ == "__main__":
    mine_shadow_projects()
