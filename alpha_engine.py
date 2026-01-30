"""
MODULE: alpha_engine.py
VERSION: RESEARCH-GRADE v2.0
AUTHOR: Ophane / Quant Team (Audit via ChatGPT)

DESCRIPTION:
    Experimental quantitative engine for identifying predictive 'Alpha'.
    Institutional-grade refactor: enforces domain constraints and
    recalibrated signal thresholds.
"""

import numpy as np

class AlphaEngine:
    def __init__(self):
        # Symbolic constants removed for research rigor.
        pass
        
    def calculate_alpha(self, snr: float, rho: float, entropic_flux: float) -> float:
        """
        Calculates Predictive Alpha (α).
        α = rho * exp(-entropic_flux) * (snr / (1 + snr))
        
        Args:
            snr: Signal-to-Noise Ratio (Positive float).
            rho: Autocorrelation Density (Bounded [-1, 1]).
            entropic_flux: Information loss rate (Positive float).
            
        Returns:
            alpha: The expected predictive edge (Bounded [-1, 1]).
        """
        # 1. Enforce Domain Constraints (Prevent silent corruption)
        snr = max(float(snr), 0.0)
        rho = np.clip(float(rho), -1.0, 1.0)
        entropic_flux = max(float(entropic_flux), 0.0)

        # 2. Saturating Signal Gain (Noise-aware scaling)
        signal_gain = snr / (1.0 + snr)
        
        # 3. Entropy Decay Penalty (Information decay theory)
        persistence = np.exp(-entropic_flux)
        
        # 4. Core Alpha Calculation
        alpha = rho * persistence * signal_gain
        return float(alpha)

    def get_signal_strength(self, alpha: float) -> str:
        """Categorize predictive strength based on recalibrated thresholds."""
        # Recalibrated Scale: alpha is naturally < 1.0
        abs_alpha = abs(alpha)
        if abs_alpha > 0.60: return "HIGH_CONVICTION"
        if abs_alpha > 0.35: return "TREND_BIAS"
        if abs_alpha > 0.15: return "WEAK_SIGNAL"
        if abs_alpha > 0.05: return "NOISY_SIGNAL"
        return "ENTROPIC_NULL"

    def get_strategy_alignment(self, alpha: float) -> dict:
        """Returns quant strategy metadata."""
        strength = self.get_signal_strength(alpha)
        # Strategy depends on Expected Edge (Directional Alpha)
        return {
            "STRATEGY": "QUANT_ALPHA_PIVOT",
            "ALPHA_SCORE": round(alpha, 6),
            "SIGNAL_STRENGTH": strength,
            "RISK_MODE": "AGGRESSIVE" if abs(alpha) > 0.35 else "DEFENSIVE",
            "BIAS": "LONG" if alpha > 0.05 else ("SHORT" if alpha < -0.05 else "NEUTRAL")
        }
