#!/usr/bin/env python3
"""
UNIVERSAL TAKEOUT PARSER & TIME-GAP CLUSTERING ENGINE
Unfragments raw Google/Claude/ChatGPT takeout export files into clean, chronologically clustered conversations.
Heuristic: 10-minute (600s) inactivity window clustering.
Author: Shaun Patrick Kelly / Antigravity Autonomous Engine
"""

import sys
import os
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any


def parse_timestamp(ts_str: str) -> float:
    """Parse various ISO and RFC timestamps to epoch seconds."""
    if not ts_str:
        return 0.0
    for fmt in [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z"
    ]:
        try:
            dt = datetime.strptime(ts_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.timestamp()
        except ValueError:
            continue
    try:
        # Fallback for ISO format
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00")).timestamp()
    except Exception:
        return 0.0


def cluster_fragments(records: List[Dict[str, Any]], gap_seconds: int = 600) -> List[List[Dict[str, Any]]]:
    """Cluster raw conversation fragments using time-gap boundary heuristic."""
    # Filter and sort by timestamp
    sorted_records = sorted(
        [r for r in records if "timestamp" in r or "created_at" in r or "time" in r],
        key=lambda x: parse_timestamp(x.get("timestamp") or x.get("created_at") or x.get("time") or "")
    )
    
    if not sorted_records:
        return []
        
    sessions = []
    current_session = [sorted_records[0]]
    last_time = parse_timestamp(sorted_records[0].get("timestamp") or sorted_records[0].get("created_at") or sorted_records[0].get("time") or "")
    
    for rec in sorted_records[1:]:
        curr_time = parse_timestamp(rec.get("timestamp") or rec.get("created_at") or rec.get("time") or "")
        
        # If time gap > threshold, split into new session
        if curr_time > 0 and last_time > 0 and (curr_time - last_time) > gap_seconds:
            sessions.append(current_session)
            current_session = [rec]
        else:
            current_session.append(rec)
            
        if curr_time > 0:
            last_time = curr_time
            
    if current_session:
        sessions.append(current_session)
        
    return sessions


def format_session_to_markdown(session_idx: int, session: List[Dict[str, Any]]) -> str:
    """Format a clustered session into clean readable Markdown."""
    first_time_ts = parse_timestamp(session[0].get("timestamp") or session[0].get("created_at") or session[0].get("time") or "")
    last_time_ts = parse_timestamp(session[-1].get("timestamp") or session[-1].get("created_at") or session[-1].get("time") or "")
    
    start_str = datetime.fromtimestamp(first_time_ts, timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC") if first_time_ts else "Unknown"
    end_str = datetime.fromtimestamp(last_time_ts, timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC") if last_time_ts else "Unknown"
    
    md = [
        f"# Session {session_idx:04d}",
        f"**Start Time:** {start_str}  ",
        f"**End Time:** {end_str}  ",
        f"**Message Count:** {len(session)}  ",
        "\n---\n"
    ]
    
    for msg in session:
        sender = msg.get("author") or msg.get("role") or msg.get("sender") or "User"
        text = msg.get("text") or msg.get("content") or msg.get("message") or ""
        ts = msg.get("timestamp") or msg.get("created_at") or ""
        
        md.append(f"### 💬 {sender.capitalize()} ({ts}):")
        md.append(f"{text.strip()}\n")
        
    return "\n".join(md)


def process_takeout_file(input_file: Path, output_dir: Path, gap_seconds: int = 600):
    """Process a raw JSON or JSONL takeout file into clustered sessions."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    raw_text = input_file.read_text(encoding="utf-8", errors="ignore")
    records = []
    
    if input_file.suffix == ".jsonl":
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
                # Check common takeout keys
                for k in ["conversations", "messages", "records", "items"]:
                    if k in data and isinstance(data[k], list):
                        records = data[k]
                        break
                if not records:
                    records = [data]
        except Exception as e:
            print(f"Error parsing JSON {input_file}: {e}")
            return
            
    print(f"Loaded {len(records):,} raw fragments from {input_file.name}")
    sessions = cluster_fragments(records, gap_seconds=gap_seconds)
    print(f"Successfully recombined into {len(sessions):,} coherent conversation sessions.")
    
    for i, s in enumerate(sessions, 1):
        md_content = format_session_to_markdown(i, s)
        out_file = output_dir / f"session_{i:04d}.md"
        out_file.write_text(md_content, encoding="utf-8")
        
    print(f"Delivered {len(sessions)} markdown sessions to {output_dir.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Takeout Time-Gap Clustering Parser")
    parser.add_argument("input_file", type=str, help="Path to raw takeout JSON/JSONL")
    parser.add_argument("--out", type=str, default="./unfragmented_sessions", help="Output directory")
    parser.add_argument("--gap", type=int, default=600, help="Time gap threshold in seconds (default 600s / 10 min)")
    args = parser.parse_args()
    
    process_takeout_file(Path(args.input_file), Path(args.out), gap_seconds=args.gap)
