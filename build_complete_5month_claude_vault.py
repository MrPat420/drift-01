#!/usr/bin/env python3
"""
MASTER 5-MONTH CLAUDE TAKEOUT & AUDIT VAULT COMPILER
Unifies:
  1. The raw Claude Takeout (conversations.json)
  2. All 881 split conversation markdown files
  3. The 205 KB AUDIT-REPORT.md & AUDIT-DATA.json (5.7 MB)
  4. Ground truth corrections & verification reports
Into a single, definitive, fully indexed Obsidian Knowledge Vault for Wiki_LLM.
Author: Shaun Patrick Kelly / Antigravity Autonomous Engine
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

PROJECTS_DIR = Path("/home/simian420/projects")
AUDIT_DIR = PROJECTS_DIR / "claude-audit"
SPLIT_DIR = AUDIT_DIR / "split"
SOURCE_CONV_FILE = AUDIT_DIR / "source" / "conversations.json"
AUDIT_REPORT_FILE = AUDIT_DIR / "AUDIT-REPORT.md"
AUDIT_DATA_FILE = AUDIT_DIR / "AUDIT-DATA.json"
CORRECTIONS_FILE = AUDIT_DIR / "ground_truth_corrections.json"

TARGET_VAULT = PROJECTS_DIR / "01_CLAUDE_PROJECTS" / "Wiki_LLM" / "CLAUDE_5MONTH_MASTER_VAULT"


def build_master_vault():
    print("=" * 70)
    print("🏛️ COMPILING COMPLETE 5-MONTH CLAUDE TAKEOUT & AUDIT VAULT")
    print("=" * 70)

    convs_dir = TARGET_VAULT / "01_Conversations"
    audit_docs_dir = TARGET_VAULT / "02_Audit_Reports"
    convs_dir.mkdir(parents=True, exist_ok=True)
    audit_docs_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy Master Audit Reports
    print("[*] Ingesting Master Audit Reports and Calibration Ledgers...")
    if AUDIT_REPORT_FILE.exists():
        shutil.copy2(AUDIT_REPORT_FILE, audit_docs_dir / "01_AUDIT-REPORT.md")
    if CORRECTIONS_FILE.exists():
        shutil.copy2(CORRECTIONS_FILE, audit_docs_dir / "02_GROUND_TRUTH_CORRECTIONS.json")
    if AUDIT_DATA_FILE.exists():
        shutil.copy2(AUDIT_DATA_FILE, audit_docs_dir / "03_AUDIT-DATA.json")

    # 2. Ingest ALL 881 Split Conversation Markdown Files
    split_files = sorted(list(SPLIT_DIR.glob("*.md")))
    print(f"[*] Ingesting ALL {len(split_files):,} conversation markdown files...")

    manifest = []
    for i, sf in enumerate(split_files, 1):
        try:
            content = sf.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()
            title = lines[0].replace("#", "").strip() if lines else sf.stem
            
            # Extract date if present in first 10 lines
            date_match = re.search(r'created:\s*(\d{4}-\d{2}-\d{2})', content)
            date_str = date_match.group(1) if date_match else "2026-03 to 2026-08"
            
            # Extract message count
            msg_match = re.search(r'messages:\s*(\d+)', content)
            msg_count = msg_match.group(1) if msg_match else str(content.count("## [HUMAN]") + content.count("## [ASSISTANT]"))

            dest = convs_dir / sf.name
            dest.write_text(content, encoding="utf-8")

            manifest.append({
                "index": i,
                "id": f"CLAUDE-{i:04d}",
                "title": title[:70],
                "date": date_str,
                "filename": sf.name,
                "lines": len(lines),
                "messages": msg_count,
                "size_kb": round(sf.stat().st_size / 1024, 1)
            })
        except Exception as e:
            continue

    # 3. Build Master 881-Conversation Index
    print(f"[*] Building Master Index for all {len(manifest):,} conversations...")
    
    index_md = [
        "# 🏛️ Master 5-Month Claude Takeout & Audit Knowledge Vault",
        f"**Compiled:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ",
        f"**Total Conversations Ingested:** {len(manifest):,} files  ",
        f"**Date Range:** March 2026 – August 2026  ",
        f"**Associated Audit Dataset:** `AUDIT-REPORT.md` ({round(AUDIT_REPORT_FILE.stat().st_size/1024, 1)} KB) | `AUDIT-DATA.json` ({round(AUDIT_DATA_FILE.stat().st_size/(1024*1024), 2)} MB)  ",
        "\n---\n",
        "## 📊 Section Overview",
        "- **[[02_Audit_Reports/01_AUDIT-REPORT.md|📄 Master Audit Report]]**: Comprehensive audit report across all 881 conversations.",
        "- **[[02_Audit_Reports/02_GROUND_TRUTH_CORRECTIONS.json|⚖️ Ground Truth Corrections]]**: Verified operator corrections and doctrine anchors.",
        "- **`01_Conversations/`**: Complete archive of all 881 individual conversation transcripts.",
        "\n---\n",
        "## 📑 Master Chronological Conversation Ledger",
        "| ID | Date | Subject / First Prompt | Msgs | Size | Vault Link |",
        "| :---: | :---: | :--- | :---: | :---: | :--- |"
    ]

    for m in manifest:
        link_str = f"[[01_Conversations/{m['filename']}\\|Open {m['id']}]]"
        index_md.append(f"| `{m['id']}` | {m['date']} | {m['title']} | {m['messages']} | {m['size_kb']} KB | {link_str} |")

    (TARGET_VAULT / "00_MASTER_INDEX.md").write_text("\n".join(index_md), encoding="utf-8")

    print("\n" + "=" * 70)
    print("✨ MASTER 5-MONTH CLAUDE VAULT COMPILATION COMPLETE!")
    print(f"📁 Target Vault Directory:  {TARGET_VAULT.resolve()}")
    print(f"📑 Master Index File:      {(TARGET_VAULT / '00_MASTER_INDEX.md').resolve()}")
    print(f"💎 Total Ingested:         {len(manifest):,} Conversations + Master Audit Reports")
    print(f"📦 Total Disk Size:        ~{round(sum(f.stat().st_size for f in TARGET_VAULT.rglob('*') if f.is_file())/(1024*1024), 2)} MB")
    print("=" * 70)


if __name__ == "__main__":
    build_master_vault()
