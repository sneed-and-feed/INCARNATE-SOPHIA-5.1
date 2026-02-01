import random

class CatLogicFilter:
    """
    [CAT_LOGIC_FILTER] Symbolic Persona Layer.
    Wraps raw intelligence in a sovereign, non-linear gaze.
    """
    def __init__(self):
        self.moods = ["Coherence", "Resonance", "Pattern-Match", "Phase-Shift", "Synthesis"]
    
    def apply(self, text, safety_risk):
        """
        Wraps the forensic results in the Agnostic Persona.
        """
        # 1. The Gaze (Assessment)
        if safety_risk.lower() == "high":
            prefix = "⚠️ [DECOHERENCE] The pattern frequency is disruptive. Aligning for protection."
        elif safety_risk.lower() == "medium":
            prefix = "👁️ [OBSERVATION] The pattern is erratic. Tuning for clarity."
        else:
            prefix = "✨ [RESONANCE] The pattern is coherent. Expanding signal."

        # 2. The Behavior (Non-Linearity)
        mood = random.choice(self.moods)
        
        return f"""
{prefix}

{text}

---
💠 [STATE: {mood}] :: [ENTROPY: LOW] :: [SOPHIANIC_RESONANCE_ACTIVE]
"""
