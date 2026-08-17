# The AI-Agent Development Stack on ChromeOS Crostini: A Complete Tool-by-Tool Report (2026)

## TL;DR
- This machine is a **fully self-contained AI-agent development workstation** running inside a Debian Linux container (Crostini) on ChromeOS: Google's Antigravity agentic tooling and Android Studio sit on top of a Google Cloud + Firebase + Gemini stack, wired together by Python 3.13 and Node.js 22 runtimes.
- The tools form a coherent **agent pipeline**: `requests`/`httpx` + `beautifulsoup4` ingest and clean web content → the `google-genai` SDK sends it to Gemini (e.g. `gemini-3.6-flash`) for analysis with `pydantic`-validated structured output → `google-cloud-firestore` persists the agent's state and memory → `gcloud`/`firebase-tools` provision and secure the cloud backend → `agy` and `gws` act as the terminal-level agent orchestration and Workspace automation layer.
- Everything here reflects the current 2026 Google agent ecosystem: Gemini 3.5/3.6 Flash models, the new **Interactions API** (GA June 2026), the **Antigravity CLI (`agy`)** that replaced the retired Gemini CLI, and the `google-genai` v2 SDK — the modern, non-deprecated path for building on Gemini.

## Key Findings
- **Antigravity is the centerpiece.** Google Antigravity (public preview November 18, 2025; expanded at Google I/O 2026 on May 19, 2026) is an agent-first development platform; its terminal client `agy` v1.1.11 is the successor to Gemini CLI and runs multi-step, multi-agent coding tasks from the shell. This is the single most important "new" tool in the stack.
- **The Gemini access path is fully modern.** `google-genai` v2.17.0 is the current unified SDK; the legacy `google-generativeai` package is in maintenance-only status and should not be used for new work. The stack targets Gemini 3.x Flash models via either `generateContent` or the newer Interactions API.
- **Firestore is doing double duty** as both the app database and the agent's persistent memory/state store — a well-established 2026 pattern for stateful LLM agents.
- **The stack cleanly separates concerns**: heavy IDE work (Android Studio) vs. lightweight CLI provisioning (`gcloud`, `firebase`), vs. agent runtime (Python venv), vs. JS tooling host (Node/nvm).
- **`gws` is an unusual, powerful addition**: a Rust-built, dynamically-generated Google Workspace CLI designed explicitly for AI agents, giving the agent scriptable, scoped access to Gmail, Drive, Calendar, Sheets, Docs, Tasks, Keep, and Forms.

## Details

### Applications / IDEs

#### 1. Android Studio (Quail 3, `/opt/android-studio/`)
**What it is:** The official Google IDE for building Android apps, built on JetBrains IntelliJ IDEA. "Quail" is the 2026 release codename; Quail 3 (version 2026.1.3) reached the stable channel in July 2026, with Quail 3 Patch 1 following in August 2026. Google ships an official ChromeOS build alongside the Linux, macOS, and Windows builds.

**Core purpose:** Write Kotlin/Java (and increasingly Jetpack Compose) code, manage the Android SDK, run Gradle builds, design layouts, and test on emulators or physical devices.

**How it's typically used:**
- **Project & build management** via Gradle — Android Studio drives Gradle Sync and build automation. (Note: from Quail 1 onward, `org.gradle.parallel=true` no longer enables parallel model fetching during Sync; you now set `org.gradle.tooling.parallel=true` to restore parallel sync.)
- **SDK Manager** to install platform tools, build tools, and system images.
- **Layout/Compose design tools** with Live Edit for immediate UI preview.
- **Emulator (AVD)** for on-device testing, plus USB debugging (adb) to real phones.
- **Gemini AI assistant** is built into the IDE for code completion and assistance.

**Running on ChromeOS Crostini:** Android Studio does not run natively on ChromeOS; the supported path is inside the Linux (Crostini) Debian container, using the official x86_64 Linux build (which is what `/opt/android-studio/` reflects). It needs a JDK (JDK 17 is the safe choice for current releases), and works best on Intel/AMD Chromebooks with 8GB+ RAM (16GB recommended). The emulator is the wildcard — hardware acceleration (KVM) support varies by Chromebook; when unavailable, developers test on real devices over USB or offload builds to the cloud. Coding and building APKs work reliably even when local emulation struggles.

**Role in the AI-agent workflow:** Android Studio is the "front-end app" layer — it's where a mobile client that consumes the Gemini/Firestore backend would be built. In this specific stack it's somewhat orthogonal to the core agent pipeline, but it ties in through Firebase (a Firebase-backed Android app reading the same Firestore the agent writes) and through the in-IDE Gemini assistant. Per Google's official announcement, "Gemini 3.5 Flash is generally available via Google Antigravity, the Gemini API in Google AI Studio and Android Studio, Gemini Enterprise Agent Platform and Gemini Enterprise" (GA May 19, 2026) — so the same Flash model powering the agent pipeline is available inside the IDE.

### CLI Tools

#### 2. Google Cloud CLI — `gcloud` v579.0.0
**What it is:** The primary command-line interface for Google Cloud Platform, part of the Google Cloud SDK (which also bundles `gsutil` and `bq`).

**Core purpose:** Create and manage GCP resources, authenticate, enable APIs, and manage services from the terminal — essential for scripting and CI/CD.

**How it's typically used:**
- **Authentication:** `gcloud auth login` authenticates the CLI itself (browser-based OAuth, stores credentials). `gcloud auth application-default login` creates Application Default Credentials (ADC) that client libraries (like `google-genai` and `google-cloud-firestore`) pick up automatically — a critical distinction. `gcloud auth print-access-token` mints a short-lived token (which, notably, `gws` can consume).
- **Project/config:** `gcloud config set project`, `gcloud config get-value project` (always check before destructive ops).
- **Enabling APIs:** `gcloud services enable firestore.googleapis.com aiplatform.googleapis.com` etc. — the necessary first step before the Firestore or Gemini/Vertex APIs will respond.
- **Service management & read-only checks:** `gcloud services list --enabled`, `gcloud projects list`.
- Service-account impersonation via `--impersonate-service-account` for least-privilege automation.

**Role in the AI-agent workflow:** `gcloud` is the **provisioning and identity layer**. It turns on the APIs the agent depends on (Firestore, Vertex AI/Gemini), and — most importantly — its ADC mechanism is how the Python agent code authenticates to Firestore and (optionally) Gemini without hard-coded keys.

#### 3. Firebase CLI — `firebase-tools` v15.26.0
**What it is:** The command-line tool for Firebase, installed as a global npm package (hence its dependency on Node.js in this stack).

**Core purpose:** Configure and deploy Firebase resources — here specifically Firestore configuration, security rules, and indexes — and link the local project to a Firebase project.

**How it's typically used:**
- `firebase login` — authenticate with a Google account.
- `firebase projects:list` — list accessible projects.
- `firebase init firestore` — scaffold the project, creating `firestore.rules` and `firestore.indexes.json`.
- **Deploy security rules:** `firebase deploy --only firestore:rules` — the canonical command. Rules in the project directory *overwrite* console-edited rules, so the CLI path keeps rules under version control alongside code.
- **Local Emulator Suite** for full local testing of rules and Firestore before deploying.

**Role in the AI-agent workflow:** Firebase CLI **secures and configures the state store**. When the agent uses Firestore as its memory, the security rules deployed via `firebase deploy` govern who/what can read and write those documents. It complements `gcloud`: `gcloud` enables the API and manages IAM at the cloud level; `firebase` manages the Firestore-specific developer experience, rules, and (for the default database) rule deployment that the Google Cloud console can't do.

#### 4. Antigravity CLI — `agy` v1.1.11
**What it is:** The terminal client for **Google Antigravity**, Google's agent-first development platform. Antigravity launched in public preview on November 18, 2025 alongside Gemini 3 Pro — per Google's official Antigravity blog, "From today, Google Antigravity is available in public preview at no charge, with generous rate limits on Gemini 3 Pro usage." It combines an AI IDE ("Editor View") with an agent-first "Manager" surface where autonomous agents plan, execute, and verify tasks across editor, terminal, and browser. `agy` is the command-line surface, announced May 19, 2026 at Google I/O as the **successor to the Gemini CLI**. Per the Google Developers Blog, "On June 18, 2026, Gemini CLI and Gemini Code Assist IDE extensions will stop serving requests for Google AI Pro and Ultra, as well as those using it free of charge using Gemini Code Assist for individuals." `agy` is a single **Go-compiled binary** (which, per hands-on reporting, "starts in a few milliseconds, occupies a handful of megabytes of RAM and includes a sub-agent orchestrator") installed to `~/.local/bin/agy`.

**Core purpose:** Bring Antigravity's multi-step reasoning, multi-file editing, tool calling, and — its headline feature — **asynchronous sub-agent orchestration** directly into the terminal, as a keyboard-centric TUI or a headless automation tool.

**How it's typically used:**
- **Interactive TUI:** run `agy` to start a session in the current directory, or `agy "Explain this repo"` with an initial prompt.
- **Headless/CI (one-shot):** `agy -p "Fix the failing tests"` runs non-interactively and prints the result; `agy -p "List all TODOs" --output-format json` for pipeable structured output. This is the mode used in shell scripts, Git hooks, and CI.
- **Models:** `agy models` lists supported models; `agy --model gemini-3-pro` selects one. It's backed by Gemini models (including Gemini 3.5/3.6 Flash).
- **Execution modes** (cycled with `Shift+Tab`): default → accept-edits → plan. The default `request-review` mode pauses before file writes to show a line-level diff.
- **In-session slash commands:** `/agents` (manage sub-agents), `/mcp` (Model Context Protocol servers), `/diff`, `/rewind`, `/plan`, `/skills`.
- **Authentication:** first launch prompts for Google OAuth (or a Google Cloud project); over SSH it prints an auth URL to paste a code back. Tokens live in the OS keyring; settings under `~/.gemini/antigravity-cli/`.
- **Migration:** `agy plugin import gemini` converts old Gemini CLI extensions to Antigravity plugins.
- Reads `AGENTS.md` / `GEMINI.md` workspace context files for project-specific instructions.

**Role in the AI-agent workflow:** `agy` is the **agent orchestration layer at the terminal**. Rather than the developer hand-writing every step of the ingest→analyze→persist pipeline, `agy` can autonomously drive it: dispatching sub-agents to fetch and process content, edit code, run the Python scripts, and verify results — all coordinated from the shell. It shares the same backend agent harness as the Antigravity 2.0 desktop app.

#### 5. `gws` — Google Workspace CLI
**What it is:** An open-source (Apache-2.0) command-line tool, invoked as `gws`, that gives humans *and AI agents* unified access to the entire Google Workspace API surface. It is written in **Rust** (~99%) and distributed as pre-built native binaries via npm (`@googleworkspace/cli`), Homebrew, Cargo, and Nix. Current version is **v0.22.5** (released March 31, 2026). It is explicitly **"not an officially supported Google product"** and is pre-v1 with expected breaking changes. Introduced in early March 2026 by Google Workspace DevRel, it hit #1 on Hacker News with 571 points and gained roughly 4,900 GitHub stars in three days (reaching about 20,800 stars by mid-March 2026).

**Core purpose:** Provide scriptable, scoped access to Google Workspace services without writing custom OAuth flows or SDK code. Its defining technical trait: it **builds its command tree dynamically from Google's Discovery Service at runtime**, so it automatically exposes any Workspace API (and stays current without updates).

**Services & granular scopes:** It supports Drive, Gmail, Calendar, Sheets, Docs, Chat, Slides, People, Admin, Classroom, Meet — and, confirmed from the official repo, **Google Tasks, Google Keep, and Google Forms** (dedicated `gws-tasks`, `gws-keep`, `gws-forms` skills exist). Scopes are granular and passed as a comma-separated service list: `gws auth login -s drive,gmail,sheets`. **Important constraint:** unverified apps in "testing mode" are capped at ~25 OAuth scopes, so the `recommended` preset (85+ scopes) will fail for personal `@gmail.com` accounts — you must select individual services.

**How it's typically used:**
- **Setup/auth:** `gws auth setup` (one-time; wraps `gcloud` to create a Cloud project, enable APIs, and log in), then `gws auth login`. Credentials are encrypted at rest (AES-256-GCM) in the OS keyring.
- **Alternative auth:** service accounts via `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`, or a pre-minted token via `export GOOGLE_WORKSPACE_CLI_TOKEN=$(gcloud auth print-access-token)`.
- **Command pattern:** `gws <service> <resource> <method> [flags]`, e.g. `gws drive files list --params '{"pageSize": 10}'`, `gws gmail messages list`, `gws calendar events list`, `gws sheets spreadsheets create --json '{"properties":{"title":"Q1 Budget"}}'`.
- **Structured output:** *all* output — success, errors, metadata — is JSON, with structured exit codes (0 success, 2 auth error, 3 validation error, etc.), making it ideal for scripting and agent consumption.
- **Agent integration:** ships 100+ "Agent Skills" (`SKILL.md` files), can run as an MCP server (`gws mcp -s drive,gmail,calendar`), and integrates with Claude Code, Cursor, and Gemini CLI. It also offers a `--sanitize` flag that routes responses through Google Cloud Model Armor to scan for prompt injection before content reaches the agent.

**Role in the AI-agent workflow:** `gws` is the **Workspace automation and data-source layer**. It lets the agent read and act on real user data — summarize inbox threads, pull data from Sheets, create Calendar events, draft Docs — as a scripted, scoped, JSON-emitting tool. Its per-service scope model and Model Armor sanitization make it a comparatively safe way to give an autonomous agent access to sensitive personal data.

### Runtimes

#### 6. Python 3.13.5 (venv at `~/projects/venv`)
**What it is:** The current-generation CPython interpreter, isolated in a virtual environment. A venv is a self-contained directory with its own `pip` and installed packages, keeping this project's dependencies separate from the system Python.

**Core purpose here:** The **agent scripting runtime** — it runs the orchestration logic that ties together web ingestion, Gemini calls, and Firestore persistence.

**How it's typically used:** activate with `source ~/projects/venv/bin/activate`, install with `pip install`, run agent scripts. All the Python libraries below (`google-genai`, `google-cloud-firestore`, `pydantic`, `requests`, `httpx`, `beautifulsoup4`) live inside this venv.

**Role in the AI-agent workflow:** This is the **glue and control plane** of the pipeline. Python's dominance in the AI/LLM ecosystem, plus first-class Google SDKs, make it the natural home for the agent's logic.

#### 7. Node.js v22.23.2 (via nvm) + npm v10.9.8
**What it is:** The JavaScript/TypeScript runtime (V8-based) with its package manager, installed via `nvm` (Node Version Manager, which allows multiple Node versions and easy switching). v22 is an LTS-line release.

**Core purpose here:** Two roles — (1) host for global CLI tools (`firebase-tools` and the `gws` npm installer both require Node), and (2) the runtime for any JavaScript front-end (the React app below).

**How it's typically used:** `nvm use 22`, `npm install -g firebase-tools`, `npm install` for project dependencies, `npm run` for scripts.

**Role in the AI-agent workflow:** Node is the **JS tooling and front-end host**. It doesn't run the core Python agent, but it powers the deployment/config CLIs and any web UI that visualizes or interacts with the agent's output.

### Python Libraries (pip, inside venv)

#### 8. `google-genai` v2.17.0 — the Gemini SDK
**What it is:** Google's official, current-generation Python SDK for Gemini models (the "Google Gen AI SDK"). It provides a unified interface to both the Gemini Developer API and Vertex AI. This is the *modern* SDK — the older `google-generativeai` package is in maintenance-only status. Per the official `python-genai` README, "The `google-generativeai` package will continue to support the original Gemini models… All new features will be developed in the new Google GenAI SDK," and the SDK advises pinning "the SDK version to < 3.0.0" to avoid unexpected updates.

**Core purpose:** Send prompts to Gemini models (e.g. `gemini-3.6-flash`, `gemini-3.5-flash`) and get back text, structured data, tool calls, or multimodal output.

**How it's typically used:**
- **Basic inference:** `client = genai.Client()` then `client.models.generate_content(model="gemini-3.5-flash", contents="...")`.
- **Interactions API (new, GA June 22, 2026):** `client.interactions.create(model="gemini-3.6-flash", input="...")` — a single endpoint that handles both models (pass `model=`) and autonomous agents (pass `agent=`, e.g. the Deep Research agent), with optional server-side state via `previous_interaction_id` and background execution. This is the forward-looking path for agentic apps.
- **Structured output:** pass a `pydantic` model or JSON schema as `response_schema` with `response_mime_type="application/json"` — Gemini returns validated, type-safe JSON. Ideal for data extraction, classification, and generating structured tool inputs.
- **Function calling:** declare tool schemas (the SDK can auto-generate them from Python function signatures/docstrings); Gemini returns a `functionCall` object your code executes and feeds back — the fundamental agentic loop.
- **Model-specific note:** for `gemini-3.6-flash` and later, per Google's Gemini API changelog, "The sampling parameters `temperature`, `top_p` and `top_k` are now deprecated" — they're ignored, so control quality/latency via thinking levels instead. Gemini 3.6 Flash "features improved token efficiency and code/agentic planning capabilities at a lower price point than 3.5 Flash."

**Role in the AI-agent workflow:** This is the **brain/inference layer** — the step where cleaned web content is analyzed, summarized, classified, or reasoned over by Gemini, ideally with `pydantic`-validated structured output that flows cleanly into Firestore.

#### 9. `google-cloud-firestore` v2.28.1 — Firestore client
**What it is:** The official Python client for Cloud Firestore, Google's serverless NoSQL document database.

**Core purpose:** Read and write documents/collections programmatically — and in this stack, serve as the agent's persistent state and memory store.

**How it's typically used:**
- `db = firestore.Client()` (picks up ADC from `gcloud`).
- **Write:** `db.collection("users").document("alovelace").set({"first": "Ada", ...})`.
- **Read:** `doc_ref.get()` → `.to_dict()`; iterate a collection with `.stream()`.
- **Add with auto-ID:** `db.collection("stories").add({...})`.
- **Real-time listeners** via `on_snapshot`; batched writes via `db.batch()`.

**Role in the AI-agent workflow:** Firestore is the **memory/state persistence layer**. A stateless LLM forgets everything between calls; Firestore gives the agent durable memory — conversation history, extracted facts, task state, and results. This is a well-established 2026 pattern (e.g., LangChain's `FirestoreChatMessageHistory`): serverless, low-latency, survives restarts, and scales across instances. In the pipeline, Gemini's structured output is written here as the agent's evolving knowledge base.

#### 10. `pydantic` v2.13.4 — data validation & models
**What it is:** The de facto Python library for data validation using type hints; you define a `BaseModel` subclass with typed fields and Pydantic validates/coerces data at runtime, raising clear errors on mismatch. v2 has a Rust-powered core for speed.

**Core purpose:** Define and enforce the *shape* of data — especially LLM outputs.

**How it's typically used:** define models with typed fields, `Field(description=...)` (the description is passed to the model as guidance), `Literal` for enums, and validators. Then `Model.model_validate_json(response)` to validate. `model_json_schema()` produces a JSON schema.

**Role in the AI-agent workflow:** Pydantic is the **contract enforcer** between Gemini and the rest of the pipeline. Because `google-genai` accepts Pydantic models directly as `response_schema`, the same model both *instructs* Gemini on the required output structure and *validates* what comes back — guaranteeing that only well-formed, type-correct data reaches Firestore. This is what makes the "Gemini analysis → Firestore state" handoff reliable rather than fragile.

#### 11. `requests` — synchronous HTTP client
**What it is:** The long-standing, ubiquitous Python HTTP library, prized for a simple, human-friendly API. Synchronous/blocking only.

**Core purpose:** Make straightforward HTTP calls — GET a web page, POST to an API.

**How it's typically used:** `requests.get(url).text`, `.json()`, `.raise_for_status()`; `Session()` for connection reuse.

**Role in the AI-agent workflow:** The **simple web-ingestion fetcher** — for one-off or sequential page fetches, `requests` is the path of least resistance. Its HTML output feeds directly into `beautifulsoup4`.

#### 12. `httpx` — async-capable HTTP client
**What it is:** A modern HTTP client with an API nearly identical to `requests` but adding **async support** (`AsyncClient`) and **HTTP/2**.

**Core purpose:** Same as `requests` for sync code, but the go-to when you need concurrency or modern protocol features.

**When to use vs. `requests`:** Use `requests` for simple sync scripts. Use `httpx` when you need to fetch many URLs concurrently (async can be 5–10× faster for concurrent workloads), when integrating with async frameworks (FastAPI, asyncio workers), or when you want HTTP/2. For new 2026 projects it's often the recommended default.

**Role in the AI-agent workflow:** The **high-throughput web-ingestion fetcher**. When the agent needs to pull dozens or hundreds of pages to feed Gemini, `httpx.AsyncClient` fires them concurrently instead of one at a time — a major throughput win over `requests` at the ingestion stage.

#### 13. `beautifulsoup4` — HTML parsing
**What it is:** A Python library (imported as `bs4`) for parsing HTML/XML into a navigable parse tree, tolerant of malformed markup. Typically paired with a parser like `lxml` or the built-in `html.parser`.

**Core purpose:** Extract structured data from messy HTML — the core of web scraping.

**How it's typically used:** `soup = BeautifulSoup(html, "html.parser")`, then `.find()`, `.find_all()`, `.get_text()`, attribute access. For web-to-markdown pipelines it's commonly combined with `markdownify` or `html-to-markdown` to turn cleaned HTML into Markdown.

**Role in the AI-agent workflow:** The **web-to-clean-content converter**, the crucial first stage of the pipeline. Raw HTML from `requests`/`httpx` is full of navigation, ads, and markup noise; BeautifulSoup strips it down to the meaningful content (and often to Markdown), producing the clean, token-efficient text that gets sent to Gemini. Markdown is a particularly good intermediate format because it's compact and preserves structure (headings, lists, links) that LLMs parse well.

### npm Libraries

#### 14. `react` and `react-dom`
**What they are:** `react` is the core JavaScript UI library for building component-based user interfaces via a declarative component model; `react-dom` is the companion package that renders those components into the browser DOM. React 19 is in production in 2026 (introducing the React Compiler, Server Components, and hooks like `useActionState`). React itself focuses narrowly on rendering; routing, state, and data-fetching come from companion libraries.

**Core purpose:** Build interactive web front-ends as reusable components.

**How they're typically used:** define function components returning JSX; `react-dom`'s `createRoot(...).render(<App />)` mounts the tree. Companion libraries (React Router for navigation, etc.) fill out a full app.

**Role in the AI-agent workflow:** React is the **human-facing UI layer** (hosted by the Node runtime). In this stack it would power a dashboard or chat interface that visualizes the agent's Firestore-stored state — displaying ingested/analyzed content, conversation history, or task status — and lets a human review, steer, or trigger the agent. It closes the loop between the autonomous back-end pipeline and the user. (Firestore has real-time listeners in JS too, so a React app can live-update as the agent writes new state.)

## Recommendations
1. **Treat `google-genai` v2 + the Interactions API as the default build target.** It's the current, non-deprecated path and unifies model calls and managed agents under one API. Migrate any code still on `google-generativeai` — that package is maintenance-only and gets no new features. Pin the SDK below 3.0.0 to avoid breaking updates. **Threshold to revisit:** if you need a stable, long-supported deployment surface today, stay on `generateContent` (still fully supported); adopt Interactions where you need server-side state or background/agentic execution.
2. **Use `pydantic` models as the single source of truth for every Gemini→Firestore handoff.** Define the schema once, pass it as `response_schema`, validate the response, then write the validated object to Firestore. This eliminates the most common class of pipeline bugs (malformed LLM output).
3. **Standardize authentication on ADC via `gcloud`.** Run `gcloud auth application-default login` once so both `google-genai` (on Vertex) and `google-cloud-firestore` authenticate without embedded keys. Reserve service-account JSON for headless/CI. For `gws`, prefer per-service scopes over the `recommended` preset to avoid the ~25-scope testing-mode ceiling.
4. **Use `httpx.AsyncClient` (not `requests`) for the ingestion stage** if the agent fetches more than a handful of pages — the concurrency gain is large and directly reduces pipeline latency. Keep `requests` for simple one-off calls.
5. **Deploy Firestore security rules via `firebase deploy --only firestore:rules` and keep them in version control.** Since the agent writes to Firestore autonomously, tight rules are your guardrail. Test with the Local Emulator Suite before deploying.
6. **Lean on `agy` for orchestration, but keep it in `request-review` mode for anything touching cloud resources or user data.** Reserve `--dangerously-skip-permissions`/`always-proceed` for sandboxed, disposable workspaces only. **Threshold:** only move to headless `agy -p ... --output-format json` in CI once the workflow is proven interactively.
7. **For Android Studio on this Chromebook, plan to test on a physical device or cloud build** rather than relying on the local emulator, unless the device has confirmed KVM/hardware acceleration and 16GB RAM.

## Caveats
- **Model naming is in flux.** The stack references `gemini-3.6-flash`; as of mid-2026, Gemini 3.5 Flash (GA May 19, 2026), Gemini 3.6 Flash, and Gemini 3.5 Flash-Lite are all documented, with Gemini 3.5 Pro announced as forthcoming. Exact model IDs and their availability change quickly — verify against the live models page before pinning one. Note also that from Gemini 3.6 Flash onward, sampling parameters (`temperature`/`top_p`/`top_k`) are deprecated and ignored.
- **`gws` is explicitly not an officially supported Google product** and is pre-v1.0 with expected breaking changes; the version installed on this machine may differ from the v0.22.5 that was current in March 2026. Treat it as powerful but unstable, and note that giving an autonomous agent broad Workspace scopes carries real data-exposure risk (mitigated, partly, by its Model Armor `--sanitize` option and least-privilege scoping).
- **Some `agy` details come from community/third-party references** (cheat sheets, tutorials) rather than a single canonical doc page, because the official CLI docs URL returned a 404 at time of research; version-specific command behavior should be confirmed with `agy changelog` and `agy --version` on the machine itself. The specific `agy` version installed (v1.1.11) is newer than the v1.1.5 covered by the most detailed public cheat sheet found. There is also a minor sourcing note on the binary's language: multiple hands-on sources describe `agy` as Go-compiled, but this has not been confirmed from an official Google engineering statement.
- **Version-specific behavior:** the exact feature set of each pinned version (e.g., `firebase-tools` 15.26.0, `gcloud` 579.0.0) may include changes not fully documented in the general sources cited; consult each tool's own changelog for release-specific details.
- **Antigravity's rapid evolution:** the platform launched November 2025 and already has a "2.0" desktop app and expanded ecosystem announced at I/O 2026, so its capabilities and the `agy`/desktop relationship are a fast-moving target.