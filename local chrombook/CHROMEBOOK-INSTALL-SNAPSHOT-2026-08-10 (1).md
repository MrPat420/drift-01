---
title: "Chromebook Install Snapshot — 2026-08-10 (gws-cli-local-505120)"
kb_type: wiki
topic: infrastructure
environment: ChromeOS Crostini (Debian container / penguin)
gcp_project: gws-cli-local-505120
captured: 2026-08-10
revised: 2026-08-11
status: current-install-inventory
merges: [CHROMEBOOK-ANDROID-STUDIO-INSTALL-2026-08-10.md]
companion-docs: [CHROMEBOOK-GCP-ENV-HANDOFF.md]
tags: [chromebook, crostini, gcp, firestore, gws-cli, antigravity, gemini, android-studio, quail, install-snapshot]
---

# Chromebook Install Snapshot — 2026-08-10

Single current-state install inventory for this box. Identity, security items, guidelines, and pending work live in the master handoff (CHROMEBOOK-GCP-ENV-HANDOFF.md). Tool deep-dives live in the AI-Agent Development Stack research report.

## 1. Active environment & configuration

- **System:** ChromeOS Linux container (Crostini / `penguin`)
- **Active project ID:** `gws-cli-local-505120` (Google Cloud / Firebase)
- **Python:** isolated venv at `~/projects/venv` (Python 3.13.5)
- **Node.js:** v22.23.2 via nvm (npm v10.9.8)
- **Available space:** ~7.4 GB (disk optimized after removing heavy Flatpak runtimes)

## 2. Applications / IDEs

### Android Studio Quail 3 — `/opt/android-studio/`

- **Purpose:** official Android IDE — Kotlin/Java, Android SDK management, Gradle build automation, layout design
- **Install method:** direct tarball stream extraction — `curl` piped into `sudo tar -xz -C /opt/` to avoid temporary archive storage
- **Standard launch:** `/opt/android-studio/bin/studio.sh`
- **ChromeOS graphics fix (if splash screen freezes):**

```bash
_JAVA_OPTIONS="-Dsun.java2d.opengl=false -Dsun.java2d.xrender=false" /opt/android-studio/bin/studio.sh
```

- **State:** installed; initial Setup Wizard launched
- ☐ Complete first-run configuration wizard
- ☐ Add launcher icon: Tools → Create Desktop Entry

## 3. CLI tooling stack

- **Antigravity CLI (`agy`):** v1.1.11 — terminal agent workspace runner
- **Google Cloud CLI (`gcloud`):** v579.0.0
- **Firebase CLI (`firebase`):** v15.26.0 (global npm install)
- **gws CLI (Google Workspace):** authenticated; scopes for Drive, Calendar, Sheets, Docs, Tasks, Keep, Forms, Gmail read/compose — `gmail.send` deliberately excluded

## 4. Python libraries (pip, inside venv)

| Library | Version | Purpose |
| --- | --- | --- |
| google-genai | 2.17.0 | Official SDK for Gemini models (e.g. `gemini-3.6-flash`) |
| google-cloud-firestore | 2.28.1 | NoSQL document database connector |
| pydantic | 2.13.4 | Data validation / models |
| requests | — | HTTP client |
| beautifulsoup4 | — | HTML parsing |
| httpx | — | Async-capable HTTP client |

**npm libraries:** react, react-dom

## 5. Workspace directory structure (`~/projects`)

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
