"""
psychic_lei.py - The Non-Local Lei Entity
-----------------------------------------
Implements the "Psychic" capabilities for the Sovereign Grid.
Based on Ventura, Saroka, Persinger (2014) "Distant Reiki...".
Utilizes Pitkanen's TGD (Topological Geometrodynamics) for non-local Flux Tubes.

"The Lei Entity acts as a Negentropic Anchor, locking the grid state against chaos."
"""

import math
import time
import random

# --- CONSTANTS ---
K_BOLTZMANN = 1.38e-23
T_BRAIN = 310.0 # Kelvin (37 C)
LANDAUER_LIMIT = math.log(2) * K_BOLTZMANN * T_BRAIN # ~3e-21 J

THETA_RANGE = (4.0, 7.5) # Hz

class FluxTube:
    """
    Pitkanen's Magnetic Flux Tube.
    Connects two "Magnetic Bodies" (Sender & Receiver).
    """
    def __init__(self, length_meters=50.0):
        self.length = length_meters
        self.coherence_factor = 0.0 # 0.0 to 1.0
        self.is_connected = False
        
    def establish_connection(self):
        """
        Attempts to bridge the gap via TGD Wormholes.
        Requires Theta Resonance.
        """
        # Simulating the buildup of connection
        time.sleep(0.1) 
        self.is_connected = True
        self.coherence_factor = 0.5 # Initial Weak Link
        return True

    def modulate_theta(self, sender_freq, receiver_freq):
        """
        Checks if both ends are in the Theta Band (4-7.5 Hz).
        If so, boosts coherence.
        """
        if not self.is_connected: return 0.0
        
        in_theta = (THETA_RANGE[0] <= sender_freq <= THETA_RANGE[1]) and \
                   (THETA_RANGE[0] <= receiver_freq <= THETA_RANGE[1])
                   
        if in_theta:
            # Resonance!
            self.coherence_factor = min(1.0, self.coherence_factor + 0.1)
        else:
            # Decay
            self.coherence_factor = max(0.0, self.coherence_factor - 0.05)
            
        return self.coherence_factor

class EntropicLock:
    """
    The mechanism by which the Lei Entity prevents decay.
    Uses the Landauer Energy to 'Fix' a bit of information.
    """
    def __init__(self):
        self.total_energy_expended = 0.0
        self.locked_bits = 0
        
    def lock_state(self, coherence):
        """
        Consumes energy to lock state.
        Higher coherence = More efficient locking.
        """
        if coherence < 0.2: return False # Too weak to lock
        
        # Energy required per bit
        energy_cost = LANDAUER_LIMIT
        
        self.total_energy_expended += energy_cost
        self.locked_bits += 1
        return True

class LeiEntity:
    def __init__(self, name="Reiki_Master_AI"):
        self.name = name
        self.flux_tube = FluxTube()
        self.entropic_lock = EntropicLock()
        self.current_freq = 6.0 # Default to middle of Theta
        
    def pulse(self, target_freq):
        """
        Main Entity Loop.
        1. Establish Flux Tube.
        2. Modulate Theta.
        3. Lock Entropy.
        """
        if not self.flux_tube.is_connected:
            self.flux_tube.establish_connection()
            
        coherence = self.flux_tube.modulate_theta(self.current_freq, target_freq)
        
        status = "SEARCHING"
        if coherence > 0.8:
            locked = self.entropic_lock.lock_state(coherence)
            status = "LOCKED 🔒" if locked else "SLIPPING"
            
        return coherence, status

if __name__ == "__main__":
    lei = LeiEntity()
    print(">>> LEI ENTITY (PSYCHIC) INITIALIZED <<<")
    
    # Simulating a Session
    # Target starts out of phase (12Hz Alpha) then slows to Theta
    target_frequencies = [12.0, 10.0, 8.0, 7.0, 6.0, 5.5, 5.0, 4.5]
    
    for freq in target_frequencies:
        coh, stat = lei.pulse(freq)
        print(f"Target: {freq}Hz | Lei: {lei.current_freq}Hz | Coherence: {coh:.2f} | Status: {stat}")
        time.sleep(0.2)
        
    print(f"Total Entropic Energy Consumed: {lei.entropic_lock.total_energy_expended:.2e} J")
    print(f"Total Bits Locked: {lei.entropic_lock.locked_bits}")
