---
name: ground-up-dag-compiler
description: |
  Antigravity skill that parses a workspace, builds a deterministic prerequisite DAG (CINCO‑01), and enforces O(1) Wiki_LLM key‑lookup rules before context hydration.
trigger: "ground-up dag compile"
---

# Overview
This skill implements the deterministic pipeline created in the **COGNITIVE_INCUBATOR__GROUND_UP** sandbox. It performs:
1. **Ingress token sanitization** (SCRUB‑01 logic) – removes volatile session noise.
2. **Grade 1..N prerequisite DAG parsing** – extracts  annotations, validates against , and asserts acyclic ordering.
3. **Wiki_LLM O(1) key‑lookup** – builds an  mapping entity keys to exact file offsets.
4. **SENTINEL‑01 AST verification** – runs AST gates on each node before allowing downstream emission.

# Parameters
-  *(string, required)* – Absolute path to the workspace to analyse.
-  *(string, required)* – Directory where the compiled DAG JSON () will be written.
-  *(boolean, default: true)* – Fail on any schema violation, missing prerequisite, or AST gate error.

# Execution Steps (Python pseudocode)
dag_node ... dag_node\n(.*?)\n

# Verification
- Run the bundled unit test  (generated alongside this skill).
- Validate the output JSON against  using .
- Ensure the command exits with status 0 for deterministic pipelines.

# License & Attribution

