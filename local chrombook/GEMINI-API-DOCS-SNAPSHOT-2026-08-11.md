---
title: "Gemini API — Docs Landing Snapshot (Models & Capabilities Index)"
kb_type: reference
topic: gemini-api
source: https://ai.google.dev/gemini-api/docs
date: 2026-08-11T14:09:21.168Z
captured-by: web2md pipeline (manual paste)
relevance: web2md-toolkit model selection; ADK/google-genai build targets on gws-cli-local-505120
companion-docs: [CHROMEBOOK-GCP-ENV-HANDOFF.md, "AI-Agent Development Stack research report"]
tags: [gemini, gemini-api, models, capabilities, api-reference, snapshot]
---

# Gemini API — Docs Landing Snapshot (2026-08-11)

Index of the current model lineup and capability surface as listed on the Gemini API docs landing page. Descriptions are paraphrased from the source; all model names, capability names, and doc links are preserved verbatim as factual identifiers.

## Current model lineup

| Model | Status | Positioning (paraphrased) | Docs link |
| --- | --- | --- | --- |
| Gemini 3.1 Pro | New (preview) | Top-tier intelligence; strongest multimodal understanding, reasoning-centric | https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview |
| Gemini 3.6 Flash | New | Near-frontier performance at much lower cost than larger models | https://ai.google.dev/gemini-api/docs/models/gemini-3.6-flash |
| Gemini 3.5 Flash-Lite | New | Cheapest/fastest tier; built for high-volume, low-latency subagent workloads | https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite |
| Gemini 3 Flash | Preview | Earlier Flash generation, same cost-efficiency positioning | https://ai.google.dev/gemini-api/docs/models/gemini-3-flash-preview |
| Nano Banana 2 / Nano Banana Pro | Current | Image generation and editing models | https://ai.google.dev/gemini-api/docs/image-generation |
| Veo 3.1 | Current | Video generation with native audio | https://ai.google.dev/gemini-api/docs/video |
| Gemini Robotics | Current | Vision-language model extending agentic reasoning to physical-world robotics | https://ai.google.dev/gemini-api/docs/robotics-overview |

**Pipeline note:** `web2md_agent.py` currently pins `gemini-3.6-flash` — confirmed still listed as a current "New" model on this snapshot date. Flash-Lite (3.5) is the documented option if subagent fan-out ever needs a cheaper tier.

## Capabilities index

| Capability | What it covers (paraphrased) | Docs link |
| --- | --- | --- |
| Native Image Generation (Nano Banana) | In-context image generation/editing via Gemini 2.5 Flash Image | https://ai.google.dev/gemini-api/docs/image-generation |
| Long Context | Multi-million-token input; understanding across images, video, unstructured docs | https://ai.google.dev/gemini-api/docs/long-context |
| Structured Outputs | Constrain responses to JSON for automated downstream processing | https://ai.google.dev/gemini-api/docs/structured-output |
| Function Calling | Agentic workflows — wiring Gemini to external APIs/tools | https://ai.google.dev/gemini-api/docs/function-calling |
| Video Generation (Veo 3.1) | Text- or image-prompted video creation | https://ai.google.dev/gemini-api/docs/video |
| Voice Agents (Live API) | Real-time voice applications and agents | https://ai.google.dev/gemini-api/docs/live |
| Tools | Built-in: Google Search, URL Context, Google Maps, Code Execution, Computer Use | https://ai.google.dev/gemini-api/docs/tools |
| Document Understanding | Up to 1000-page PDFs, full multimodal processing; other text file types | https://ai.google.dev/gemini-api/docs/document-processing |
| Thinking | Reasoning controls for complex/agentic tasks | https://ai.google.dev/gemini-api/docs/thinking |

**Pipeline note:** Structured Outputs + Function Calling are the two capabilities already load-bearing in the web2md pipeline (pydantic `response_schema` → Firestore handoff). URL Context under Tools is worth evaluating as a possible native alternative/supplement to the requests/BeautifulSoup ingest stage.

## Resource links

| Resource | Purpose | Link |
| --- | --- | --- |
| Google AI Studio | Prompt testing, API key management, usage monitoring, prototyping | https://aistudio.google.com |
| Developer Community | Q&A with developers and Google engineers | https://discuss.ai.google.dev/c/gemini-api/4 |
| API Reference | Full reference documentation | https://ai.google.dev/api |
| Status | Service status for Gemini API / AI Studio / model services | https://aistudio.google.com/status |

## Cross-reference to standing tasks

- API key for ADK `.env` comes from AI Studio (link above) — matches the open `.env` placeholder fix.
- `gemini-3.6-flash` note from stack research report still applies: sampling params (`temperature`/`top_p`/`top_k`) deprecated from 3.6 onward; control via thinking levels.
