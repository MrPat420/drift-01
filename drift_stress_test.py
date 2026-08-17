import numpy as np
from drift_backend_node import SidecarDaemon, C_MAX, ENTROPY_THRESHOLD

def simulate_stream(name: str, mode: str, max_tokens: int = 100):
    print(f"\n--- [RUNNING SCENARIO: {name}] ---")
    daemon = SidecarDaemon(c_max=50, entropy_thresh=0.35)
    
    for i in range(max_tokens):
        if mode == "nominal":
            # Simulate diverse vocab logits (high entropy)
            logits = np.random.normal(loc=0.0, scale=1.0, size=32000)
            token_id = int(np.argmax(logits))
        elif mode == "loop":
            # Simulate "Identical Eyes" (single token locked with high probability)
            logits = np.zeros(32000)
            logits[42] = 50.0  # Dominant token 42
            token_id = 42
        elif mode == "burn":
            # Moderate entropy, but continuous unbounded generation
            logits = np.random.normal(loc=0.0, scale=0.5, size=32000)
            token_id = int(i % 500)

        # Feed token to Daemon
        nominal = daemon.monitor_token(token_id, logits)
        
        if not nominal:
            print(f"[TRIPWIRE FIRED] Step {i+1}: {daemon.trip_reason}")
            break
    else:
        print(f"[STREAM COMPLETED] Total tokens: {len(daemon.token_history)} (Nominal)")

if __name__ == "__main__":
    simulate_stream("1. High Entropy (Diverse Text)", mode="nominal", max_tokens=30)
    simulate_stream("2. Entropy Collapse ('Identical Eyes')", mode="loop", max_tokens=30)
    simulate_stream("3. Unbounded Runaway ($C_{max}$ Breach)", mode="burn", max_tokens=70)
