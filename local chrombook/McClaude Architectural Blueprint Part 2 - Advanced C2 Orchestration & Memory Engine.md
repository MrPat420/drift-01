# **[[McClaude]] Architectural Blueprint Part 2: Advanced [[C2]] Orchestration, State Management & Gemini Silicon Bridge**

**Project:** McClaude (Autonomous Agentic CLI & C2 Control Plane)  
**Author:** Shaun Patrick Kelly  
**Date:** August 12, 2026  
**Parent Blueprint:** McClaude Architectural Blueprint & GCP Migration Strategy (Part 1\)  
Target Infrastructure: Google Cloud Platform (Vertex AI, Cloud Run, Secret Manager, GCS) & OpenRouter API

# **1\. Architectural Layering Rationale & "Engine vs. Transmission" Paradigm**

## **1.1 Foundation & Layering Rationale**

Part 1 established the foundational infrastructure of McClaude: the three-tier decoupling of the CLI Control Plane from the Data/Model Plane, GCP Cloud Run hosting, Secret Manager key isolation, basic MCP tool translation (Read, Write, Edit, exec\_bash, Agent), and initial dynamic model routing between Vertex AI and OpenRouter.

Part 2 layers the operational C2 execution engine directly on top of Part 1\. It bridges Anthropic's Model Context Protocol (MCP) task and memory schemas with Google's Vertex AI enterprise infrastructure.

## **1.2 The "Engine vs. Transmission" Paradigm**

* **Google Silicon (The Engine):** Gemini 2.5/3.0 Pro and Flash models provide unmatched raw cognitive compute: a 1M to 2M token native context window, sub-second multimodal comprehension, and low-cost explicit context caching on Vertex AI.  
* **Claude MCP Protocol (The Transmission):** Anthropic's local I/O architecture provides a precise, opinionated control layer. It defines clean filesystem mappings, multi-agent C2 hierarchies (Commander \-\> Vice Commander (XO) \-\> Watch Station \-\> Unit Agents), deterministic task state tracking, and second-brain memory persistence.  
* **The Layered Synthesis:** McClaude hijacks the Anthropic MCP tool definitions and task state machine, wrapping them into a sanitized protocol translation bridge that routes execution directly to Vertex AI Gemini endpoints and OpenRouter worker models.

# **2\. Vectorless Memory Architecture (mcp\_\_brain Middleware)**

## **2.1 Eliminating Vector Database Overhead**

Traditional multi-agent systems rely on heavy external vector databases (e.g., Pinecone, Milvus, Qdrant) for Retrieval-Augmented Generation (RAG). McClaude replaces vector DB complexity with local filesystem frontmatter (Markdown files with YAML headers) mounted directly into Vertex AI's Explicit Context Cache.

## **2.2 Dual-Layer Memory Engine**

* **Layer 1 Memory (mcp\_\_brain\_\_save\_state / get\_state):**  
  * Maintains the active project state note (./memory/state.md).  
  * Structurally partitioned into: Now (Active Focus), In Flight (Active Subagents), Decisions (Locked Architecture), Blockers, and Next Steps.  
  * Overwritten in-place during milestone transitions to maintain a single source of truth.  
* **Layer 2 Memory (mcp\_\_brain\_\_save\_memories / search\_context):**  
  * Stores durable, distilled knowledge in structured JSON/Markdown (./memory/memories.json).  
  * Implements title-based refresh-in-place, deduplication, and supersedes tracking.  
  * Records critical architectural decisions, resolved bugs, environment quirks, and compliance constraints.

## **2.3 Vertex AI Context Cache Binding**

When working across large codebases (\>32k tokens), McClaude serializes and mounts the entire /memory/ repository directly into a Vertex AI Context Cache. Because Gemini 2.5/3.0 Pro supports up to 2M tokens, the model evaluates the complete project history, current state, and codebase simultaneously without retrieval latency or chunking loss.

# **3\. Deterministic C2 Command & Task Orchestration**

## **3.1 C2 Command Hierarchy**

1. **Commander (Strategic Level \- Gemini Pro / Vertex AI):** High-level decision making, system architecture, policy compliance, and major milestone approval.  
2. **Vice Commander / XO (Overwatch Level \- Gemini Pro / Vertex AI):** Operational monitoring, inter-agent coordination, plan evaluation, and risk mitigation.  
3. **Watch Station (Tactical Supervisor \- Gemini Flash / OpenRouter):** Context management, task queue dispatching, and error monitoring.  
4. **Unit Agents (Worker Level \- OpenRouter / DeepSeek / GLM / Llama):** Granular file edits, code linting, test execution, and targeted web research.

## **3.2 Deterministic Task State Machine**

To prevent agent drift and hallucination across multi-step execution loops, McClaude enforces deterministic task graphs using TaskCreate, TaskUpdate, and Workflow primitives:

* **Dependency Blocking:** Tasks support strict parent/child and blocking relationships (blocked\_by). Task B is hard-blocked from execution until Task A returns a completed status.  
* **State Verification:** Task status moves strictly through pending \-\> in\_progress \-\> completed | failed.  
* **Execution Validation:** Agents are prohibited from freestyling; every mutation must be logged against a specific active Task ID.

## **3.3 Asynchronous Execution & Self-Paced Loops**

* **Git Worktree Isolation (EnterWorktree / ExitWorktree):** Parallel subagents are spawned inside isolated git worktrees, preventing race conditions or dirty working tree collisions during concurrent code edits.  
* **Self-Paced Resumption (ScheduleWakeup, CronCreate, Monitor):** Allows long-running or non-blocking background operations to stream stdout events and wake the main execution loop upon completion.

# **4\. Expanded [[MCP]] Tool Registry & Translation Schemas**

Part 2 expands the tool registry established in Part 1 to full MCP feature parity:

## **4.1 File System & Discovery Operations**

* **Read(path, line\_range):** Reads local files with line slicing and image/PDF support.  
* **Write(path, content):** Performs atomic file creation or complete overwrites.  
* **Edit(path, old\_str, new\_str):** String replacement with mandatory pre-read and uniqueness validation.  
* **NotebookEdit(path, cell\_index, content):** Edits specific cells in Jupyter notebooks.  
* **Grep(pattern, path, context):** Regex content search with context line control (-A/-B/-N).  
* **Glob(pattern):** File pattern matching supporting recursive wildcards (\*\*/\*).  
* **WebSearch(query) & WebFetch(url):** Live web querying and URL-to-markdown conversion.

## **4.2 Task & Orchestration Primitives**

* **TaskCreate(title, description, blocked\_by):** Adds a structured task to the execution graph.  
* **TaskUpdate(task\_id, status, output):** Updates status and records task output.  
* **Workflow(phase\_list):** Executes multi-stage deterministic agent workflows.  
* **Agent(prompt, isolation, subagent\_type):** Spawns an isolated subagent process.  
* **SendMessage(recipient, message):** Inter-agent bus communication between subagents and the main controller.

## **4.3 Memory & Environment Management**

* **mcp\_\_brain\_\_get\_state():** Retrieves active project state (memory/state.md).  
* **mcp\_\_brain\_\_save\_state(content):** Synthesizes and updates Layer 1 project state.  
* **mcp\_\_brain\_\_save\_memories(memories\[\]):** Stores distilled Layer 2 facts and decisions.  
* **mcp\_\_brain\_\_search\_context(query):** Historical context search across project conversations.  
* **EnterPlanMode() / ExitPlanMode():** Switches between architectural planning and code execution modes.  
* **EnterWorktree() / ExitWorktree():** Isolates agent execution within a clean git worktree.

# **5\. Operational Boundaries & Security Protocols**

## **5.1 Security & Compliance Constraints**

* Operations are restricted to authorized development, pentesting, CTF, defensive security, and research contexts.  
* Destructive actions, unhedged outward-facing deployments, and mass-targeting requests are blocked at the MCP Bridge layer.  
* Dual-use security tools require explicit authorization flags in project configuration.

## **5.2 Permission-Based Execution & Fallbacks**

* **Tool Call Refusal Handling:** Denied or failed tool calls trigger structural parameter adjustment rather than verbatim retries.  
* **Truthful Outcome Reporting:** System output reports plain facts (test failures, skipped steps, execution errors) without hedging or false success claims.  
* **Environment Isolation:** Non-interactive shell environments manage explicit PATH definitions, environment variables, and sandboxed subprocess execution.

# **6\. Implementation & Deployment Roadmap (Phases 5–8)**

## **Phase 5: mcp\_\_brain Memory Engine & Context Cache Binding (Weeks 9–10)**

* Implement local Markdown/YAML frontmatter state parser and Layer 2 memory deduplication engine.  
* Build automated Vertex AI Explicit Context Cache refresher triggered on mcp\_\_brain\_\_save\_state calls.

## **Phase 6: Deterministic Task Tracker & Dependency Engine (Weeks 11–12)**

* Develop the core TaskCreate, TaskUpdate, and Workflow state machine middleware.  
* Enforce DAG dependency blocking before dispatching tasks to worker models.

## **Phase 7: Parallel Agent Worktree & Inter-Agent Bus (Weeks 13–14)**

* Integrate git worktree management into the Agent primitive for non-interfering parallel agent sub-processes.  
* Build SendMessage IPC bus for real-time inter-agent status updates and result pass-through.

## **Phase 8: End-to-End C2 Loop Integration & Production Hardening (Weeks 15–16)**

* Deploy full 4-tier C2 command loop connecting Vertex AI Gemini Pro/Flash with OpenRouter worker nodes.  
* Validate zero-data-retention compliance, budget guardrails, and automated Cloud Run scaling under heavy multi-agent workloads.

