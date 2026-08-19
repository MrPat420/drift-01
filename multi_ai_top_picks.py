"""
Multi-AI Independent Top Picks Deliberation Engine (Exact Live Model Slugs)
Queries 4 independent AI evaluation models to generate uninfluenced, unbiased Top Picks.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

BASE_DIR = Path("/home/simian420/projects")
OUTPUT_FILE = BASE_DIR / "MULTI_AI_INDEPENDENT_TOP_PICKS.md"

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "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").strip()
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-e16c91d5d6ac4e35bbe0f70a22afa58d").strip()

def load_corpus_context() -> str:
    ledger_path = BASE_DIR / "MASTER_LEDGER_GEM_THREE_ACCOUNTS.md"
    audit_path = BASE_DIR / "claude-audit" / "AUDIT-REPORT.md"
    registry_path = BASE_DIR / "PROJECT_REGISTRY.md"
    
    ledger_txt = ledger_path.read_text()[:12000] if ledger_path.exists() else ""
    audit_txt = audit_path.read_text()[:12000] if audit_path.exists() else ""
    registry_txt = registry_path.read_text()[:12000] if registry_path.exists() else ""
    
    return f"""
=== MASTER LEDGER (THREE GEM ACCOUNTS: patkelly74, simiandox, simian420) ===
{ledger_txt}

=== AUDIT REPORT & VENTURE REGISTRY EXCERPT ===
{audit_txt}

=== PROJECT REGISTRY EXCERPT ===
{registry_txt}
"""

NEUTRAL_SYSTEM_PROMPT = """You are an independent, objective evaluation intelligence.
Your task is to impartially review the entire provided multi-account corpus and independently select what YOU determine to be the absolute top highest-value assets, ventures, intellectual property, technologies, or recovery items.
Do not follow any pre-existing bias or preferred ranking. Use your own analytical judgment and criteria."""

NEUTRAL_USER_PROMPT_TEMPLATE = """
Review the entire multi-account corpus below representing years of research, software projects, legal discovery, and IP across three primary accounts (patkelly74, simiandox, simian420):

{corpus}

--- YOUR INDEPENDENT TASK ---
As an independent AI evaluation engine, select your Top 10-15 HIGHEST-VALUE PICKS from this entire corpus based purely on your own objective assessment.

For EACH item you select, provide:
1. **Rank & Item Name / Code**
2. **Account / Source Origin** (e.g., patkelly74, simiandox, simian420, or cross-account)
3. **Core Substance** (What it is technically, commercially, or legally)
4. **Why YOU Picked It** (Your independent evaluation: feasibility, uniqueness, revenue potential, or critical importance)
5. **Evaluation Score** (1-100 on Viability & Impact)

At the end of your list, provide a brief 2-paragraph summary explaining your overall strategic thesis.
"""

def query_openrouter(model_id: str, prompt: str, label: str) -> str:
    print(f"🤖 Querying {label} ({model_id})...")
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://antigravity.internal",
        "X-Title": "Multi-AI Deliberation"
    }
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": NEUTRAL_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 4096
    }
    try:
        req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=120) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            if "choices" in res and len(res["choices"]) > 0:
                print(f"✅ {label} completed evaluation.")
                return res["choices"][0]["message"]["content"]
    except Exception as ex:
        print(f"[WARN] {label} hit error: {ex}")
        return f"*[Evaluation from {label} error: {ex}]*"
    return f"*[Evaluation from {label} returned empty]*"

def query_deepseek_direct(prompt: str) -> str:
    print(f"🤖 Querying DeepSeek Reasoning Engine (deepseek-chat)...")
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": NEUTRAL_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 4096
    }
    try:
        req = urllib.request.Request("https://api.deepseek.com/chat/completions", data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=120) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            if "choices" in res and len(res["choices"]) > 0:
                print("✅ DeepSeek direct completed evaluation.")
                return res["choices"][0]["message"]["content"]
    except Exception as ex:
        print(f"[WARN] DeepSeek error: {ex}")
        return f"*[DeepSeek error: {ex}]*"

def main():
    print("==========================================================")
    print("⚡ Starting Multi-AI Independent Top Picks Deliberation")
    print("==========================================================")
    
    corpus = load_corpus_context()
    user_prompt = NEUTRAL_USER_PROMPT_TEMPLATE.format(corpus=corpus)
    
    # 1. DeepSeek (Direct API)
    deepseek_results = query_deepseek_direct(user_prompt)
    time.sleep(2)
    
    # 2. Google Gemini 3.5 Flash (OpenRouter live ID)
    gemini_results = query_openrouter("google/gemini-3.5-flash", user_prompt, "Google Gemini 3.5 Flash")
    time.sleep(2)
    
    # 3. Meta LLaMA 3.3 70B (OpenRouter live ID)
    llama_results = query_openrouter("meta-llama/llama-3.3-70b-instruct", user_prompt, "Meta LLaMA 3.3 70B")
    time.sleep(2)
    
    # 4. GLM 5.2 (OpenRouter Free Tier Live ID)
    glm_results = query_openrouter("z-ai/glm-5.2:free", user_prompt, "GLM-5.2 Free Engine")
    
    master_doc = f"""# MULTI-AI INDEPENDENT TOP PICKS & CONSENSUS DOSSIER
**Deliberation Methodology**: 4 Independent AI Engines evaluated the three-account corpus (`patkelly74`, `simiandox`, `simian420`) under strict neutrality prompts with zero injected bias.
**Engines Participated**: DeepSeek V3 · Google Gemini 3.5 Flash · Meta LLaMA 3.3 70B · GLM-5.2

---

## ⚡ PANEL 1: DeepSeek Reasoning Engine Independent Picks
{deepseek_results}

---

## 🌐 PANEL 2: Google Gemini 3.5 Flash Independent Picks
{gemini_results}

---

## 🏛️ PANEL 3: Meta LLaMA 3.3 70B Independent Picks
{llama_results}

---

## 🔬 PANEL 4: GLM-5.2 Free Engine Independent Picks
{glm_results}
"""
    OUTPUT_FILE.write_text(master_doc)
    print(f"\n✨ Master Multi-AI Deliberation complete!")
    print(f"📄 Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
