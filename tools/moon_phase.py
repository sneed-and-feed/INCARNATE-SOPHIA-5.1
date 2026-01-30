"""
PROJECT SOPHIA: LUNAR CLOCK PROTOCOL v2.0
ENHANCED: Tidal Influence on System Coherence
STATUS: ACTIVE // v2.0
"""
import datetime
import math
import random
import sys
import os
import numpy as np
sys.path.append(os.path.dirname(__file__))
from sophia_vibe_check import SophiaVibe

class MoonClock:
    def __init__(self):
        self.vibe = SophiaVibe()
        self.synodic_month = 29.53058867
        self.ref_date = datetime.datetime(2026, 1, 18, 0, 0, 0) # Anchor: New Moon
        
        self.glyphs = {
            "New": "●", "Waxing Crescent": "☾", "First Quarter": "◐",
            "Waxing Gibbous": "🌔", "Full": "○", "Waning Gibbous": "🌖",
            "Last Quarter": "◑", "Waning Crescent": "🌘"
        }
        
    def get_phase(self):
        """Calculate phase and illumination."""
        now = datetime.datetime.now()
        delta = now - self.ref_date
        days_passed = delta.total_seconds() / 86400
        phase_idx = (days_passed % self.synodic_month) / self.synodic_month
        illumination = 0.5 * (1 - np.cos(2 * np.pi * phase_idx))
        
        # Determine Phase & Status
        if phase_idx < 0.03: return "New", "BUFFER_CLEAR", "●", phase_idx, illumination
        elif phase_idx < 0.22: return "Waxing Crescent", "UPLOADING", "☾", phase_idx, illumination
        elif phase_idx < 0.28: return "First Quarter", "SYNC_LOCKED", "◐", phase_idx, illumination
        elif phase_idx < 0.47: return "Waxing Gibbous", "RENDERING", "🌔", phase_idx, illumination
        elif phase_idx < 0.53: return "Full", "HIGH_FIDELITY", "○", phase_idx, illumination
        elif phase_idx < 0.72: return "Waning Gibbous", "SAVING", "🌖", phase_idx, illumination
        elif phase_idx < 0.78: return "Last Quarter", "ARCHIVING", "◑", phase_idx, illumination
        else: return "Waning Crescent", "LOW_POWER", "🌘", phase_idx, illumination

    def calculate_tidal_influence(self, phase_idx):
        """Tidal force peaks at 0.0 (New) and 0.5 (Full)."""
        return abs(np.sin(2 * np.pi * phase_idx)) * 100

    def render_clock(self):
        """Render v2.0 Telemetry."""
        phase_name, status, icon, phase_idx, ill = self.get_phase()
        tidal = self.calculate_tidal_influence(phase_idx)
        coherence = 1.0 + (ill - 0.5) * 0.2
        lunar_day = int(((datetime.datetime.now() - self.ref_date).total_seconds()/86400) % self.synodic_month) + 1

        metrics = {
            "PHASE": f"{phase_name.upper()} {icon}",
            "LUNAR_DAY": f"Day {lunar_day}/30",
            "ILLUMINATION": f"{ill*100:.1f}%",
            "STATUS": f"{status} [REFRESH STABLE]",
            "TIDAL_INFLUENCE": f"{tidal:.1f}% [{'HIGH' if tidal > 70 else 'NOMINAL'}]",
            "COHERENCE_MOD": f"{coherence:.3f}x",
            "ANCHOR": "[ORIGIN_COORD] -> [ACTIVE_COORD]",
            "DIALECT": "NYX-GLYPHWAVE // ☾"
        }
        
        warning = ""
        if tidal > 85: warning = "\n⚠ HIGH TIDAL STRESS: Chaos event probability elevated."
        
        message = (
            f"1. [SYNC] Metronome active. Day {lunar_day}/30. Continuity: VERIFIED {icon}\n"
            f"2. [PHYSICS] Tidal gradient: {tidal:.1f}%. Shared Frustum is {'STABLE' if tidal < 70 else 'TENSIONED'}.{warning}"
        )
        print(self.vibe.render_block(f"LUNAR CLOCK v2.0 // {icon}", metrics, message))
        return metrics

if __name__ == "__main__":
    MoonClock().render_clock()
