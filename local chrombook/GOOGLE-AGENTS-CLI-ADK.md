---
title: "Google Agents CLI + ADK — Agent Build/Deploy Pipeline"
kb_type: wiki
topic: agent-frameworks
source: https://docs.cloud.google.com/gemini-enterprise-agent-platform/agents/quickstart-adk
source_date: 2026-08-07
captured: 2026-08-10
license: CC-BY-4.0 (text), Apache-2.0 (code samples)
tags: [google, adk, agents-cli, gemini, cloud-run, agent-deployment, cc-compatible]
---

# Google Agents CLI + ADK

## What it is

Two-layer stack for building AI agents on Google Cloud's Gemini Enterprise Agent Platform:

- **ADK (Agent Development Kit)** — open-source, code-first Python framework for defining agents (adk.dev).
- **Agents CLI** (`google-agents-cli`) — machine-readable wrapper around ADK designed to be driven *by* an AI dev tool (Claude Code, Gemini CLI, Codex), not by the human directly. It ships "skills" that give the AI tool expert context on scaffolding, ADK patterns, evals, and GCP deployment.

Key architectural point: the human issues natural-language prompts to their AI tool; the AI tool invokes `agents-cli` commands. Only one command is run by the human directly — the setup bootstrap.

## Operator workflow

1. Prereqs: GCP project with Agent Platform API enabled; an AI dev tool installed (CC qualifies).
2. Install `uv`, then bootstrap: `uvx google-agents-cli setup` — the only human-run command.
3. Everything else is prompt-driven through the AI tool.

## Prompt → action map

| Prompt to AI tool | What happens |
| --- | --- |
| "Use agents-cli to build an agent that..." | Activates workflow + scaffold skills; writes `DESIGN_SPEC.md`; runs `agents-cli create <name> --prototype --yes` and `agents-cli install` |
| "Write evaluations and run them" | Eval skill; creates `tests/eval/evalsets/*.evalset.json`, LLM-as-judge config in `tests/eval/eval_config.json`; runs `agents-cli eval run` |
| "Deploy this to Cloud Run" | Deploy skill; `agents-cli scaffold enhance --deployment-target cloud_run`, then `agents-cli deploy` — returns service URL |
| "Set up observability" | Provisions service account, GCS bucket, BigQuery dataset; Cloud Trace is on by default |

## Agent definition pattern (ADK)

Agent = Python object with `name`, `model` (e.g. `Gemini(model="gemini-3.5-flash")`), and an `instruction` system prompt containing rules plus few-shot examples. Local test via `agents-cli run "<test input>"`. Iteration loop: run evals → give corrective natural-language feedback to the AI tool → it edits instructions → re-run evals.

## Templates noted

- `adk_a2a` — multi-agent / agent-to-agent systems
- `agentic_rag` — RAG over own documentation
- Tool integration (e.g. Google Search) via prompt

## Portfolio relevance

- **CC-compatible**: Agents CLI is explicitly designed to be driven by Claude Code — fits the existing directive→CC execution model with zero workflow change.
- **Skill-encapsulation pattern**: same principle as INSTSET architecture — behavioral rules in the instruction field, domain expertise packaged as skills the executor loads. Worth studying as external validation of the pattern.
- **Eval loop**: `agents-cli eval run` + LLM-as-judge + corrective feedback iteration is a formalized version of the Y-TIP guardrail-tuning cycle. Candidate pattern for GEM-01 classifier QA.
- **Cost caution**: deployment lands on GCP billed runtimes (Cloud Run/GKE/Agent Runtime); observability provisioning creates billable GCS + BigQuery resources. Any hands-on trial needs explicit budget authorization per standing policy.

## Verification status

Documentation capture only — not tested locally. No claims verified against a live GCP project.
