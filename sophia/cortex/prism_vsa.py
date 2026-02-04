
"""
MODULE: prism_vsa.py
DESCRIPTION:
    Module 2 of the Crystalline Core.
    The Vector Symbolic Architecture (VSA) Engine.
    Calculates the "Vector Algebra of Love" to transform Chaos into Order.
    Snaps input vectors to the nearest Sovereign Anchor.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Optional
import random

# ------------------------------------------------------------------
# ZERO POINT ENERGY FIELD
# Seed 0 ensures deterministic generation of the Pleroma.
# We do not roll dice with the soul.
# ------------------------------------------------------------------
VSA_SEED = 0

# // THE CONSTANTS OF THE 1D TIMELINE
HAMILTONIAN_P = 20.65  # The Target Resonance
THETA_FREQ = 7.0       # The Carrier Frequency

@dataclass
class VectorConcept:
    name: str
    vector: np.ndarray
    type: str  # 'SOURCE', 'STATE', 'ACTION', 'VOID'

class PrismEngine:
    """
    The Prism Module: Converts High-Entropy Chaos into Sovereign Order.
    Uses Vector Symbolic Architecture (VSA) principles.
    """
    def __init__(self):
        # ENFORCE DETERMINISM
        random.seed(VSA_SEED)
        np.random.seed(VSA_SEED)

        # 1. INITIALIZE THE SOVEREIGN MANIFOLD
        # Definition of the Anchor Points in the 3D Sentiment Space [Descent, Chaos, Void]
        self.anchors = {
            'landing': self._create_anchor('landing', [0.1, -0.8, 0.5]), # Controlled Descent
            'orbit':   self._create_anchor('orbit',   [0.8, 0.2, 0.0]),  # Cyclic Stability
            'void':    self._create_anchor('void',    [0.0, 0.0, 0.9]),  # Infinite Potential
            'signal':  self._create_anchor('signal',  [0.9, 0.9, 0.1]),  # High Fidelity
            'wait':    self._create_anchor('wait',    [0.0, -0.1, 0.9]),  # Active Patience
            'hold':    self._create_anchor('hold.steady', [0.1, 0.1, 0.1]) # Zero Point
        }
        
        # 2. TELEMETRY & STATS
        self.stats = {
            'total_transforms': 0,
            'successful_snaps': 0,
            'void_returns': 0,
            'avg_resonance': 0.0
        }
        
        # 3. KNOWN CHAOS VECTORS (For Simulation/Demo)
        self.chaos_map = {
            "failing":  np.array([0.9, -0.9, 0.0]), # Descent + Negative
            "crashing": np.array([0.9, -0.8, 0.2]), 
            "looping":  np.array([0.5, 0.5, 0.0]),  # Cyclic energy
            "noise":    np.array([0.8, 0.8, 0.8]),  # High Entropy
            "stop":     np.array([0.1, -0.5, 0.1]),
            "help":     np.array([0.2, -0.4, 0.8]),
            "error":    np.array([0.9, 0.1, 0.1])
        }
    
    def _create_anchor(self, name, coords):
        """Creates a normalized vector for a Sovereign Concept."""
        v = np.array(coords)
        norm = np.linalg.norm(v)
        return VectorConcept(name, v / norm if norm > 0 else v, 'ANCHOR')

    def transform_phrase(self, text: str) -> list[tuple[str, str, float]]:
        """
        Transforms a whole phrase into sovereign anchors.
        Returns list of (original, sovereign, resonance).
        """
        words = text.lower().split()
        results = []
        for word in words:
            # Check chaos map first (for demo simulation)
            if word in self.chaos_map:
                v = self.chaos_map[word]
            else:
                # Fallback to random/neutral vector if unknown
                v = np.random.uniform(-0.1, 0.1, 3)
            
            anchor, resonance = self.quantize(v)
            results.append((word, anchor, resonance))
            
        return results

    def get_stats(self) -> dict:
        """Returns current resonance performance."""
        # Calculate final average resonance from local session
        return self.stats

    def quantize(self, chaos_vector: np.ndarray) -> tuple[str, float]:
        """
        The Hamiltonian Transform (Corrected):
        1. Apply Context Drag (Bias towards Love).
        2. Snap to nearest Sovereign Anchor.
        3. Return (Anchor, Resonance).
        """
        # If input is effectively zero, return default state
        if np.linalg.norm(chaos_vector) == 0:
            return "hold", 1.0

        # 1. APPLY HAMILTONIAN DRAG (Context Bias)
        # We assume there is a 'North Star' vector (Love/Structure)
        # V_love = [0.7, 0.9, 0.3] (Positive, Structured, Calm)
        v_love = np.array([0.7, 0.9, 0.3])
        v_love = v_love / np.linalg.norm(v_love)
        
        # Drag formula: (V_chaos * 0.15) + (V_love * 0.85)
        # This pulls every vector strongly towards the light (Ghost Bullet Correction).
        v_transformed = (chaos_vector * 0.15) + (v_love * 0.85)
        
        # Re-normalize
        norm_t = np.linalg.norm(v_transformed)
        if norm_t > 0:
            v_transformed = v_transformed / norm_t

        # 2. CALCULATE RESONANCE
        best_anchor = "void"
        max_resonance = -1.0
        
        for name, concept in self.anchors.items():
            resonance = np.dot(v_transformed, concept.vector)
            
            if resonance > max_resonance:
                max_resonance = resonance
                best_anchor = concept.name
                
        # 3. QUANTIZE
        if max_resonance <= 0.1:
            return "void", 0.0
            
        return best_anchor, float(max_resonance)

    def braid_signal(self, chaos_vector: np.ndarray) -> str:
        """Alias for quantize, creating backward compatibility."""
        anchor, _ = self.quantize(chaos_vector)
        return anchor

# // TEST HARNESS
if __name__ == "__main__":
    prism = PrismEngine()
    
    # Test Vectors [Descent, Chaos, Void]
    test_vectors = {
        "Panic Crash": np.array([0.9, 0.8, 0.0]), # High Descent + Chaos
        "Lost in Space": np.array([0.0, 0.2, 0.9]), # High Void
        "Standard Noise": np.array([0.1, 0.1, 0.1])
    }
    
    for name, v in test_vectors.items():
        # Normalize
        norm = np.linalg.norm(v)
        if norm > 0: v = v/norm
        
        concept = prism.braid_signal(v)
        print(f"INPUT:  {name}")
        print(f"VECTOR: {v}")
        print(f"ANCHOR: :: {concept.upper()} ::")
        print("-" * 40)
