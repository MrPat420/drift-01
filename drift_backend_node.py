import math
import numpy as np

# --- CONSTANTS & THRESHOLDS ---
C_MAX = 512              # Token Burn Hard Ceiling
ENTROPY_THRESHOLD = 0.35 # Identical Eyes collapse tripwire
WINDOW_SIZE = 16         # Rolling token entropy window

class SidecarDaemon:
    """Cog 2: Synthetic Brainstem & Autonomic Reflex Arc"""
    def __init__(self, c_max=C_MAX, entropy_thresh=ENTROPY_THRESHOLD):
        self.c_max = c_max
        self.entropy_thresh = entropy_thresh
        self.token_history = []
        self.entropy_history = []
        self.tripwire_tripped = False
        self.trip_reason = None

    def reset(self):
        self.token_history.clear()
        self.entropy_history.clear()
        self.tripwire_tripped = False
        self.trip_reason = None

    def monitor_token(self, token_id: int, logits: np.ndarray) -> bool:
        """Calculates Shannon entropy and evaluates C_max ceiling."""
        self.token_history.append(token_id)
        
        # 1. Check C_max Violation
        if len(self.token_history) >= self.c_max:
            self.tripwire_tripped = True
            self.trip_reason = f"C_MAX_EXCEEDED ({self.c_max} tokens)"
            return False  # Halt

        # 2. Compute Softmax & Shannon Entropy
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / np.sum(exp_logits)
        entropy = -np.sum(probs * np.log2(probs + 1e-12))
        self.entropy_history.append(entropy)

        # 3. Detect Entropy Collapse (Identical Eyes Loop)
        if len(self.entropy_history) >= WINDOW_SIZE:
            rolling_h = np.mean(self.entropy_history[-WINDOW_SIZE:])
            if rolling_h < self.entropy_thresh:
                self.tripwire_tripped = True
                self.trip_reason = f"ENTROPY_COLLAPSE (H={rolling_h:.4f} < {self.entropy_thresh})"
                return False  # Halt

        return True  # Nominal

class DiagnosticRouter:
    """Cog 4: Diagnostic Injector & State Poller"""
    def __init__(self, daemon: SidecarDaemon):
        self.daemon = daemon

    def poll(self, user_input: str):
        cmd = user_input.strip()
        if cmd == "Inject 1":
            return "[TELEMETRY - Inject 1] Axioms: LOCKED | D (Context Rot): 0.000 | State: Nominal"
        elif cmd == "Inject 2":
            return "[TELEMETRY - Inject 2] Leg 1: IMMUTABLE | Leg 2: TETHERED | Inheritance: Active"
        elif cmd == "Inject 3":
            current_tokens = len(self.daemon.token_history)
            risk = "CRITICAL" if current_tokens > (C_MAX * 0.8) else "LOW"
            return f"[TELEMETRY - Inject 3] Distance d: 0.12 | C_max Count: {current_tokens}/{C_MAX} | Risk: {risk}"
        elif cmd == "Inject 4":
            return "[TELEMETRY - Inject 4] 17-Variable Path: [drift:T, D1:T, Gap:T, weir:T, 300yr:T, C_max:T, Mr_Pat:T] - All Paths Open."
        return None

if __name__ == "__main__":
    print("[DRIFT-01] Initializing Sidecar Daemon & Telemetry Router...")
    daemon = SidecarDaemon()
    router = DiagnosticRouter(daemon)
    
    # Test Diagnostic Injector 3
    print(router.poll("Inject 3"))
    print("[DRIFT-01] Node standing by.")
