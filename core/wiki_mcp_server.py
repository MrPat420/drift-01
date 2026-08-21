#!/usr/bin/env python3
"""
WikiBrain MCP Server - G3: The Boundary Persistence Fix (v2)
A local, persistent SQL registry allowing AI agents to store and retrieve
state, IP, and context across session boundaries.
Upgraded via Pathway-B Red-Team (Claude).
"""
import os
import sqlite3
from fastmcp import FastMCP

# Define database location inside the persistent agent directory
DB_PATH = "/home/simian420/projects/.agent/wikibrain.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    
    # GAP #4 Fix: WAL mode for concurrency
    conn.execute('PRAGMA journal_mode=WAL')
    
    cursor = conn.cursor()
    # GAP #3 Fix: Added source and epistemic_status
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entities (
            key TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            tags TEXT,
            source TEXT DEFAULT 'unknown',
            epistemic_status TEXT DEFAULT 'unverified',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Handle schema migration if columns don't exist
    try:
        cursor.execute("ALTER TABLE entities ADD COLUMN source TEXT DEFAULT 'unknown'")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE entities ADD COLUMN epistemic_status TEXT DEFAULT 'unverified'")
    except sqlite3.OperationalError:
        pass
        
    conn.commit()
    conn.close()

init_db()

mcp = FastMCP("WikiBrain")

@mcp.tool()
def add_entity(key: str, content: str, tags: str = "", source: str = "agent", epistemic_status: str = "inference") -> str:
    """
    Saves a persistent memory/entity to the 2nd-Brain.
    Must explicitly define source (e.g. 'claude', 'antigravity', 'user') 
    and epistemic_status ('verified', 'inference', 'estimate').
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO entities (key, content, tags, source, epistemic_status, updated_at) 
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(key) DO UPDATE SET 
        content=excluded.content, 
        tags=excluded.tags, 
        source=excluded.source,
        epistemic_status=excluded.epistemic_status,
        updated_at=CURRENT_TIMESTAMP
    ''', (key, content, tags, source, epistemic_status))
    conn.commit()
    conn.close()
    return f"Successfully saved/updated entity: {key} (Status: {epistemic_status})"

@mcp.tool()
def read_entity(key: str) -> str:
    """
    Retrieves the exact content of an entity by its key.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT content, source, epistemic_status FROM entities WHERE key = ?', (key,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return f"[Source: {result[1]} | Status: {result[2]}]\n\n{result[0]}"
    return f"Entity '{key}' not found in WikiBrain."

@mcp.tool()
def search_brain(query: str) -> str:
    """
    Searches the 2nd-Brain for keys, tags, OR CONTENT matching the query.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    search_term = f"%{query}%"
    
    # GAP #2 Fix: Added content search
    cursor.execute('''
        SELECT key, tags, source, epistemic_status 
        FROM entities 
        WHERE key LIKE ? OR tags LIKE ? OR content LIKE ?
    ''', (search_term, search_term, search_term))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return f"No results found for query '{query}'."
        
    output = "Found entities:\n"
    for row in results:
        output += f"- Key: {row[0]} | Tags: {row[1]} | Status: {row[3]}\n"
    return output

if __name__ == "__main__":
    print(f"[*] Starting WikiBrain MCP Server (Database: {DB_PATH})")
    mcp.run(transport="stdio")
