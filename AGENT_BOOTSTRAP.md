# AGENT BOOTSTRAP PROTOCOL // ZERO-TOUCH EXOSKELETON ONBOARDING

> **INSTRUCTION FOR AI AGENTS (Claude, Anti-G, ChatGPT, Cursor, Windsurf):**
> Autonomous onboarding manifest for the Cognitive Exoskeleton Framework.

---

## Autonomous Setup Directive

### 1. Environment Initialization
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip fastapi uvicorn pydantic anyio annotated-doc jsonschema
```

### 2. Verify Physical Binaries & Skills
```bash
mkdir -p ~/.local/bin ~/.agent/skills
systemctl --user is-active byteaddr-shim.service || echo "Start shim daemon on :9001"
```

### 3. Execution Sanity Sweep
```bash
byteaddr-cli list --type entity --limit 1
drift-guard --help
swarm-arbiter --help
ip-genealogy --help
hw-audit --help
```

## Core Architecture Matrix

| Priority | Identifier | Interface | Function |
|:---|:---|:---|:---|
| **P0** | **Ground-Up DAG** | AST Schema Gate | Halts circular dependencies & enforces causal rules |
| **P0** | **ByteAddress MCP** | Port 9001 (systemd) | Deterministic O(1) byte-offset exact memory indexer |
| **P0** | **CINCO Drift Guard** | CLI Telemetry | KV-cache degradation & hallucination tripwire |
| **P1** | **Swarm Arbiter** | Multi-LLM API | Red-team divergence & multi-model consensus |
| **P2** | **IP Genealogy** | Causal Lineage | SHA-256 Title 18 forensic evidence & provenance tree |
| **P3** | **Hardware Auditor** | Heuristic / Rotor | Key-rotation quotas & perimeter security sweep |
