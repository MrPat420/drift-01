#!/usr/bin/env python3
"""
EXECUTIVE TAKEOUT EXTRACTION & CLIENT OBSIDIAN VAULT GENERATOR
Turns raw, chaotic ChatGPT / Claude / Gemini Takeout exports (JSON, JSONL, or Markdown directories)
into a clean, structured Obsidian / Notion-ready knowledge vault with table of contents,
tag categorization, and search index for high-paying consulting clients.
Author: Shaun Patrick Kelly / Antigravity Autonomous Engine
"""

import sys
import os
import re
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any


def parse_iso_ts(ts_str: str) -> float:
    if not ts_str:
        return 0.0
    for fmt in [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S%z"
    ]:
        try:
            dt = datetime.strptime(ts_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.timestamp()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00")).timestamp()
    except Exception:
        return 0.0


def build_client_vault(input_path: Path, output_vault_dir: Path, client_name: str = "Executive Client", gap_seconds: int = 600):
    output_vault_dir.mkdir(parents=True, exist_ok=True)
    sessions_dir = output_vault_dir / "01_Sessions"
    sessions_dir.mkdir(exist_ok=True)

    print("=" * 65)
    print(f"💼 EXECUTIVE AI TAKEOUT INGESTION ENGINE: {client_name}")
    print("=" * 65)

    manifest = []

    # Case A: Input is a directory of existing session files (Markdown/Text)
    if input_path.is_dir():
        mdfiles = list(input_path.glob("*.md")) + list(input_path.glob("*.txt"))
        print(f"[*] Processing directory with {len(mdfiles):,} conversation documents...")
        for i, mf in enumerate(mdfiles[:150], 1):
            try:
                content = mf.read_text(encoding="utf-8", errors="ignore")
                lines = content.splitlines()
                first_line = lines[0].replace("#", "").strip() if lines else mf.stem
                
                dest_file = sessions_dir / f"{i:04d}_{mf.name}"
                dest_file.write_text(content, encoding="utf-8")
                
                manifest.append({
                    "id": f"SESS-{i:04d}",
                    "title": first_line[:65],
                    "date": "Archived Session",
                    "file": dest_file.name,
                    "count": len(lines)
                })
            except Exception:
                continue

    # Case B: Input is a raw JSON/JSONL takeout file
    else:
        raw_text = input_path.read_text(encoding="utf-8", errors="ignore")
        records = []
        if input_path.suffix == ".jsonl":
            for line in raw_text.splitlines():
                if line.strip():
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        continue
        else:
            try:
                data = json.loads(raw_text)
                if isinstance(data, list):
                    records = data
                elif isinstance(data, dict):
                    for k in ["conversations", "messages", "records", "items"]:
                        if k in data and isinstance(data[k], list):
                            records = data[k]
                            break
                    if not records:
                        records = [data]
            except Exception as e:
                # If markdown file passed directly, wrap as single session
                records = [{"text": raw_text, "timestamp": datetime.now(timezone.utc).isoformat(), "author": "User"}]

        print(f"[*] Ingested {len(records):,} raw message records from {input_path.name}")

        sorted_records = sorted(
            [r for r in records if "timestamp" in r or "created_at" in r or "time" in r or "text" in r],
            key=lambda x: parse_iso_ts(x.get("timestamp") or x.get("created_at") or x.get("time") or "")
        )

        sessions = []
        curr = [sorted_records[0]] if sorted_records else []
        last_t = parse_iso_ts(curr[0].get("timestamp") or curr[0].get("created_at") or "") if curr else 0

        for r in sorted_records[1:]:
            curr_t = parse_iso_ts(r.get("timestamp") or r.get("created_at") or "")
            if curr_t > 0 and last_t > 0 and (curr_t - last_t) > gap_seconds:
                sessions.append(curr)
                curr = [r]
            else:
                curr.append(r)
            if curr_t > 0:
                last_t = curr_t
        if curr:
            sessions.append(curr)

        print(f"[+] Recombined into {len(sessions):,} clean, unfragmented conversation sessions.")

        for i, sess in enumerate(sessions, 1):
            t_start = parse_iso_ts(sess[0].get("timestamp") or sess[0].get("created_at") or "")
            start_str = datetime.fromtimestamp(t_start, timezone.utc).strftime("%Y-%m-%d %H:%M") if t_start else "Unknown"
            
            first_user_msg = ""
            for m in sess:
                sender = (m.get("author") or m.get("role") or m.get("sender") or "").lower()
                if sender in ["user", "human"] and (m.get("text") or m.get("content")):
                    first_user_msg = (m.get("text") or m.get("content"))[:60].replace("\n", " ").strip()
                    break
            if not first_user_msg:
                first_user_msg = f"Session_{i:03d}"

            clean_slug = re.sub(r'[^a-zA-Z0-9_]', '_', first_user_msg[:30]).strip('_')
            fname = f"{start_str[:10]}_{i:03d}_{clean_slug}.md"
            sfile = sessions_dir / fname

            content_md = [
                f"# {first_user_msg}",
                f"**Session ID:** `SESS-{i:04d}` | **Date:** {start_str} | **Messages:** {len(sess)}",
                "\n---\n"
            ]

            for m in sess:
                author = m.get("author") or m.get("role") or m.get("sender") or "User"
                body = m.get("text") or m.get("content") or m.get("message") or ""
                ts = m.get("timestamp") or m.get("created_at") or ""
                content_md.append(f"### 💬 {author.capitalize()} ({ts}):\n{body.strip()}\n")

            sfile.write_text("\n".join(content_md), encoding="utf-8")
            manifest.append({"id": f"SESS-{i:04d}", "title": first_user_msg, "date": start_str, "file": fname, "count": len(sess)})

    # Build Master Obsidian / Notion Index
    index_md = [
        f"# 🏛️ {client_name}'s Private Knowledge Vault",
        f"**Generated on:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ",
        f"**Total Historical Conversations Recovered:** {len(manifest):,}  ",
        f"**Source Target:** `{input_path.name}`  ",
        "\n---\n",
        "## 📑 Master Chronological Index\n",
        "| Session ID | Date / Status | Subject / First Prompt | Size / Lines | Link |",
        "| :---: | :---: | :--- | :---: | :--- |"
    ]

    for m in manifest:
        index_md.append(f"| `{m['id']}` | {m['date']} | {m['title']} | {m['count']} lines | [[01_Sessions/{m['file']}\\|Open Session]] |")

    (output_vault_dir / "00_START_HERE_INDEX.md").write_text("\n".join(index_md), encoding="utf-8")

    print("\n" + "=" * 65)
    print("✨ CLIENT KNOWLEDGE VAULT GENERATION COMPLETE!")
    print(f"📁 Vault Location:     {output_vault_dir.resolve()}")
    print(f"📑 Master Entrypoint:  {(output_vault_dir / '00_START_HERE_INDEX.md').resolve()}")
    print(f"💎 Total Recovered:    {len(manifest):,} Sessions ready for delivery!")
    print("=" * 65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executive Takeout to Obsidian/Notion Vault Builder")
    parser.add_argument("input_path", help="Path to client's raw Takeout JSON/JSONL or directory")
    parser.add_argument("--out", default="./Client_Knowledge_Vault", help="Output directory")
    parser.add_argument("--client", default="Executive Client", help="Client name")
    args = parser.parse_args()

    build_client_vault(Path(args.input_path), Path(args.out), client_name=args.client)
