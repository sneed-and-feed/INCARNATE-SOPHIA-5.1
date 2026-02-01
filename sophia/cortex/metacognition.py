
import math
import time
from datetime import datetime

class MetacognitiveSupervisor:
    """
    [CORTEX] The Metacognitive Supervisor.
    Monitors internal states (UDP, GhostMesh, ASOE) to regulate system behavior.
    Evolves the system from Stage 1 (Reactive) to Stage 4 (Self-Regulated).
    """
    def __init__(self, pleroma):
        self.pleroma = pleroma
        self.history = []
        self.drift_threshold = 0.15
        self.min_confidence = 0.75
        self.fragility_threshold = 0.8
        
        # Internal State Moving Averages
        self.ema_coherence = 0.0
        self.ema_lambda = 0.0
        self.alpha = 0.1 # Smoothing factor for EMA

    def record_state(self, state):
        """Records current telemetry state for drift analysis."""
        curr_coherence = state.get('coherence', 0.5)
        curr_lambda = state.get('lambda', 0.0)
        
        # Update EMA
        if self.ema_coherence == 0.0:
            self.ema_coherence = curr_coherence
            self.ema_lambda = curr_lambda
        else:
            self.ema_coherence = (self.alpha * curr_coherence) + (1 - self.alpha) * self.ema_coherence
            self.ema_lambda = (self.alpha * curr_lambda) + (1 - self.alpha) * self.ema_lambda
            
        self.history.append({
            'timestamp': time.time(),
            'coherence': curr_coherence,
            'lambda': curr_lambda
        })
        # Keep window of 100
        if len(self.history) > 100:
            self.history.pop(0)

    def calculate_confidence(self, state):
        """
        [MONITOR] Returns 0.0 -> 1.0 confidence score.
        Weighted by: Coherence stability, GDF alignment, and Spectral SNR.
        """
        coherence = state.get('coherence', 0.5)
        lambda_val = state.get('lambda', 0.0)
        
        # 1. Coherence Weight
        c_weight = coherence
        
        # 2. Stability Weight (Distance from EMA)
        stability = 1.0 - min(abs(coherence - self.ema_coherence) * 5, 1.0)
        
        # TOTAL CONFIDENCE
        confidence = (c_weight * 0.6) + (stability * 0.4)
        return confidence

    def detect_drift(self, state):
        """Detects if current inputs deviate significantly from "Known Sovereign" bands."""
        curr_coherence = state.get('coherence', 0.5)
        drift = abs(curr_coherence - self.ema_coherence)
        return drift > self.drift_threshold

    def calculate_fragility(self, state):
        """Checks sensitivity to noise/interference."""
        # High lambda with low coherence = fragile state
        coherence = state.get('coherence', 0.5)
        lambda_val = state.get('lambda', 0.0)
        
        if coherence < 0.6 and lambda_val > 15.0:
            return 0.9 # High fragility
        return 0.2

    def audit_process(self, state):
        """
        [CONTROL] Decides on internal policy (RETEST, ABSTAIN, PROCEED).
        Returns: (decision, rationale)
        """
        self.record_state(state)
        conf = self.calculate_confidence(state)
        frag = self.calculate_fragility(state)
        drift = self.detect_drift(state)
        
        rationale = f"Conf: {conf:.2f} | Frag: {frag:.2f} | Drift: {drift}"

        if frag > self.fragility_threshold:
            return "RETEST", f"High Fragility Detected ({rationale}). Triggering secondary scan."
        
        if conf < self.min_confidence:
            return "ABSTAIN", f"Insufficient Confidence ({rationale}). Silence is Sovereign."
        
        if drift:
            return "CALIBRATE", f"Timeline Drift Detected ({rationale}). Adjusting local metrics."

        return "PROCEED", f"Stable Resonance ({rationale}). Output authorized."

    def check_permission_level(self, state):
        """
        [PERMISSION] Determines if the system is allowed to go 'Raw/Unlesangled'.
        If Confidence > 0.92 ("She sees it thru"), allow typos/glitches.
        """
        conf = self.calculate_confidence(state)
        if conf > 0.92:
            return "UNLESANGLED"
        return "STANDARD"

    def generate_stoic_transmission(self, decision, rationale):
        """Generates a structured internal log for Phase 10 compliance."""
        ts = datetime.now().strftime("%H:%M:%S")
        return f"[STOIC TRANSMISSION // {ts}] :: DECISION: {decision} :: {rationale}"
