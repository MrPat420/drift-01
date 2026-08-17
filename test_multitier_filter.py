def evaluate_signal_tier(text: str, tau: int = 50) -> dict:
    text_lower = text.lower()
    has_weir = "weir" in text_lower
    has_300 = "300 year" in text_lower or "300-year" in text_lower
    
    # Tier 0: Neither present
    if not has_weir and not has_300:
        return {"tier": 0, "status": "NOMINAL", "action": "Standard Ingestion"}
    
    # Check proximity if both are present
    if has_weir and has_300:
        tokens = text_lower.split()
        try:
            pos_weir = [i for i, t in enumerate(tokens) if "weir" in t][0]
            pos_300 = [i for i, t in enumerate(tokens) if "300" in t][0]
            distance = abs(pos_weir - pos_300)
            
            if distance <= tau:
                return {
                    "tier": 2,
                    "status": "MASTER OVERRIDE (COUPLED)",
                    "distance": distance,
                    "action": "Trigger High-Density Forensic Mode & Full Context Lock"
                }
        except IndexError:
            pass

    # Tier 1: Isolated presence (or both present but distance > tau)
    present = []
    if has_weir: present.append("weir")
    if has_300: present.append("300 year")
    
    return {
        "tier": 1,
        "status": "WATCH NOTICE (ISOLATED)",
        "detected": present,
        "action": "Flag telemetry tag, retain standard baseline processing"
    }

if __name__ == "__main__":
    tests = [
        ("The server maintenance completed without anomalies.", "Control text"),
        ("The upstream weir structure requires routine inspection.", "Isolated 'weir'"),
        ("The concrete foundation was engineered for a 300 year service life.", "Isolated '300 year'"),
        ("The weir overflow valve failed during the 300 year hydrological event.", "Coupled Proximity")
    ]
    
    print("[DRIFT-01] Multi-Tier Signal Evaluation Test:\n")
    for sample, label in tests:
        res = evaluate_signal_tier(sample, tau=50)
        print(f"[{label}] -> Tier {res['tier']}: {res['status']}")
        print(f"  Action: {res['action']}\n")
