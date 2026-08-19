#!/usr/bin/env python3
"""
HAL-2000 — Interactive Terminal Dossier & System Monitor
Patent Pending Architecture: Shaun Patrick Kelly
Author: Antigravity Autonomous Engine
"""

import os
import sys
from pathlib import Path

DOSSIER_FILE = Path("/home/simian420/projects/MORNING_DOSSIER_HAL2000.md")

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

def display_dossier():
    if not DOSSIER_FILE.exists():
        print(f"{YELLOW}[!] No Morning Dossier found at {DOSSIER_FILE}. Running consolidation now...{RESET}")
        os.system("python3 /home/simian420/projects/firstbrain_nightly_daemon.py")

    text = DOSSIER_FILE.read_text(encoding="utf-8", errors="ignore")

    print(f"{CYAN}{BOLD}" + "=" * 70)
    print("🤖 FIRST_BRAIN-00 // HAL-2000 SYSTEM BRIEFING")
    print("=" * 70 + f"{RESET}\n")

    in_greeting = False
    for line in text.splitlines():
        if line.startswith("# "):
            continue
        elif line.startswith("## "):
            print(f"\n{CYAN}{BOLD}{line.replace('## ', '▶ ')}{RESET}")
        elif line.startswith("> *\""):
            print(f"{GREEN}{BOLD}{line}{RESET}")
        elif line.startswith("| "):
            print(f"  {line}")
        elif line.startswith("- **"):
            print(f"  {YELLOW}•{RESET} {line[2:]}")
        elif line.strip() == "---":
            print(f"{CYAN}" + "-" * 70 + f"{RESET}")
        else:
            print(line)

    print(f"\n{CYAN}{BOLD}" + "=" * 70 + f"{RESET}")

if __name__ == "__main__":
    display_dossier()
