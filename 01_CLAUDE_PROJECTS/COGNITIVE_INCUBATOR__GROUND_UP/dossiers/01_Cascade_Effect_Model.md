# 01_Cascade_Effect_Model

## Overview
This dossier captures the core concepts of the **Cascade‑Effect Tracking Mechanism** (v2) as defined in `CASCADE_EFFECT_TRACKING_MECHANISM_DRAFT_v2_20260716.md`. It focuses on the **Mechanical vs. Judgment split** and the **Entry schema** used to log cross‑project changes.

### Mechanical vs. Judgment Split
| Aspect | Mechanical (automatable) | Judgment (requires reasoning) |
|---|---|---|
| Scope | Detects literal‑reference matches from diffs (file names, project identifiers, rule IDs). | Determines **plausible but unstated** targets, assesses risk level, writes narrative change description. |
| Auto‑filled fields | `change_id`, `date`, `source_project`, `source_artifact`, `literal_references_found` | `change_description`, `plausible_additional_targets`, `risk_level`, `reviewer`, `review_date`, `disposition_notes` |
| Reliability | Deterministic, based on exact string matches. | Human/AI review – not auto‑populated. |

### Entry Schema (v2)
| Field | Filled by | Notes |
|---|---|---|
| `change_id` | Auto | Unique identifier |
| `date` | Auto | Timestamp of detection |
| `source_project` | Auto | Originating project |
| `source_artifact` | Auto | File/commit identifier |
| `change_description` | **Judgment** | Narrative summary of the change |
| `literal_references_found` | **Mechanical** | Exact‑string matches from the diff |
| `plausible_additional_targets` | **Judgment** | Potential downstream impacts not captured mechanically |
| `risk_level` | Judgment | low / med / high |
| `review_status` | Both | `PENDING-REVIEW` → `REVIEWED — no issue` → `REVIEWED — flagged: …` |
| `reviewer` / `review_date` | Judgment | Reviewer identity and date |
| `disposition_notes` | Judgment | Decisions taken |

## Review Cadence (Two‑Tier)
1. **Routine sweep** – aligned with the existing quarterly/​milestone “Check Ride” cadence for standard‑risk entries.
2. **Triggered review** – any entry flagged `risk_level: high` is escalated to the next operator session for immediate review.

---
*Generated from the source draft on 2026‑07‑16.*
