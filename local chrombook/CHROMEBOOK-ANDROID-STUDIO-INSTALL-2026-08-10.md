---
title: "Chromebook Android Studio Install — 2026-08-10 (Quail 3)"
kb_type: wiki
topic: infrastructure
environment: ChromeOS Crostini (Debian container / penguin)
captured: 2026-08-10
status: installed-first-run-pending
updates: CHROMEBOOK-GCP-ENV-HANDOFF.md §"Pending stack" — Android Studio (Quail) now installed
tags: [chromebook, crostini, android-studio, quail, ide, install-snapshot]
---

# Chromebook Android Studio Install — 2026-08-10

Android Studio Quail 3 installed on the Crostini container. Closes the "Android Studio (Quail)" item in the master handoff's pending stack; first-run configuration still open.

## Environment

- **OS:** ChromeOS Linux container (Debian Crostini / `penguin`)
- **Available space:** ~7.4 GB (disk optimized after removing heavy Flatpak runtimes)

## Install

- **Application:** Android Studio Quail 3
- **Path:** `/opt/android-studio/`
- **Method:** direct tarball stream extraction — `curl` piped into `sudo tar -xz -C /opt/` to avoid temporary archive storage

## Launch

- **Standard:** `/opt/android-studio/bin/studio.sh`
- **ChromeOS graphics fix (if splash screen freezes):**

```bash
_JAVA_OPTIONS="-Dsun.java2d.opengl=false -Dsun.java2d.xrender=false" /opt/android-studio/bin/studio.sh
```

## Purpose

Official IDE for Android application development — Kotlin/Java, Android SDK management, Gradle build automation, layout design.

## Current state / next steps

- Installed in `/opt/`; initial Setup Wizard launched
- ☐ Complete first-run configuration wizard
- ☐ Add launcher icon: Tools → Create Desktop Entry
