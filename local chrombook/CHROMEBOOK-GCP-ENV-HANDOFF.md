---
title: "Chromebook GCP Environment — Master Handoff (gws-cli-local-505120)"
kb_type: wiki
topic: infrastructure
environment: ChromeOS Crostini (Debian container)
gcp_project: gws-cli-local-505120
account: simian420@gmail.com
captured: 2026-08-10
status: active-secondary-environment
tags: [chromebook, crostini, gcp, firestore, web2md, gws-cli, antigravity, gemini, simian420]
---

# Chromebook GCP Environment — Master Handoff

Secondary development environment, separate from the Kali workstation. ChromeOS Linux container (Crostini, Debian-based), bash-driven, operated via step-by-step terminal commands and raw JSON/REST payloads.

## Identity & project

- **GCP project:** `gws-cli-local-505120`
- **Account:** `simian420@gmail.com` (also a GEM-01 ingest account)
- **Auth:** user OAuth in file-backed keyring (gws CLI); Application Default Credentials planned for code execution identity

## Verified active infrastructure

**GCP APIs enabled:** cloudfunctions, run, cloudscheduler, secretmanager, documentai, admin.

**gws CLI (Google Workspace):** authenticated, granular scopes for Drive, Calendar, Sheets, Docs, Tasks, Keep, Forms, Gmail read/compose. **Security lock: `gmail.send` deliberately excluded** — no automated email sending.

**Live verified artifacts:**

| Artifact | ID / evidence |
| --- | --- |
| Google Doc "Agent Ideas Scratchpad" | `19BKQ8lHv8HU99rYdLXH1VS4oDFEXyzu9vsuy7RvK4VY` |
| Google Sheet "Agent Database Test" | `1HYaxKOKL5zBylG_AfWTai3GcVCubP_4D5ThhuoXbtDo` — row appends verified |
| Google Tasks | test insertion verified (`SU1GUkhhcWVyNUlzcF9GVQ`) |
| Secret Manager | `test-agent-key` provisioned |
| Document AI | endpoint routing verified via direct REST call |

## web2md-toolkit (primary project on this box)

Agent utility: ingest web content → structured Markdown → Gemini analysis → stateful memory in Firestore.

- **Pipeline:** `web2md_agent.py` in `~/projects/` — loads `google.cloud.firestore` + `google.genai` clients, infers with `gemini-3.6-flash`, persists to `web2md_artifacts` Firestore collection.
- **Scripts:** `agent_pipeline.py` (main orchestration), `web_fetcher.py` / `web2md_agent.py` (precursors), `setup_budget.py` / `final_verify.py` (FinOps hooks, health checks), `sanitizer.py` (regex + `isprintable()` prompt-injection filter).
- **Config:** `firebase.json`, `firestore.rules`, `firestore.indexes.json`, `~/.config/gws-agent/env.sh` (loads `GEMINI_API_KEY`, GCP project vars).

## ⚠ Open security item

`firestore.rules` currently `read, write: if true` — wide open. Hardening required before anything production-adjacent. Standing task, not yet done.

## Consolidated installed inventory

*(source sections 4–6 deduplicated)*

- **Runtimes:** Node.js v22.23.2 (nvm), npm v10.9.8, Python v3.13.5 (`python3-full`), venv at `~/projects/venv` (all Python work stays inside it)
- **CLI tools:** `gcloud` (authed, bound to project), `firebase-tools` v15.26.0, `agy` (Antigravity CLI) v1.1.11
- **Python libs:** google-genai, google-cloud-firestore, beautifulsoup4 v4.15.0, soupsieve v2.9.2, requests v2.34.2
- **npm libs:** react, react-dom

## Development guidelines (standing, for AI executors on this box)

1. All Python inside `~/projects/venv`.
2. Assume `GEMINI_API_KEY` and `GCP_PROJECT` must be set per session.
3. Prefer explicit CLI linking (`firebase use --add`, `gcloud services enable`) over interactive wizards.
4. Every future implementation carries the firestore.rules hardening task.
5. New packages must be compatible with Python 3.13.5 / Node 22.

## Pending stack (not yet implemented)

- **Tooling:** Android Studio (Quail), Antigravity + CLI expansion, AI Studio SDK bindings, Builders Hub/Firebase integration, Web2MD Markdown processor integration
- **Identity:** ADC login, headless service account, Domain-Wide Delegation
- **Agent core:** Vertex AI / Generative Language APIs, Firestore + BigQuery state memory, Document AI processor instance, Pub/Sub Eventarc triggers
- **Resiliency:** Terraform IaC, FinOps billing kill-switch Cloud Function, Pub/Sub DLQs with exponential backoff for Sheets 429s, kernel tuning `fs.inotify.max_user_watches=524288`
- **Task list:** robust web→md fetcher (BeautifulSoup/trafilatura), programmatic budget alerts, input sanitization layer expansion, Terraform migration

## Cross-references

- GEM-01 — simian420 is an ingest account in the PAIR pipeline
- Web2md concept overlaps MEMORY-ALPHA-01 raw-capture workflow — potential convergence or dedup decision needed
- Google Developer Program enrollment offers noted in source (Cloud/Firebase + AI Studio data-read consents) — no action recorded
