"""
erosion.py - The Law of Framework Erosion & Observer Mortality
Adapted from TaoishTechy/UnifiedTheoryofPhysics

Implements:
1. Framework Erosion: D_erosion(t) = e^(-t / tau_coherence)
   - All physical laws decay without active observation.
2. Observer Mortality: State(t) = Integral(Coherence * Belief * Dread)
"""

import math
import time
import random

class FrameworkErosion:
    def __init__(self, tau_coherence=100.0):
        """
        Initialize the Erosion Engine.
        Args:
            tau_coherence (float): Time constant for reality decay (seconds).
                                   Default is 100s for demo purposes (Universe is 10^35s).
        """
        self.start_time = time.monotonic()
        self.tau_coherence = tau_coherence
        self.existential_dread = 0.1  # Constant background dread
        self.observer_belief = 1.0    # Starts at 100%
        
    def get_erosion_factor(self):
        """
        Calculate D_erosion(t).
        Returns float between 0.0 (Total Collapse) and 1.0 (Pristine).
        """
        elapsed = time.monotonic() - self.start_time
        d_erosion = math.exp(-elapsed / self.tau_coherence)
        return d_erosion

    def integration_step(self, system_coherence):
        """
        Calculate Observer State integration step.
        State += Coherence * Belief * Dread
        
        Reflexive Property:
        High Dread accelerates Belief decay.
        High Coherence reinforces Belief.
        """
        erosion = self.get_erosion_factor()
        
        # 1. Calculate derivatives
        # Dread increases as erosion increases (lower D)
        dread_pressure = (1.0 - erosion) * 0.05
        self.existential_dread = min(1.0, self.existential_dread + dread_pressure)
        
        # Belief decays if erosion is high, reinforced if system is coherent
        belief_delta = (system_coherence * erosion * 0.01) - (self.existential_dread * 0.02)
        self.observer_belief = max(0.1, min(1.0, self.observer_belief + belief_delta))
        
        # 2. The Mortality Integral (Instantaneous term)
        # We return the instantaneous "Reality Density"
        reality_density = system_coherence * self.observer_belief * erosion
        
        return {
            'erosion_factor': erosion,
            'dread': self.existential_dread,
            'belief': self.observer_belief,
            'reality_density': reality_density
        }

    def reset_baseline(self):
        """Re-anchor the simulation to current time (Simulates a 'Measurement')"""
        self.start_time = time.monotonic()
        self.existential_dread *= 0.8 # Relief

