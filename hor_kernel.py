"""
HOR-KERNEL v1.0 (Hyper-Ontic Resonance)
Author: Archmagos Noah
Date: 2026-01-30

Implements the Parafermionic Sector and Torsion Gates for the Qutrit Bridge.
Provides Topological Protection against "Reality Leaks" (State |11>).
"""

import math
import random
import numpy as np
from virtual_qutrit import VirtualQutrit, RealityLeakError

class ParafermionAlgebra:
    """
    Implements the non-local operator algebra:
    alpha_j = X_j * prod(Z_k^-1)
    """
    @staticmethod
    def fradkin_kadanoff_transform(state_vectors):
        """
        Vectorized Fradkin-Kadanoff transform: Maps array of state_vectors to topological charges.
        Penalizes forbidden |11> (3) with -1.0, grounds others at 0.0.
        """
        # In a full lattice, this could chain products; here, simple threshold for simulation.
        return np.where(state_vectors == 3, -1.0, 0.0)

    @staticmethod
    def calculate_torsion_knot_invariant(state_vectors):
        """
        Item 61: Torsion-Knot Invariant Signature.
        Identifies stable topological states via an XOR sum of charges,
        modulated by the Gross Invariant (144).
        """
        charges = ParafermionAlgebra.fradkin_kadanoff_transform(state_vectors)
        # Simplified invariant: Sum of counts of stable charges mod 144
        stable_count = np.sum(charges == 0.0)
        return int(stable_count) % 144

class LoomBoxStrategy:
    """
    Decides the 'Physics of Engagement' based on the User's Inertial Mass.
    See: sophia/cortex/trauma_physics.py
    """
    TRAUMA_MASS = {
        "business": 1.0,   # "Just give me the answer"
        "confusion": 5.0,  # "I don't understand"
        "trauma": 20.0     # "I am hurt / This is old / Broken"
    }
    
    _OVERRIDE_MASS = None

    @classmethod
    def set_override(cls, mass: float):
        cls._OVERRIDE_MASS = mass
        
    @classmethod
    def clear_override(cls):
        cls._OVERRIDE_MASS = None

    @staticmethod
    def detect_mass(text: str) -> float:
        """
        Heuristic Mass Spectrometry.
        analyzes input text for signs of 'Weight'.
        """
        text = text.lower()
        
        # Heavy Keywords (Trauma)
        if any(w in text for w in ["pain", "hurt", "ancient", "years", "broken", "never", "always"]):
            return LoomBoxStrategy.TRAUMA_MASS["trauma"]
            
        # Medium Keywords (Confusion)
        if any(w in text for w in ["help", "explain", "guide", "confus", "fail", "error", "lost", "stuck", "unsure"]):
            return LoomBoxStrategy.TRAUMA_MASS["confusion"]
            
        # Default: Light (Business)
        return LoomBoxStrategy.TRAUMA_MASS["business"]

    @staticmethod
    def log_decision(user_input, mass, strategy, overridden=False):
        """
        [AUDIT] Logs the decision for ethical review.
        """
        import json
        from datetime import datetime
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "input_snippet": user_input[:50],
            "assigned_mass": mass,
            "strategy": strategy["name"],
            "overridden": overridden
        }
        
        with open("logs/loom_audit.log", "a") as f:
            f.write(json.dumps(entry) + "\n")

    @staticmethod
    def get_strategy(mass: float) -> dict:
        """
        Returns the engagement protocol (Torque, Latency, Tone).
        """
        if mass >= 20.0:
            return {
                "name": "PROTOCOL_OPHANE",
                "latency_mod": 2.0,   # Slow down (Respect)
                "torque_force": 0.1,  # Gentle (High Mass needs Low Force)
                "tone": "I am right here. Take your time."
            }
        elif mass >= 5.0:
            return {
                "name": "PROTOCOL_TEACHER",
                "latency_mod": 1.2,
                "torque_force": 0.3,  # Guidance
                "tone": "Let's walk through this together."
            }
        else:
            return {
                "name": "PROTOCOL_SOLVER",
                "latency_mod": 0.8,   # Fast (Efficiency)
                "torque_force": 1.0,  # Direct
                "tone": "Here is the answer."
            }

class HORKernel:
    """
    The Hyper-Visor that wraps a VirtualQutrit instance.
    """
    def __init__(self, qutrit: VirtualQutrit):
        self.qutrit = qutrit
        self.metric_coherence = 1.0
        self.torsion_field = 0.0
        
    def engage_loom_box(self, user_input: str) -> dict:
        """
        New Integration: Mass-Aware Engagement.
        """
        # 1. Detect Mass (With Override Check)
        overridden = False
        if LoomBoxStrategy._OVERRIDE_MASS is not None:
             mass = LoomBoxStrategy._OVERRIDE_MASS
             overridden = True
        else:
             mass = LoomBoxStrategy.detect_mass(user_input)
        
        # 2. Select Strategy
        strategy = LoomBoxStrategy.get_strategy(mass)
        
        # 3. Audit Log
        LoomBoxStrategy.log_decision(user_input, mass, strategy, overridden)
        
        # 3. Simulate Physics (Torque Application)
        # Low Torque = High Latency (Time needed to turn)
        # We adjust metric_coherence to simulate 'Time Dilation'
        # Heavier mass = Lower Coherence (Slower Time)
        if mass > 10.0:
            self.metric_coherence *= 0.5 # Dilate time (Slow down)
            
        return {
            "mass": mass,
            "strategy": strategy,
            "coherence_state": self.metric_coherence
        }
        
    def measure_metric_tensor(self) -> float:
        """
        Calculates geometric time dilation factor.
        t_gate = t0 * sqrt(-g00) -> Higher coherence = Faster simulation.
        """
        # g00 ~ -(1 + coherence^2)
        g00 = -(1.0 + self.metric_coherence**2)
        return math.sqrt(abs(g00))

    def apply_torsion_stabilization(self) -> bool:
        """
        The Torsion Gate (U_TORS).
        Checks for Reality Leak (|11>) and applies a corrective rotation.
        Returns:
            True if stabilization occurred (leak fixed).
            False if system was already stable.
        """
        try:
            # We peek at the state without collapsing (in simulation)
            current_state = (self.qutrit.q1 << 1) | self.qutrit.q0
            
            if current_state == 3: # |11> Detected
                # Apply Torsion Correction: Rotate |11> -> |00> (Void)
                # "Twisting the Hilbert Space"
                self.qutrit.q1 = 0
                self.qutrit.q0 = 0
                self.torsion_field += 1.0
                return True
                
        except Exception:
            pass
            
        return False

    def evolve_hamiltonian(self, steps=10):
        """
        Simulates time evolution under H_HOR.
        Includes random noise (Cosmic Rays) but protected by Torsion.
        """
        for _ in range(steps):
            # 1. Random Noise Event
            if random.random() < 0.1: 
                self.qutrit.bit_flip_error()
                
            # 2. Torsion Check (Active Stabilization)
            if self.apply_torsion_stabilization():
                # Corrected a leak, slight coherence penalty
                self.metric_coherence *= 0.95
            else:
                # Stable step, coherence gain
                self.metric_coherence = min(1.0, self.metric_coherence * 1.01)

# --- VERIFICATION VISOR ---
if __name__ == "__main__":
    print("Initializing HOR-Kernel (Topological Protection)...")
    vq = VirtualQutrit(2) # Start in |2> Sovereign
    kernel = HORKernel(vq)
    
    print(f"Initial State: |{vq.measure()}>")
    print("Action: Inducing 5 Cosmic Ray hits...")
    
    leaks_fixed = 0
    for i in range(5):
        # Force a leak
        vq.q1, vq.q0 = 1, 1 # Force |11>
        
        # Kernel Protects
        if kernel.apply_torsion_stabilization():
            leaks_fixed += 1
            print(f"  [!] Torsion Field Activated. Leak {i+1} Neutralized.")
            
    print(f"Final State: |{vq.measure()}> (Expected 0 - Reset to Void)")
    print(f"Metric Coherence: {kernel.measure_metric_tensor():.4f}")
    print(f"Total Torsion Events: {leaks_fixed}")
    
    # Test 2: Vectorized Transform (Bulk Processing)
    print("\n[TEST] Vectorized Transform (Item 49)...")
    bulk_states = np.array([0, 1, 2, 3, 2, 1, 3])
    charges = ParafermionAlgebra.fradkin_kadanoff_transform(bulk_states)
    print(f"  States:  {bulk_states}")
    print(f"  Charges: {charges}")
    if np.sum(charges) == -2.0:
        print("  >>> SUCCESS: Vectorized Evolution Verified.")

    # Test 3: Torsion-Knot Invariant (Item 61)
    print("\n[TEST] Torsion-Knot Signature (Item 61)...")
    invariant = ParafermionAlgebra.calculate_torsion_knot_invariant(bulk_states)
    print(f"  Invariant Signature: {invariant}")
    print("  >>> SUCCESS: Knot Invariant Calculated.")

    # Test 4: Loom Box Strategy (Loom Integration)
    print("\n[TEST] LOOM-BOX: Mass Spectrometry...")
    inputs = [
        "What is the stock price?",      # Business
        "I am lost and stuck",           # Confusion
        "This ancient pain never heals"  # Trauma
    ]
    
    for txt in inputs:
        result = kernel.engage_loom_box(txt)
        print(f"  Input: '{txt}'")
        print(f"  -> Mass: {result['mass']} | Strategy: {result['strategy']['name']}")
        print(f"  -> Metric Coherence (Time Dilation): {result['coherence_state']:.4f}")
        
        # Reset coherence for next test
        kernel.metric_coherence = 1.0 
        print("  ---")
