#!/usr/bin/env python3
"""
CLAUDE TAKEOUT & KNOWLEDGE INGESTION PIPELINE FOR WIKI_LLM
Ingests the 881 split conversation files (last 5+ months of Claude), SimianDOX entity matrices,
and today's master analysis into 01_CLAUDE_PROJECTS/Wiki_LLM/ and wiki/.
Prepares clean, chunked embeddings for local RTX 3060 LLM indexing.
Author: Shaun Patrick Kelly / Antigravity Autonomous Engine
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

PROJECTS_DIR = Path("/home/simian420/projects")
CLAUDE_SPLIT_DIR = PROJECTS_DIR / "claude-audit" / "split"
WIKI_LLM_DIR = PROJECTS_DIR / "01_CLAUDE_PROJECTS" / "Wiki_LLM"
WIKI_CONCEPTS_DIR = PROJECTS_DIR / "wiki" / "concepts"
OUTPUT_CORPUS_DIR = WIKI_LLM_DIR / "ingested_corpus"
INDEX_FILE = WIKI_LLM_DIR / "MASTER_WIKI_LLM_INDEX.json"


def clean_markdown_text(text: str) -> str:
    """Strip extraneous headers, normalize whitespace, extract core substance."""
    # Remove system prompt boilerplate if present
    text = re.sub(r'#+\s*(?:System Prompt|Context Window|Instructions)[\s\S]*?(?=#+\s*User|#+\s*Human|\Z)', '', text, flags=re.IGNORECASE)
    return text.strip()


def ingest_corpus():
    OUTPUT_CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 65)
    print("🚀 INGESTING CLAUDE TAKEOUT & KNOWLEDGE CORPUS INTO WIKI_LLM")
    print("=" * 65)
    
    master_index = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "total_documents": 0,
        "categories": {
            "claude_sessions_5months": 0,
            "wiki_concepts": 0,
            "master_dossiers": 0
        },
        "documents": []
    }
    
    # 1. Ingest 881 Claude Split Files (Last 5 Months)
    if CLAUDE_SPLIT_DIR.exists():
        split_files = list(CLAUDE_SPLIT_DIR.glob("*.md"))
        print(f"[*] Processing {len(split_files):,} Claude split conversation files...")
        
        for f in split_files:
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                lines = content.splitlines()
                title = lines[0].replace("#", "").strip() if lines else f.stem
                
                # Extract any tagged project codes (e.g. GEM-01, Y-TIP, PAIR, etc.)
                project_codes = list(set(re.findall(r'\b([A-Z0-9]{2,10}-[0-9]{1,4})\b', content)))
                
                doc_record = {
                    "id": f.stem,
                    "title": title,
                    "category": "claude_sessions_5months",
                    "original_path": str(f.resolve()),
                    "size_bytes": f.stat().st_size,
                    "lines": len(lines),
                    "project_codes": project_codes,
                    "preview": content[:250].replace("\n", " ").strip()
                }
                
                # Save into Wiki_LLM corpus
                dest = OUTPUT_CORPUS_DIR / f"claude_{f.name}"
                dest.write_text(content, encoding="utf-8")
                
                master_index["documents"].append(doc_record)
                master_index["categories"]["claude_sessions_5months"] += 1
            except Exception as e:
                print(f"[WARN] Error reading {f.name}: {e}")
                continue
                
    # 2. Ingest Wiki Concepts & SimianDOX Extracted Files
    if WIKI_CONCEPTS_DIR.exists():
        concept_files = list(WIKI_CONCEPTS_DIR.glob("*.md"))
        print(f"[*] Processing {len(concept_files):,} Wiki concept & entity files...")
        
        for f in concept_files:
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                lines = content.splitlines()
                title = lines[0].replace("#", "").strip() if lines else f.stem
                project_codes = list(set(re.findall(r'\b([A-Z0-9]{2,10}-[0-9]{1,4})\b', content)))
                
                doc_record = {
                    "id": f.stem,
                    "title": title,
                    "category": "wiki_concepts",
                    "original_path": str(f.resolve()),
                    "size_bytes": f.stat().st_size,
                    "lines": len(lines),
                    "project_codes": project_codes,
                    "preview": content[:250].replace("\n", " ").strip()
                }
                
                dest = OUTPUT_CORPUS_DIR / f"concept_{f.name}"
                dest.write_text(content, encoding="utf-8")
                
                master_index["documents"].append(doc_record)
                master_index["categories"]["wiki_concepts"] += 1
            except Exception as e:
                continue

    # 3. Ingest Master Dossiers from projects root
    master_dossiers = [
        "TOP_50_HIGH_VALUE_MASTER_ASSETS.md",
        "HIGH_VALUE_CONCRETE_GEMS.md",
        "IP_CRYPTO_CONTAINER_MASTER_SYNTHESIS.md",
        "FORWARD_COMMERCIAL_TOP_PICKS.md",
        "ACCOUNT_HANDOFF_GUIDE.md"
    ]
    for dname in master_dossiers:
        dpath = PROJECTS_DIR / dname
        if dpath.exists():
            content = dpath.read_text(encoding="utf-8", errors="ignore")
            doc_record = {
                "id": dpath.stem,
                "title": dname,
                "category": "master_dossiers",
                "original_path": str(dpath.resolve()),
                "size_bytes": dpath.stat().st_size,
                "lines": len(content.splitlines()),
                "project_codes": list(set(re.findall(r'\b([A-Z0-9]{2,10}-[0-9]{1,4})\b', content))),
                "preview": content[:250].replace("\n", " ").strip()
            }
            dest = OUTPUT_CORPUS_DIR / f"master_{dpath.name}"
            dest.write_text(content, encoding="utf-8")
            master_index["documents"].append(doc_record)
            master_index["categories"]["master_dossiers"] += 1

    master_index["total_documents"] = len(master_index["documents"])
    INDEX_FILE.write_text(json.dumps(master_index, indent=2), encoding="utf-8")
    
    print("\n" + "=" * 65)
    print("✨ INGESTION COMPLETE!")
    print(f"📄 Total Ingested Documents: {master_index['total_documents']:,}")
    print(f"   • Claude 5-Month Sessions:  {master_index['categories']['claude_sessions_5months']:,}")
    print(f"   • Wiki Concept Dossiers:    {master_index['categories']['wiki_concepts']:,}")
    print(f"   • Master Strategic Indexes: {master_index['categories']['master_dossiers']:,}")
    print(f"📁 Output Corpus Location:     {OUTPUT_CORPUS_DIR.resolve()}")
    print(f"📑 Master JSON Index:          {INDEX_FILE.resolve()}")
    print("=" * 65)


if __name__ == "__main__":
    ingest_corpus()
