import os, json, subprocess
from pathlib import Path

MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
USE_OPENROUTER = os.getenv("USE_OPENROUTER", "false").lower() == "true"

TOP_PICKS_FILE = Path("top-25-picks.txt")

def load_top_picks():
    if not TOP_PICKS_FILE.exists():
        print("[WARN] No top‑25 picks file found – proceeding without it.")
        return []
    return [l.strip() for l in TOP_PICKS_FILE.read_text().splitlines() if l.strip()]

def run_subagent(name, args):
    cmd = ["agy", "subagent", "invoke",
           "--name", name,
           "--json-args", json.dumps(args)]
    if USE_OPENROUTER:
        cmd += ["--model", "openrouter"]
    subprocess.run(cmd, check=True)

def main():
    top = load_top_picks()
    agents = [
        {"name": "ip-auditor"},
        {"name": "product-analyzer"},
        {"name": "legal-recovery"},
        {"name": "simiandox-ingest"},
    ]
    for a in agents:
        args = {
            "corpus_path": "/home/simian420/projects/claude-audit",
            "top_picks": top,
            "model": MODEL,
        }
        run_subagent(a["name"], args)

if __name__ == "__main__":
    main()
