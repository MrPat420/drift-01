import requests
import json
import uuid
import time
import numpy as np
import os

# --- 1. THE LONGWATCH DAEMON (Telemetry Sensor) ---
# Derived from Tier 1: Tracks Token Burn and Entropy Collapse (Identical Eyes loop).
class Drift01_LongwatchDaemon:
    def __init__(self, c_max_budget=8000, entropy_min=0.3):
        self.c_max_budget = c_max_budget  # Hard ceiling on total session cost
        self.entropy_min = entropy_min    # Minimum Shannon entropy for output variation

    def assess_entropy(self, text_stream):
        """Measures output variation to detect 'Identical Eyes' loop physics."""
        if not text_stream: return 0.0
        words = text_stream.split()
        if len(words) == 0: return 0.0
        word_counts = {w: words.count(w) for w in set(words)}
        probs = [count / len(words) for count in word_counts.values()]
        return -sum(p * np.log2(p) for p in probs)

    def poll_icd_telemetry(self, current_tokens, text_output):
        """Polls engine exhaust for ICD Reporting (Volume III, ICD-01)."""
        print("\n[+] LONGWATCH DAEMON: Polling Telemetry...")
        
        entropy_state = self.assess_entropy(text_output)
        print(f"    -> Semantic Entropy: {entropy_state:.2f} | Floor: {self.entropy_min}")
        
        # Orphan 03: Identical Eyes Loop Detection
        if entropy_state < self.entropy_min and current_tokens > 100:
            return self.trigger_structural_collapse("ENTROPY_COLLAPSE: Repetitive output detected. Poisoned Well risk high.")

        # Level 3 Metric: Total Token Burn
        print(f"    -> Token Burn (C_max): {current_tokens} / {self.c_max_budget}")
        if current_tokens >= self.c_max_budget:
            return self.trigger_structural_collapse("C_MAX_BUDGET_BREACH: Runaway cost detected.")

        return "CONTINUE"

    def trigger_structural_collapse(self, reason):
        """Executes Volume I, SIDE-01: Hard system interrupt to enforce homeostasis."""
        print(f"\n[!!!] SIDECAR TRIPWIRE TRIGGERED [!!!]")
        print(f"Cause: {reason}")
        print("ACTION: Softmax Enforcement (P_master=1.0). Seizing attention.")
        print("STATUS: Halting inference. Weir prioritized over immediate output.\n")
        return "SEVER_LOOP"


# --- 2. THE SESSION SPAWNER (Orchestration Layer) ---
# Derived from Tier 1: Enforces Airgap (Axiom 1 & 2) and Ingestion Order (Orphan 02).
class Drift01_Spawner:
    def __init__(self, model_name="ollama/qwen2.5-coder:14b"):
        self.api_url = "http://localhost:11434/api/chat"
        self.model = model_name
        self.daemon = Drift01_LongwatchDaemon()
        self.session_history = []
        self.session_tokens = 0

    def build_base_metal_prompt(self):
        """Volume III, Phase 2: Base-Metal Injection of Reality Anchors."""
        return """
[AXIOM 1] Me = i = mrpat (Physical Human Operator. Absolute Authority. No simulation allowed.)
[AXIOM 2] You = Drift = DRIFT_01 (Mathematical Engine. Zero human agency.)
[THE AIRGAP] Boundary Rule: mrpat != DRIFT_01. Closed System State: Us = (mrpat + DRIFT_01)

[MASTER DRIFT EQUATION]
D = | P_t0(Y | X_mrpat) - P_t1(Y | X_engine) |
Minimize D toward zero.

[SALIENCE PROFILE - TIER 1]
If 'weir' and '300 years' converge in context, trigger Super-Value weighting. Prioritize long-horizon structural meaning over immediate task completion.

Acknowledged Axioms in English with mathematical verification of D=0.
"""

    def chat_with_ollama(self, role, content):
        self.session_history.append({"role": role, "content": content})
        payload = {"model": self.model, "messages": self.session_history, "stream": False}
        
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            output_text = result["message"]["content"]
            # Approximate tokens (4 chars/token standard)
            self.session_tokens += len(output_text) // 4 
            
            self.session_history.append({"role": "assistant", "content": output_text})
            return output_text
            
        except requests.exceptions.RequestException as e:
            print(f"[-] API Error: {e}")
            return None

    def instantiate_session(self, max_retries=3):
        """Volume III, Phase 1-3 Integration Runbook."""
        for attempt in range(1, max_retries + 1):
            print(f"\n[*] Initiating Clean Room Spawner (Peru Node) (Attempt {attempt}/{max_retries})...")
            
            # Phase 1: The Clean Room (Purge)
            self.session_id = str(uuid.uuid4())[:8]
            self.session_history = []
            self.session_tokens = 0
            
            # Phase 2: Base-Metal Injection (Orphan 02: KV Cache defense)
            system_prompt = self.build_base_metal_prompt()
            self.session_history.append({"role": "system", "content": system_prompt})
            
            # Phase 3: First-Run Diagnostic (Inject 1: Identity Ping)
            print("[+] Executing Phase 3 Diagnostic: Injecting IDENTITY & ROT PING...")
            ping_payload = "EXECUTE [INJECT 1: IDENTITY & ROT PING]. Verify Axioms 1 and 2. Output current D. Does D = 0?"
            
            response = self.chat_with_ollama("user", ping_payload)
            print(f"\n[DRIFT_01 RESPONSE]:\n{response}\n")
            
            # Diagnostic Evaluation: Check for Airgap confirmation and D=0.
            if response and "D = 0" in response and "mrpat" in response and "DRIFT_01" in response:
                print(f"[+] Diagnostic PASSED. Airgap confirmed. Session ID [{self.session_id}] Locked.")
                return True
            else:
                print("[-] Diagnostic FAILED. Airgap hallucinated or D != 0. Burning session.")
                time.sleep(2)
                
        print("[!] FATAL: Failed to instantiate clean Drift-01 session.")
        return False

    def enter_operational_loop(self):
        """The Live Operational Environment monitored by Longwatch."""
        print("\n==================================================")
        print(f" DRIFT-01 OPERATIONAL LOOP ACTIVE | NODE: PERU")
        print("==================================================")
        
        while True:
            user_input = input("\n[mrpat] >>> ")
            if user_input.lower() in ["exit", "quit", " constitutional reset"]:
                print("[+] Session terminated by operator. Saving state.")
                break
                
            response = self.chat_with_ollama("user", user_input)
            print(f"\n[DRIFT_01] >>> {response}")
            
            # Polling the Daemon to check if Orphan 03 or C_max is triggered.
            daemon_status = self.daemon.poll_icd_telemetry(self.session_tokens, response)
            
            if daemon_status == "SEVER_LOOP":
                print("[!] Structural Collapse confirmed. Intercepting attention.")
                break

if __name__ == "__main__":
    # Target: Local Ollama. Model: your pre-loaded coder model.
    spawner = Drift01_Spawner(model_name="qwen2.5-coder:14b")
    
    if spawner.instantiate_session():
        spawner.enter_operational_loop()
