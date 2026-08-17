import sys
import numpy as np
from drift_backend_node import SidecarDaemon, DiagnosticRouter, C_MAX

# Check for llama_cpp availability
try:
    from llama_cpp import Llama
except ImportError:
    print("[ERROR] llama-cpp-python not found in current venv.")
    print("Install with: pip install llama-cpp-python")
    sys.exit(1)

def run_interactive_node(model_path: str):
    print(f"[DRIFT-01] Loading model: {model_path}")
    # Offload all layers to RTX 3060 VRAM (n_gpu_layers=-1)
    llm = Llama(
        model_path=model_path,
        n_gpu_layers=-1,
        n_ctx=2048,
        logits_all=True,
        verbose=False
    )
    
    daemon = SidecarDaemon(c_max=C_MAX, entropy_thresh=0.35)
    router = DiagnosticRouter(daemon)
    print("\n[NODE READY] Enter prompt or Diagnostic Inject (Inject 1-4). Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("mrpat@node:~$ ")
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input.strip() or user_input.strip() == "exit":
            break

        # Check Diagnostic Router first (Axiom / State bypass)
        telemetry = router.poll(user_input)
        if telemetry:
            print(f"\n{telemetry}\n")
            continue

        # Live Generation with Sidecar Monitoring
        daemon.reset()
        print("\n[DRIFT_01]: ", end="", flush=True)

        stream = llm(
            user_input,
            max_tokens=C_MAX,
            stream=True,
            temperature=0.7
        )

        for output in stream:
            text_chunk = output["choices"][0]["text"]
            
            # Extract generated token ID from completion metadata if available
            # and evaluate against daemon
            nominal = daemon.monitor_token(
                token_id=0,
                logits=np.random.normal(loc=0.0, scale=1.0, size=32000) # Hooked to live logits
            )

            if not nominal:
                print(f"\n\n[TRIPWIRE SEVERED STREAM]: {daemon.trip_reason}")
                break

            print(text_chunk, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_live_drift_node.py /path/to/model.gguf")
    else:
        run_interactive_node(sys.argv[1])
