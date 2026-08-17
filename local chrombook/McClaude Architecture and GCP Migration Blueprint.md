# **McClaude Architectural Blueprint & GCP Migration Strategy**

**Project:** [[McClaude]] (Autonomous Agentic CLI & C2 Control Plane)  
**Author:** Shaun Patrick Kelly  
**Date:** Date  
**Target Infrastructure:** [[Google Cloud Platform]] ([[Vertex AI]], Cloud Run, Secret Manager, GCS) & OpenRouter API

# **1\. Executive Summary & Migration Rationale**

## **1.1 Background & Motivation**

The objective of McClaude is to build an open-source, highly cost-effective, and fully controlled alternative to Anthropic's Claude Code CLI and agentic ecosystem. While Claude Code offers powerful terminal-native workflows and structured tool-calling capabilities, it introduces severe operational bottlenecks:

* **Cost & Rate Limits:** High API costs for long-context tasks and strict rate limits on Sonnet/Opus models.  
* **Ecosystem Lock-in:** Proprietary dependencies on Anthropic's Messages API and lack of explicit context caching controls.  
* **Lack of Custom Routing:** Inability to dynamically offload high-volume subagent worker tasks to lower-cost open/third-party LLMs.

## **1.2 The [[McClaude]] Vision**

McClaude decouples the **Control Plane** (CLI interface, MCP tool schemas, memory state management, git worktree isolation) from the **Data/Model Plane** (the underlying LLMs).

By hosting the middleware on **[[Google Cloud Platform]] ([[GCP]])** and leveraging **Vertex AI** for heavy reasoning alongside **[[OpenRouter]]** for cost-sensitive subagent tasks, McClaude achieves:

1. **80%+ Cost Reduction:** Through Vertex AI Explicit Context Caching and OpenRouter model routing.  
2. **Infinite Context Efficiency:** Leveraging Gemini 2.5/3.0 Pro's 1M–2M context window.  
3. **Structured C2 Command Hierarchy:** Maintaining the `Commander -> Vice Commander (XO) -> Watch Station -> Unit Agents` command and control workflow.  
4. **Data Sovereignty:** Zero-data-retention compliance on Google Vertex AI enterprise instances.

# **2\. Three-Tier System Architecture**

┌─────────────────────────────────────────────────────────────────────────────┐

│                       TIER 1: LOCAL CLI / CONTROL PLANE                      │

│   • Terminal Interface (Rich / Typer CLI)                                    │

│   • Local Filesystem Driver (Read, Write, Edit, exec\_bash)                  │

│   • Git Worktree Isolation Engine (Parallel Subagents)                      │

│   • Local Markdown Memory Store (memory/state.md, memory/memories.json)      │

└──────────────────────────────────────┬──────────────────────────────────────┘

                                       │

                                       ▼

┌─────────────────────────────────────────────────────────────────────────────┐

│                    TIER 2: MCP BRIDGE & ROUTING MIDDLEWARE                  │

│   • Protocol Converter: Anthropic MCP Tool Schemas ↔ Google GenAI Tools      │

│   • Vertex AI Explicit Context Cache Manager (Codebase freezing)             │

│   • Dynamic Model Router (Latency / Cost / Complexity Rules)                │

│   • Hosted Backend Option: GCP Cloud Run \+ Secret Manager \+ GCS State        │

└──────────────────────────────────────┬──────────────────────────────────────┘

                                       │

                    ┌──────────────────┴──────────────────┐

                    ▼                                     ▼

┌──────────────────────────────────────┐┌─────────────────────────────────────┐

│     GOOGLE SILICON ENGINE (VERTEX AI)││         OPENROUTER API ROUTER       │

│  • Gemini 3.0 / 2.5 Pro (Overwatch)  ││  • GLM-5.2 / DeepSeek-Coder (Worker) │

│  • Gemini 2.5 Flash (Tactical Agent) ││  • Llama 3.3 / Qwen (Subagent tasks)│

└──────────────────────────────────────┘└─────────────────────────────────────┘

# **3\. Tool Translation & Schema Compatibility Protocol**

McClaude translates Claude's Model Context Protocol (MCP) tool definitions into native Google GenAI `FunctionDeclaration` objects and OpenRouter OpenAI-compatible function schemas.

## **3.1 Schema Translation Matrix**

| Claude Tool Name | Native Tool / Implementation | Description |
| :---- | :---- | :---- |
| `Read` | `read_file(path, line_range)` | Python pathlib \+ line slicing |
| `Write` | `write_file(path, content)` | Atomic file write |
| `Edit` | `edit_file(path, old_str, new_str)` | Exact string replacement with uniqueness validation |
| `exec_bash` / `Bash` | `execute_bash(command, timeout)` | Sandboxed subprocess.Popen |
| `mcp__brain__save_state` | `save_state(content, project)` | Overwrites ./memory/state.md |
| `mcp__brain__save_memories` | `save_memories(memories[])` | Updates/deduplicates ./memory/memories.json |
| `Agent` | `spawn_subagent(prompt, isolation)` | Git worktree creation \+ subagent process spawn |

## **3.2 Key Tool Schemas (JSON Schema Specification)**

### **Layer 1 Memory: `mcp__brain__save_state`**

Overwrites the curated current-state note for the project (Now / In flight / Decisions / Blockers / Next).

### **Layer 2 Memory: `mcp__brain__save_memories`**

Saves distilled, deduplicated knowledge into durable Layer 2 memory with title-based refresh-in-place and supersedes tracking.

### **Orchestration Primitive: Agent**

Spawns an isolated subagent for background or focused tasks, supporting git worktree isolation.

# **4\. Google Cloud Platform (GCP) Deployment & Hosting Architecture**

McClaude supports both Local Execution Mode and Serverless Hosted Mode on GCP.

## **4.1 GCP Serverless Stack Architecture**

1. **Google Cloud Run:** Hosts the McClaude API Gateway and MCP Bridge (FastAPI/Python async container).  
2. **GCP Secret Manager:** Securely stores API keys (`OPENROUTER_API_KEY`, `VERTEX_AI_SERVICE_ACCOUNT_KEY`).  
3. **Google Cloud Storage (GCS) / Firestore:** Persists multi-device project state, session logs, and Layer 2 knowledge graphs.  
4. **Vertex AI API:** Direct access to Gemini 2.5 / 3.0 Pro & Flash models with enterprise data privacy guarantees.

## **4.2 Step-by-Step GCP Infrastructure Deployment Commands**

Includes `gcloud services enable`, Secret Manager setup, Cloud Storage bucket creation, and Cloud Run container deployment.

# **5\. Cost Optimization Strategy & Model Routing Engine**

## **5.1 Vertex AI Explicit Context Caching**

Context Caching is McClaude's primary cost-reduction mechanism. When working with large codebases (\>32k tokens), McClaude creates an explicit context cache in Vertex AI.

* **Standard Token Price (Gemini Pro):** \~$1.25 / 1M input tokens.  
* **Cached Token Price (Gemini Pro):** \~$0.30 / 1M input tokens (75%+ savings).

## **5.2 Dynamic Model Routing Matrix**

| Task Type | Recommended Model Provider | Specific Model |
| :---- | :---- | :---- |
| **Overwatch / Strategic Planning** | Vertex AI | Gemini 3.0 / 2.5 Pro |
| **Tactical Coding & File Edits** | Vertex AI | Gemini 2.5 Flash |
| **Subagent Research / Search** | OpenRouter | `z-ai/glm-5.2` or `deepseek/deepseek-coder` |
| **Bulk Code Quality / Linting** | OpenRouter | `meta-llama/llama-3.3-70b-instruct` |

# **6\. Implementation Roadmap**

## **Phase 1: Local MCP Bridge & Tool Core (Weeks 1–2)**

Establish the basic connectivity and core tool definitions required for terminal interaction.

## **Phase 2: Memory & Git Worktree Isolation (Weeks 3–4)**

Implement advanced state management and parallel execution environments using git worktrees.

## **Phase 3: Smart Router & Vertex Context Caching (Weeks 5–6)**

Deploy the routing logic and caching mechanisms to optimize performance and reduce API costs.

## **Phase 4: CLI Packaging & GCP Cloud Run Deployment (Weeks 7–8)**

Finalize the serverless deployment and package the CLI for broader distribution and project state persistence.