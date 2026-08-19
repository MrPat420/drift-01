#!/usr/bin/env python3
"""wiki_mcp_server_with_health.py

Thin wrapper around the existing FastMCP server that adds a lightweight
/healthz endpoint (and simple /entity and /entities REST routes) while
preserving the original /mcp namespace.
"""
import pathlib
import importlib.util

# ----------------------------------------------------------------------
# Load the original server implementation (wiki_mcp_server.py) which
# registers all FastMCP tools.
# ----------------------------------------------------------------------
orig_path = pathlib.Path("/home/simian420/projects/wiki_mcp_server.py")
spec = importlib.util.spec_from_file_location("wiki_mcp_server", orig_path)
orig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(orig)  # populates `orig.mcp` and tool functions

# ----------------------------------------------------------------------
# FastAPI app is exposed by FastMCP via the `app` attribute.
# ----------------------------------------------------------------------
app = getattr(orig, "mcp").app

# ----------------------------------------------------------------------
# Health‑check endpoint – always returns OK.
# ----------------------------------------------------------------------
@app.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok"}

# ----------------------------------------------------------------------
# Simple entity retrieval – reuse the existing `read_entity` function if
# available, otherwise return a placeholder.
# ----------------------------------------------------------------------
@app.get("/entity/{key}")
async def get_entity(key: str):
    if hasattr(orig, "read_entity"):
        # `read_entity` returns a string; FastAPI will wrap it as JSON.
        return orig.read_entity(key)
    return {"error": f"entity {key} not found"}

# ----------------------------------------------------------------------
# List entities – a very lightweight placeholder implementation.
# ----------------------------------------------------------------------
@app.get("/entities")
async def list_entities(type: str = "entity", limit: int = 15):
    # Return dummy data matching the expected shape.
    return [{"key": f"{type}_{i}", "type": type} for i in range(1, limit + 1)]

# ----------------------------------------------------------------------
# Run the server on the traditional FastMCP port (9000) – this keeps the
# /mcp tools reachable while exposing the new REST routes.
# ----------------------------------------------------------------------
if __name__ == "__main__":
    orig.mcp.run(transport="sse", host="127.0.0.1", port=9000)
