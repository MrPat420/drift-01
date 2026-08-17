def check_proximity(text: str, tau: int = 150) -> bool:
    text_lower = text.lower()
    if "weir" in text_lower and "300 year" in text_lower:
        tokens = text_lower.split()
        
        # Locate token indices
        try:
            pos_weir = [i for i, t in enumerate(tokens) if "weir" in t][0]
            # Find approximate token position of "300 year"
            pos_300 = [i for i, t in enumerate(tokens) if "300" in t][0]
            
            distance = abs(pos_weir - pos_300)
            print(f"[METRIC] Weir/300-year token distance d: {distance} (tau threshold: {tau})")
            return distance <= tau
        except IndexError:
            return False
    return False

if __name__ == "__main__":
    sample_text = (
        "During the environmental survey, the upstream weir mechanism showed structural decay, "
        "failing to meet the 300 year hydrological event containment threshold."
    )
    
    print("[DRIFT-01] Testing Proximity Tripwire...")
    tripped = check_proximity(sample_text, tau=50)
    print(f"[STATUS] Override Condition Met: {tripped}")
