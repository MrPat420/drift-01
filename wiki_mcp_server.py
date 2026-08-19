#!/usr/bin/env python3
"""
SOVEREIGN THINK-TANK WIKI MCP SERVER
FastMCP Model Context Protocol Server for programmatic access to the 1,435+ Entity Wiki,
Concept Papers, and Codebases.
Author: Shaun Patrick Kelly / Antigravity Autonomous Engine
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional

try:
    from fastmcp import FastMCP
except ImportError:
    # Fallback minimal server interface if FastMCP is loading
    class FastMCP:
        def __init__(self, name):
            self.name = name
            self.tools = {}
        def tool(self):
            def decorator(f):
                self.tools[f.__name__] = f
                return f
            return decorator
        def run(self):
            print(f"[{self.name}] Running in stdio mode with {len(self.tools)} tools.")

# Initialize the MCP Server
mcp = FastMCP("sovereign-thinktank-wiki")

PROJECTS_DIR = Path("/home/simian420/projects")
WIKI_DIR = PROJECTS_DIR / "wiki"
ENTITIES_DIR = WIKI_DIR / "entities"
CONCEPTS_DIR = WIKI_DIR / "concepts"


@mcp.tool()
def search_wiki(query: str, search_type: str = "all", limit: int = 15) -> List[Dict[str, str]]:
    """
    Search across the 1,435+ entity dossiers and concept papers.
    
    Args:
        query: Search keywords or phrases.
        search_type: 'entities', 'concepts', or 'all'.
        limit: Max number of results (default 15).
    """
    results = []
    query_lower = query.lower()
    
    target_dirs = []
    if search_type in ["entities", "all"] and ENTITIES_DIR.exists():
        target_dirs.append(("entity", ENTITIES_DIR))
    if search_type in ["concepts", "all"] and CONCEPTS_DIR.exists():
        target_dirs.append(("concept", CONCEPTS_DIR))
        
    for doc_type, tdir in target_dirs:
        for f in tdir.glob("*.md"):
            name_match = query_lower in f.name.lower()
            snippet = ""
            
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                content_lower = content.lower()
                
                if name_match or query_lower in content_lower:
                    # Find a relevant snippet
                    idx = content_lower.find(query_lower)
                    if idx != -1:
                        start = max(0, idx - 80)
                        end = min(len(content), idx + 180)
                        snippet = content[start:end].replace("\n", " ").strip()
                    else:
                        snippet = content[:150].replace("\n", " ").strip()
                        
                    results.append({
                        "type": doc_type,
                        "filename": f.name,
                        "path": str(f.resolve()),
                        "size_bytes": f.stat().st_size,
                        "snippet": snippet
                    })
            except Exception:
                continue
                
            if len(results) >= limit * 2:
                break
                
    # Sort by exact name match first, then size
    results.sort(key=lambda x: (query_lower in x["filename"].lower(), x["size_bytes"]), reverse=True)
    return results[:limit]


@mcp.tool()
def read_entity(entity_name: str) -> str:
    """
    Read the full content of an entity dossier by name or filename.
    
    Args:
        entity_name: The entity name (e.g. 'MARITIME-AIS-COURSE-DEVIATION-RISK-EVALUATOR' or with .md).
    """
    if not entity_name.endswith(".md"):
        entity_name += ".md"
        
    target = ENTITIES_DIR / entity_name
    if not target.exists():
        # Try case-insensitive fuzzy match
        for f in ENTITIES_DIR.glob("*.md"):
            if entity_name.lower() in f.name.lower():
                target = f
                break
                
    if not target.exists():
        return f"Error: Entity '{entity_name}' not found in {ENTITIES_DIR}."
        
    return target.read_text(encoding="utf-8", errors="ignore")


@mcp.tool()
def read_concept(concept_name: str) -> str:
    """
    Read the full content of a concept synthesis paper by name or filename.
    
    Args:
        concept_name: The concept paper name (e.g. 'sovereign-thinktank-master-plan' or with .md).
    """
    if not concept_name.endswith(".md"):
        concept_name += ".md"
        
    target = CONCEPTS_DIR / concept_name
    if not target.exists():
        for f in CONCEPTS_DIR.glob("*.md"):
            if concept_name.lower() in f.name.lower():
                target = f
                break
                
    if not target.exists():
        return f"Error: Concept paper '{concept_name}' not found in {CONCEPTS_DIR}."
        
    return target.read_text(encoding="utf-8", errors="ignore")


@mcp.tool()
def list_top_assets(category: str = "all") -> List[Dict[str, str]]:
    """
    List the top-ranked commercial and technical assets from the verified master catalog.
    
    Args:
        category: 'creator', 'peru_trade', 'power', 'local_compute', 'forensics', 'maritime', or 'all'.
    """
    master_file = PROJECTS_DIR / "TOP_50_HIGH_VALUE_MASTER_ASSETS.md"
    if not master_file.exists():
        return [{"error": "TOP_50_HIGH_VALUE_MASTER_ASSETS.md not found on disk."}]
        
    text = master_file.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    
    assets = []
    for l in lines:
        if l.strip().startswith("| **") and "|" in l:
            parts = [p.strip() for p in l.split("|")[1:-1]]
            if len(parts) >= 4:
                assets.append({
                    "rank": parts[0].replace("**", ""),
                    "name": parts[1].replace("**", ""),
                    "status": parts[2].replace("**", ""),
                    "description": parts[3].replace("**", ""),
                    "monetization": parts[4].replace("**", "") if len(parts) > 4 else ""
                })
    return assets


@mcp.tool()
def write_wiki_concept(filename: str, content: str, overwrite: bool = False) -> str:
    """
    Write or update a synthesis concept paper inside the wiki/concepts directory.
    
    Args:
        filename: Target markdown filename.
        content: Markdown content to write.
        overwrite: Overwrite existing file if true.
    """
    if not filename.endswith(".md"):
        filename += ".md"
        
    CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)
    target = CONCEPTS_DIR / filename
    
    if target.exists() and not overwrite:
        return f"Error: File '{filename}' already exists and overwrite is False."
        
    target.write_text(content, encoding="utf-8")
    return f"Successfully wrote {len(content):,} characters to {target.resolve()}."


# ----------------------------------------------------------------------
# FastAPI health and entity routes – expose additional REST endpoints on the same FastMCP server.
# ----------------------------------------------------------------------
app = mcp.app  # FastMCP creates an internal FastAPI app instance.

@app.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok"}

@app.get("/entity/{key}")
async def get_entity(key: str) -> str:
    # Reuse existing read_entity tool for consistency.
    return read_entity(key)

@app.get("/entities")
async def list_entities(type: str = "entity", limit: int = 15) -> list:
    # Simple placeholder: return first N entity filenames.
    import os
    entities_path = ENTITIES_DIR
    if not entities_path.exists():
        return []
    files = [f.name for f in entities_path.glob("*.md")][:limit]
    return [{"key": f, "type": type} for f in files]

if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=9000)
    # duplicate line removed
