---
title: "Chromebook Install Snapshot — 2026-08-10 (gws-cli-local-505120)"
kb_type: wiki
topic: infrastructure
environment: ChromeOS Crostini (Debian container)
gcp_project: gws-cli-local-505120
captured: 2026-08-10
status: current-install-inventory
supersedes-sections: CHROMEBOOK-GCP-ENV-HANDOFF.md §"Consolidated installed inventory"
tags: [chromebook, crostini, gcp, firestore, gws-cli, antigravity, gemini, install-snapshot]
---

# Chromebook Install Snapshot — 2026-08-10

Full install inventory as of this date. Supersedes the installed-inventory section of the master handoff; all other sections of that doc (identity, security items, guidelines, pending stack) remain authoritative.

## 1. Active environment & configuration

- **System:** ChromeOS Linux container (Crostini)
- **Active project ID:** `gws-cli-local-505120` (Google Cloud / Firebase)
- **Python:** isolated venv at `~/projects/venv` (Python 3.13.5)
- **Node.js:** v22.23.2 via nvm (npm v10.9.8)

## 2. Verified installed tooling & CLI stack

- **Antigravity CLI (`agy`):** v1.1.11 — terminal agent workspace runner
- **Google Cloud CLI (`gcloud`):** v579.0.0
- **Firebase CLI (`firebase`):** v15.26.0 (global npm install)

**Key Python libraries (pip, inside venv):**

| Library | Version | Purpose |
| --- | --- | --- |
| google-genai | 2.17.0 | Official SDK for Gemini models (e.g. `gemini-3.6-flash`) |
| google-cloud-firestore | 2.28.1 | NoSQL document database connector |
| pydantic | 2.13.4 | Data validation / models |
| requests | — | HTTP client |
| beautifulsoup4 | — | HTML parsing |
| httpx | — | Async-capable HTTP client |

## 3. Workspace directory structure (`~/projects`)

Agent scripts:

- `app.py` — active agent script; queries Gemini 3.6 Flash and logs execution state/responses to Firestore
- `gws-agent-test.py` — integration check: Firestore writes + Gemini API connectivity
- `verify_env.py` — automated system health check and audit script
- `agent_pipeline.py` — main orchestration
- `web_fetcher.py`, `web2md_agent.py` — web ingest / precursor modules
- `sanitizer.py` — prompt-injection filter (regex + `isprintable()`)
- `setup_budget.py` — FinOps hook

Configuration:

- `firebase.json`, `firestore.rules`, `firestore.indexes.json`

Sub-toolkits / workspace directories:

- `web2md-toolkit`
- `claude-export-tools`
- `Antigravity-Workspace`

## Standing items (carried from master handoff, still open)

- ⚠ `firestore.rules` still `read, write: if true` — hardening required before anything production-adjacent
- All Python work stays inside `~/projects/venv`
- `GEMINI_API_KEY` and `GCP_PROJECT` set per session
- `gmail.send` scope deliberately excluded — no automated email sending
