---
title: "Google AI Pro Benefits — Full Reference Summary"
kb_type: wiki
topic: reference
captured: 2026-08-11
source: support.google.com/googleone/answer/14534406
status: reference-only
tags: [google-ai-pro, antigravity, android-studio, ai-studio, jules, flow, photos, health, home, reference]
---

# Google AI Pro Benefits — Full Reference Summary

Paraphrased from Google's official Google One help page (not verbatim — source page is copyrighted). Full detail: support.google.com/googleone/answer/14534406

## Dev-stack relevant

**Google Antigravity** — Gemini 3 Pro-powered dev environment for managing autonomous coding agents across editor, terminal, browser. Pro members get higher usage limits and priority traffic on Gemini 3 Pro plus other Vertex AI Model Garden models (Claude 4.5 Sonnet, gpt-oss-120b), and priority access to new experimental models. Usage is two-tiered: a time-bound baseline quota, then optional purchased AI credits once that's used. Overage handling is configurable in Antigravity's Settings/Models selector (Never charge / Always charge / manual toggle). Requires age 18+; desktop app only (Windows/macOS/Linux); English-only prompts.

**Google AI Studio** — sign in for a Playground to experiment with Gemini, Nano Banana, and Lyria models; build/prototype apps without writing code; direct access to newest dev tools and models. Also supports remixing community AI tools from an app gallery, generating pitches/case studies/speaker notes from documents or audio, generating songs/speech, and sharing chat sessions or app demos with others. Pro gives higher limits on Gemini 3.1 Pro and Nano Banana Pro.

**Gemini in Android Studio** — higher usage limits and dedicated capacity for Gemini 3 code completion and complex reasoning on Android projects. Aimed at individual devs/small teams; code is excluded from model training.

**Google Developer Program premium** — bundled with AI Pro. Includes: Gemini Code Assist with higher IDE quotas, $10/month in Google Cloud credits, 30 Firebase Studio workspaces, plus developer community/forum access. Not shareable with a family group — requires an active AI Pro membership linked to your Developer profile. Support: developers.google.com/profile/help/faq, or gdp-premium-support@google.com.

**Jules** — AI coding agent built on Gemini 2.5 Pro that independently handles coding tasks and integrates with GitHub repos. Pro tier gets higher task limits, higher concurrency, and access to newer models. Requires 18+, English only. Support via Discord (discord.com/invite/googlelabs) or jules.google/docs/changelog.

## Gemini app & productivity

- **Gemini app** — with Pro, stronger at coding, logical reasoning, following nuanced instructions, creative collaboration; runs with Gemini 3 Pro and Veo. Web, Android, iOS.
- **Deep Research** — in-depth, real-time research inside Gemini Apps; 18+, desktop and mobile, requires sign-in.
- **Gemini in Gmail, Docs, Vids** — feature availability varies by plan tier.
- **Gemini Notebook** — AI research/writing assistant. Pro gives higher limits than the Plus tier on Audio Overviews, Flashcards, Infographics, Q&A, Quizzes, Reports, Slides, Video Overviews; notebook size up to 300 sources; priority access to new features. Available on web and mobile (iOS/Android) in a long list of supported countries (~190, spanning most of the Americas, Europe, Africa, Asia-Pacific — full list in source doc).
- **Auto browse in Gemini in Chrome** — Gemini completes multi-step web tasks (compare products, book travel, make reservations). US only, 18+, Chrome 144+, must be signed in.
- **Gemini Spark** — personal automation agent that works across Connected Apps, skills, chats, sites you're signed into, Personal Intelligence, and location to handle goals you set. US only, 18+, requires Keep Activity turned on, English only, mobile app + web only.
- **"Have AI check pricing"** — in Google Search, Gemini contacts local businesses on your behalf to check pricing/availability (salons, car maintenance, phone repair, pet grooming). US, English, signed-in users, web/Android/iOS.

## Creative / generative media

- **Google Flow** — creative studio for video/image storytelling: text-to-video, ingredients-to-video, frames-to-video, text-to-image, image-to-image. Credits purchasable via Google One once dedicated usage is exhausted; same AI-credit pool as Antigravity. English-only prompts and responses. Has safety guardrails on prompts.
- **Google Flow Music** — separate app (flowmusic.app), Google sign-in. Pro tier = Flow Music's Plus plan: 10,000 monthly credits (~2,000 songs), daily top-up credits, 12 concurrent generations, all core features, commercial use rights.
- **Google Photos Generative AI** — Photo to video (animates a still photo into a short cinematic clip, portrait-mode output, daily limits by plan) and Remix (restyles photos into art styles like 3D animation, anime, sketch, comic book, daily limits by plan). Both add a visible AI watermark and an invisible SynthID watermark. Available in select countries, Android/iPhone/iPad, 13+.
- **Google TV Create Hub** — AI video/image generation on Gemini-enabled TCL Google TV devices: text-to-video, image-to-video, video-to-video, text-to-image, image-to-image. US only, 18+; higher limits unlockable via in-device QR code upgrade.

## Other bundled benefits

- **Google Health Premium** — AI coaching (personalized health guidance via Gemini) when paired with a Pixel Watch or Fitbit device through the Google Health app. Not for medical use; results may vary. Shareable with family group. Available in a defined list of ~35 countries including the US, UK, most of the EU, Japan, South Korea, India, Brazil, Mexico, Canada, Australia, New Zealand.
- **Google Home Premium** — Standard plan included free with AI Pro (Advanced plan available as paid add-on) for supported Google Home devices; helps surface important home events. Available in ~20 countries including US, UK, most of the EU, Canada, Japan, Mexico, Australia, NZ.
- **YouTube Premium Lite (individual plan)** — included automatically with certain paid AI Pro memberships, no separate activation. Fewer ads on regular YouTube/YouTube Kids videos, offline/background play for those. Does NOT include YouTube Music Premium, ad-free Shorts, ad-free music-partner content, or extras like Jump Ahead/high-quality audio. Not shareable across family group; unavailable during AI Pro free trials (kicks in once you convert to paid).
- **5–10 TB storage** — exact amount depends on the specific AI Pro plan tier purchased.

## Notes for this environment

- The $10/mo GCP credit and 30 Firebase Studio workspaces (Developer Program premium) are worth checking against project `gws-cli-local-505120` if not already claimed.
- Antigravity's tiered quota system is directly relevant since `agy` is already installed.
- Jules is a candidate tool not currently in the stack — GitHub-integrated coding agent, distinct from `agy`/ADK. Worth a look once git is set up in `~/projects` (open standing gap).
