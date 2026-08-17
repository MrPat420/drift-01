SITREP // [[DEFENSIVE NODE]]: PERU // [[ OIG STATUS]]: LAS // SYSTEM SPECIFICATION HANDOFF  
DOCUMENT: MC-SPEC-REV-2026.08 // OPERATION MCCLAUDE PLATFORM MIGRATION  
TARGET: LOCAL ENGINE DEPLOYMENT & AUTONOMOUS C2 COCKPIT  
ENVIRONMENT THERMAL: 21°C / 70°F (294.15 K) // REPO BASELINE: MrPat420/McClaude

# **SYSTEM SPECIFICATION DOCUMENT: OPERATION MCCLAUDE**

## **1\. High-Level Architecture Overview**

Operation McClaude is a modular, zero-amnesia, container-optimized multi-agent execution platform. The system operates as a hybrid edge-cloud pipeline: hardware audio capture and local command-and-control (C2) run inside the local Linux environment (Chromebook Crostini / container), while heavy multimodal processing, speech synthesis, and context caching route to Google Cloud / Vertex AI (v1beta Live API).

                        ┌────────────────────────────────────────────────────────┐  
                        │             OPERATOR WORKSTATION / C2 HUD             │  
                        │   • 16kHz PCM16 WebAudio Stream                        │  
                        │   • Bidirectional WebSocket (BidiGenerateContent)     │  
                        │   • Dual-Pane Visual Telemetry Console                 │  
                        └───────────────┬────────────────────────▲───────────────┘  
                                        │                        │  
                    wss:// RealtimeAudio│                        │ wss:// Audio & ToolCall  
                                        ▼                        │  
                        ┌────────────────────────────────────────┴───────────────┐  
                        │      GEMINI MULTIMODAL LIVE / VERTEX AI FABRIC         │  
                        │   • Full-Duplex Multimodal Reasoning                   │  
                        │   • 32k Token Context Caching Deduplicator             │  
                        │   • Function Call JSON Generation                      │  
                        └───────────────┬────────────────────────────────────────┘  
                                        │  
                                        │ Tool Call Payload (JSON-RPC)  
                                        ▼  
                        ┌────────────────────────────────────────────────────────┐  
                        │           FASTAPI LOCAL INGRESS ROUTER                 │  
                        │   • Port 8000 Static & API Host                        │  
                        │   • POST /api/dispatch Bridge                          │  
                        └───────────────┬────────────────────────────────────────┘  
                                        │  
                                        ▼  
                        ┌────────────────────────────────────────────────────────┐  
                        │          TOOL TRANSLATOR & WORKSPACE JAIL             │  
                        │   • 7 Canonical Primitives                             │  
                        │   • Path Traversal Containment (Strict Root Jail)      │  
                        └───────┬───────────────┬────────────────┬───────────────┘  
                                │               │                │  
          ┌─────────────────────┘               │                └─────────────────────┐  
          ▼                                     ▼                                      ▼  
┌─────────────────────────┐         ┌─────────────────────────┐            ┌─────────────────────────┐  
│   STATE & MEMORY ENGINE │         │   GIT WORKTREE RUNNER   │            │   OTEL & CLOUD AUDIT    │  
│ • state.md (Scratchpad) │         │ • Ephemeral Git Sandbox │            │ • Execution Traces      │  
│ • memories.json (Arch)  │         │ • Subagent Subprocesses │            │ • Cloud Run Deploy      │  
│ • Auto-Prompt Hydration │         │ • Non-Destructive Merge │            │ • Forensic Audit Log    │  
└─────────────────────────┘         └─────────────────────────┘            └─────────────────────────┘

## **2\. Complete File & Directory Structure**

Plaintext  
mcclaude-platform/  
├── .env.example  
├── .gitignore  
├── Dockerfile  
├── pyproject.toml  
├── requirements.txt  
├── README.md  
├── memories.json  
├── state.md  
├── modules/  
│   ├── \_\_init\_\_.py  
│   ├── mcclaude/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── translator.py           \# Module 01: Canonical Tool Dispatcher  
│   │   └── fs\_jail.py              \# Module 02: Path Containment & File Primitives  
│   ├── memory/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── state\_store.py          \# Module 03: Short-Term Sprint State  
│   │   ├── memory\_store.py         \# Module 04: Long-Term Memory Store  
│   │   └── hydration.py            \# Module 05: Prompt Hydration Engine  
│   ├── caching/  
│   │   ├── \_\_init\_\_.py  
│   │   └── cache\_gate.py           \# Module 06: Vertex 32k Cache Cost-Gate  
│   ├── worktree/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── manager.py              \# Module 07: Ephemeral Git Worktree Manager  
│   │   └── subagent.py             \# Module 08: Subagent Task IPC Runner  
│   ├── live\_ingress/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── api.py                  \# Module 11: FastAPI Ingress & Dispatch Server  
│   │   └── static/  
│   │       ├── audio\_worklet.js    \# Module 09: 16kHz PCM16 Audio Worklet  
│   │       ├── ws\_client.js        \# Module 10: Gemini Live WebSocket Client  
│   │       └── index.html          \# Module 12: Dark-Mode C2 HUD Frontend  
│   └── telemetry/  
│       ├── \_\_init\_\_.py  
│       ├── otel.py                 \# Module 12: OpenTelemetry Audit Tracer  
│       └── orchestrator.py         \# Module 13: Cloud Run Execution Controller  
└── tests/  
    ├── \_\_init\_\_.py  
    ├── conftest.py  
    ├── test\_router.py  
    ├── test\_fs\_jail.py  
    ├── test\_memory.py  
    ├── test\_caching.py  
    ├── test\_worktree.py  
    ├── test\_live\_dispatch.py  
    └── test\_live\_e2e.py

## **3\. Module Breakdown (1 to 13\)**

### **Module 01: Canonical Tool Dispatcher (modules/mcclaude/translator.py)**

* **Responsibility:** Normalizes heterogeneous LLM tool call schemas into 7 canonical execution primitives. Enforces strict parameter mapping and returns uniform JSON responses.  
* **Inputs:** tool\_name (str), arguments (dict).  
* **Outputs:** Execution payload {"status": "success" | "error", "output": Any, "execution\_time\_ms": float}.  
* **Key Logic:** Dispatches only the 7 approved actions: read\_file, write\_file, edit\_file, execute\_bash, mcp\_\_brain\_\_save\_state, mcp\_\_brain\_\_save\_memories, Agent.  
* **Dependencies:** Python Standard Library (inspect, json, time).

### **Module 02: Workspace File System Jail (modules/mcclaude/fs\_jail.py)**

* **Responsibility:** Executes deterministic, safe filesystem I/O operations (read\_file, write\_file, edit\_file) and sandboxed shell execution (execute\_bash).  
* **Inputs:** Target path strings, contents, search/replace blocks, shell command strings.  
* **Outputs:** File contents, patch status confirmation, or command stdout/stderr/returncode.  
* **Key Logic:** \* Path resolution: os.path.commonpath(\[workspace\_root, target\_path\]) \== workspace\_root. Rejects any traversal using ../.  
  * Atomic writes: Writes to .tmp file and performs atomic os.replace.  
  * Command timeouts: subprocess.run(..., timeout=120, capture\_output=True).  
* **Dependencies:** Standard library os, pathlib, subprocess.

### **Module 03: Short-Term Sprint State Store (modules/memory/state\_store.py)**

* **Responsibility:** Reads and mutates dynamic sprint state stored in state.md.  
* **Inputs:** Updated task lists, sprint objectives, blocker notes.  
* **Outputs:** Structured state object / Markdown buffer.  
* **Key Logic:** Parsing and updating markdown headers (\#\# Active Phase, \#\# Task Queue, \#\# Blockers).  
* **Dependencies:** pathlib.

### **Module 04: Long-Term Memory Repository (modules/memory/memory\_store.py)**

* **Responsibility:** Reads, writes, and deduplicates persistent architectural rules and system constraints in memories.json.  
* **Inputs:** Memory keys, categorizations, rule declarations.  
* **Outputs:** Queryable dictionary of persistent parameters.  
* **Key Logic:** Key-value schema validation with duplicate key prevention and timestamped updates.  
* **Dependencies:** json, pathlib.

### **Module 05: Auto-Hydration Prompt Compiler (modules/memory/hydration.py)**

* **Responsibility:** Prepend persistent memory and state directly into model system instructions prior to session initialization.  
* **Inputs:** Base system prompt, state.md, memories.json.  
* **Outputs:** Fully hydrated system prompt string.  
* **Key Logic:** Assembles context block:  
  Markdown  
  \# McClaude Memory Context  
  \#\# Persistent Memory:  
  {memories.json}  
  \#\# Active System State:  
  {state.md}

* **Dependencies:** modules.memory.state\_store, modules.memory.memory\_store.

### **Module 06: Vertex Context Caching Gate (modules/caching/cache\_gate.py)**

* **Responsibility:** Evaluates outbound prompt token depth against the $32\\text{k}$ token threshold ($32,768$) to invoke Google Cloud Context Caching.  
* **Inputs:** Hydrated system prompt, codebase payload string.  
* **Outputs:** cache\_id (str) or None (standard pass-through).  
* **Key Logic:**  
  * Computes hashlib.sha256(context.encode()).hexdigest().  
  * Token estimation: If token\_count \>= 32768, calls Google GenAI SDK client.aio.caches.create().  
* **Dependencies:** google-genai, hashlib.

### **Module 07: Ephemeral Git Worktree Manager (modules/worktree/manager.py)**

* **Responsibility:** Spawns and prunes isolated Git worktree sandboxes to eliminate blast radius during automated code modifications.  
* **Inputs:** task\_id (str), base\_branch (str).  
* **Outputs:** Worktree directory path (/tmp/worktrees/\<task\_id\>).  
* **Key Logic:**  
  * Spawns: git worktree add \-b agent/\<task\_id\> /tmp/worktrees/\<task\_id\> HEAD.  
  * Teardown: git worktree remove \--force /tmp/worktrees/\<task\_id\>.  
* **Dependencies:** git, subprocess, shutil.

### **Module 08: Subagent Task Runner (modules/worktree/subagent.py)**

* **Responsibility:** Dispatches autonomous subagent execution loops inside isolated worktrees.  
* **Inputs:** Subagent instruction payload, isolation flag (True/False).  
* **Outputs:** Subagent diff report, unit test execution status, execution stdout/stderr.  
* **Key Logic:** Spawns asynchronous worker subprocess confined strictly to the designated worktree path.  
* **Dependencies:** asyncio, modules.worktree.manager.

### **Module 09: WebAudio PCM16 Downsampling Worklet (modules/live\_ingress/static/audio\_worklet.js)**

* **Responsibility:** Captures hardware mic input at native sample rates (e.g., 44.1kHz / 48kHz) and downsamples in real time to 16kHz mono PCM16 Int16 chunks.  
* **Inputs:** Float32 audio frame buffer from browser microphone.  
* **Outputs:** 16kHz Int16 linear PCM byte chunks.  
* **Key Logic:** Linear interpolation downsampling algorithm running in an isolated AudioWorkletProcessor thread.  
* **Dependencies:** Browser Web Audio API.

### **Module 10: Gemini Live WebSocket Engine (modules/live\_ingress/static/ws\_client.js)**

* **Responsibility:** Manages full-duplex WebSocket session with Google Gemini Multimodal Live API.  
* **Inputs:** 16kHz PCM16 audio chunks, text turns, tool response JSON.  
* **Outputs:** Synthesized model audio frames (24kHz PCM), text transcriptions, toolCall JSON events.  
* **Key Logic:**  
  * Connects to wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent?key=API\_KEY.  
  * Sends initial setup JSON configuring model (models/gemini-2.0-flash-exp or gemini-2.0-flash), response modalities (\["AUDIO"\]), and tool definitions.  
* **Dependencies:** Native Browser WebSocket API.

### **Module 11: FastAPI Ingress & Tool Dispatch Server (modules/live\_ingress/api.py)**

* **Responsibility:** Hosts static C2 assets and exposes the local bridge endpoint for tool execution.  
* **Inputs:** HTTP GET requests for HUD assets, HTTP POST requests to /api/dispatch.  
* **Outputs:** Static HTML/JS files, tool execution JSON.  
* **Key Logic:**  
  * Mounts static directory via app.mount("/", StaticFiles(directory=static\_dir, html=True), name="static").  
  * Route POST /api/dispatch deserializes {"tool": str, "args": dict} and invokes modules.mcclaude.translator.dispatch().  
* **Dependencies:** fastapi, uvicorn, pydantic.

### **Module 12: OpenTelemetry Audit Tracer (modules/telemetry/otel.py)**

* **Responsibility:** Intercepts all tool executions, bash commands, and state mutations to produce structured, immutable audit traces.  
* **Inputs:** Tool execution metadata, start/stop timestamps, error traces.  
* **Outputs:** Structured OTel spans exported to local logs or GCP Cloud Trace.  
* **Key Logic:** Standard OpenTelemetry TracerProvider instrumenting function execution decorators.  
* **Dependencies:** opentelemetry-api, opentelemetry-sdk.

### **Module 13: Cloud Run Orchestrator (modules/telemetry/orchestrator.py)**

* **Responsibility:** Encapsulates the runtime environment into a containerized deployable image on GCP Cloud Run for autonomous, headless execution.  
* **Inputs:** Container environment variables, GCP Service Account credentials.  
* **Outputs:** Production cloud service endpoint routing tool dispatches.  
* **Key Logic:** Multi-stage Docker build running Uvicorn on $PORT with Secret Manager key injection.  
* **Dependencies:** Docker, Google Cloud SDK.

## **4\. Integration & State Management**

### **Multimodal Signal Flow & Tool Dispatch Loop**

\[ Operator Voice \]   
       │   
       ▼  
(1) AudioWorklet (16kHz PCM16 downsampled buffer)  
       │   
       ▼  
(2) ws\_client.js ──\> wss://generativelanguage.googleapis.com (BidiGenerateContent)  
                          │  
                          ▼  
                     \[ Gemini Live Model \]  
                          │  
                          ▼  
(3) WebSocket Message \<── toolCall: { "name": "execute\_bash", "args": {"command": "pytest"} }  
       │  
       ▼  
(4) ws\_client.js ──\> POST http://localhost:8000/api/dispatch  
                          │  
                          ▼  
(5) FastAPI Router ──\> translator.dispatch("execute\_bash", {"command": "pytest"})  
                          │  
                          ▼  
(6) fs\_jail / subprocess ──\> executes command, captures stdout/stderr  
                          │  
                          ▼  
(7) HTTP Response \<── { "status": "success", "output": "262 passed" }  
       │  
       ▼  
(8) ws\_client.js ──\> WebSocket Send: toolResponse: { "response": { "output": "262 passed" } }  
                          │  
                          ▼  
(9) Gemini Live Model ──\> Synthesizes voice audio response: "All 262 tests passed."  
       │  
       ▼  
(10) ws\_client.js \<── 24kHz PCM16 Output Chunks ──\> WebAudio Context Speaker Output

## **5\. Setup & Execution Steps**

### **1\. Environment Provisioning (Local / Crostini)**

Bash  
\# Clone the repository  
git clone https://github.com/MrPat420/McClaude.git \~/platform  
cd \~/platform

\# Create virtual environment with Python 3.12+  
python3 \-m venv venv  
source venv/bin/activate

\# Upgrade pip and install core dependencies  
pip install \--upgrade pip  
pip install fastapi uvicorn pydantic pytest opentelemetry-api opentelemetry-sdk google-genai

### **2\. Dependency Manifest (requirements.txt)**

Plaintext  
fastapi\>=0.115.0  
uvicorn\[standard\]\>=0.30.0  
pydantic\>=2.8.0  
pytest\>=8.3.0  
opentelemetry-api\>=1.26.0  
opentelemetry-sdk\>=1.26.0  
google-genai\>=0.1.0

### **3\. Execution Verification Suite**

Run the full test harness to verify primitive safety, worktree sandboxing, and dispatch routes:

Bash  
pytest \-v tests/

### **4\. Booting the C2 Cockpit HUD**

Bash  
\# Kill any zombie process on port 8000  
kill \-9 $(lsof \-t \-i:8000) 2\>/dev/null || true

\# Launch the Uvicorn ingress server  
source venv/bin/activate && python3 \-c "  
import uvicorn  
from modules.live\_ingress.api import create\_app  
uvicorn.run(create\_app(), host='127.0.0.1', port=8000)  
"

### **5\. Accessing the Command Bridge**

* Open your browser and navigate to: **http://localhost:8000**  
* Hold **Shift** and click **Connect** to set your active Gemini API key.  
* The C2 HUD is now live and synchronized with the 13-module execution pipeline.