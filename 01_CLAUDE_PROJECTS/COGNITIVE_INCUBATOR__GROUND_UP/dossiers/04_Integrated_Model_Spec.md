# 04_Integrated_Model_Spec

## End‑to‑End Signal Path
```
[Ingress Scrubbing (SCRUB‑01)]
    → [Level 4 Invariant Anchor (T₀)]
    → [CINCO‑01 Causal DAG Traversal]
    → [Exact Key Resolution (Wiki_LLM O(1) Registry)]
    → [SENTINEL‑01 AST/Kinematics Gate]
    → [Deterministic Emission]
```
The pipeline enforces strict layered verification: each stage must emit a **state token** that the downstream stage validates before proceeding.

## Sub‑System Interface Contracts
| From → To | Payload Type | Required Fields | Validation |
|---|---|---|---|
| SCRUB‑01 → T₀ | JSON `{ "clean_tokens": int, "scrub_hash": string }` | `clean_tokens`, `scrub_hash` | SHA‑256 of pre‑scrub input must match `scrub_hash`.
| T₀ → DAG Traversal | JSON `{ "invariant_id": string, "anchor_hash": string }` | `invariant_id` (e.g., `L4_INVARIANT`), `anchor_hash` | `anchor_hash` must correspond to a known Level 4 invariant hash.
| DAG Traversal → Key Registry | JSON `{ "required_keys": [string], "resolved": [{"entity_key":string,"offset":{ "start":int,"end":int}}] }` | `required_keys`, `resolved` | All `required_keys` must resolve; otherwise emit `UNKNOWN_ENTITY`.
| Key Registry → AST Gate | JSON `{ "entity_key":string, "source_file":string, "byte_range":[int,int], "payload":object }` | `entity_key`, `source_file`, `byte_range`, `payload` | Byte range must be within file bounds; payload is the deterministic AST fragment.
| AST Gate → Emission | JSON `{ "ast_hash":string, "output":string }` | `ast_hash`, `output` | `ast_hash` must match SHA‑256 of the AST payload.

## Hardware Alignment & Zero‑Remanence Memory
- **eMRAM cache**: Stores immutable invariant anchors (`T₀`) with hardware‑enforced write‑once semantics, guaranteeing zero‑remanence after power‑cycle.
- **Fast‑State Non‑Volatile Registers**: Hold DAG traversal state (`node_id`, `grade_level`) with atomic update guarantees, preventing stale state propagation.
- **Cache‑Coherency Protocol**: Guarantees that any change to the `entity_key_registry` triggers a hardware‑level invalidation signal, ensuring all downstream stages read the latest offset.

## Deterministic Guarantees
1. **No probabilistic inference** – every token emitted is traceable to a source offset via O(1) lookup.
2. **State‑Machine Halt on Failure** – encountering `UNKNOWN_ENTITY`, `UNKNOWN_DEPENDENCY`, or `PREREQUISITE_FAILURE` aborts the pipeline with a deterministic error report.
3. **Replayability** – given identical inputs, the pipeline reproduces the exact same output hash, enabling rigorous regression testing.

---
*Compiled from the CINCO‑01 DAG schema and findings (see `findings.md`).*
