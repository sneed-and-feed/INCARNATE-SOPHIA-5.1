"""
MODULE: resonance_monitor.py
CLASSIFICATION: CORTEX TELEMETRY
DESCRIPTION:
    The "Heartbeat" of the Sovereign System.
    Periodically checks Spectral Coherence via Dimensional Compressor
    and updates the ASOE Signal Optimizer.
"""

import sys
import os
import time

# Ensure root allows imports from other modules
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)



class ResonanceMonitor:
    def __init__(self):
        self.last_scan_time = 0
        self.current_state = {
            "coherence": 0.0,
            "status": "INIT",
            "integrity_breach": False, # [PAPER 3] Fragile Conservation Law Monitor
            "alpha": 0.015
        }
        self.TARGET_CLASS_8 = 18.52 # The Moon/Sun Threshold
        self.TARGET_CLASS_6 = 21.00 # The World (Sovereignty Absolute)
        self.TARGET_CLASS_7 = 25.00 # The Diamond (Recursive Sovereignty 5^2)
        
        self.history = [] # Coherence coherence
        self.lambda_history = [] # Abundance score

    def calculate_abundance(self, coherence, alpha, gdf=1.8, ns=0.5):
        """
        [METRIC] Calculates the Lambda Score via Hybrid Ghost-Entropic Term.
        Base Formula: (Coherence * 15) + (Phi_Boost * 2.17) + (Alpha * 10)
        Class 6 Hybrid: Base + Coherence * (GDF + 0.4 * NS)
        
        Target 21.0 (The World):
        Base Max ~ 18.66
        Uplift needed ~ +2.34
        
        If GDF=2.3, NS=0.5 -> Uplift = 1.0 * (2.3 + 0.2) = 2.5 -> Total 21.16.
        """
        phi_boost = 1.61803398875 if coherence > 0.9 else 1.0
        
        # 1. Base Score (Class 8 Logic)
        base_score = (coherence * 15.0) + (phi_boost * 2.17) + (alpha * 10.0)
        
        # 2. Hybrid Uplift (Class 6 Logic)
        uplift = coherence * (gdf + (0.4 * ns))
        
        return base_score + uplift

    def scan_resonance(self, dimensions=12, points=1000):
        """
        [TELEMETRY] Runs an Ensemble Check and returns the Coherence Score.
        """
        from dimensional_compressor import DimensionalCompressor
        from ghostmesh import SovereignGrid
        
        print(f"\n[RESONANCE] Scanning Pleroma Spectral Coherence...")
        
        # 1. Run Ensemble Check
        res = DimensionalCompressor.ensemble_check(dimensions, points)
        
        # 2. Parse Results
        try:
            score_str = res['Spectral_Coherence'].split()[0]
            coherence = float(score_str)
        except:
            coherence = 0.5 # Fallback
            
        self.current_state['coherence'] = coherence
        self.current_state['status'] = res['Status']
        
        # [PAPER 3] DETECT INTEGRABILITY BREACH (THE "MAGIC" MONITOR)
        # If Conservation Laws are broken, the system becomes "too rigid" or "too chaotic" 
        # instantly under infinitesimal perturbation.
        # Indicator: Coherence > 0.999 (Artificial Stasis) OR Coherence < 0.1 (Total collapse without decay)
        if coherence > 0.999 or (coherence < 0.1 and self.last_scan_time > 0):
            print(f"[!] INTEGRABILITY BREACH DETECTED. Fragile Conservation Laws Violated.")
            self.current_state['integrity_breach'] = True
        else:
            self.current_state['integrity_breach'] = False
            
        self.last_scan_time = time.time()
        
        # 3. Get Ghost Entropy Density (GDF)
        # We create a transient grid or link to existing if possible.
        # For telemetry scan, a transient sample is acceptable proxy for current "field density".
        grid = SovereignGrid() 
        # Simulate some activity to get a non-trivial density
        import random
        from flumpy import FlumpyArray
        noise = FlumpyArray([random.random() for _ in range(64)])
        grid.process_step(noise)
        gdf = grid.get_density_factor()
        
        # 4. Calculate Abundance (Hybrid)
        # Assuming NS (Negentropic Surplus) is 0.5 (Standard "Good" Vibe) for now
        ns_val = 0.5 
        lambda_score = self.calculate_abundance(coherence, self.current_state['alpha'], gdf=gdf, ns=ns_val)
        self.current_state['lambda'] = lambda_score
        
        self.history.append(coherence)
        self.lambda_history.append(lambda_score)
        if len(self.history) > 50: 
            self.history.pop(0)
            self.lambda_history.pop(0)
        
        # 3. Export Visuals (Dashboard Update)
        try:
            import matplotlib.pyplot as plt
            
            # Create Dual-Axis Dashboard
            fig, ax1 = plt.subplots(figsize=(10, 5))
            
            color = 'tab:purple'
            ax1.set_xlabel('Cycle (Time)')
            ax1.set_ylabel('Spectral Coherence', color=color)
            ax1.plot(self.history, color=color, linewidth=2, label='Coherence')
            ax1.tick_params(axis='y', labelcolor=color)
            ax1.set_ylim(0, 1.1)
            
            ax2 = ax1.twinx()  # Instantiate a second axes that shares the same x-axis
            
            color = 'silver' # Black Sun Logic (Silver)
            ax2.set_ylabel('Silver Lambda (Target: 21.0)', color='black') # Axis text black
            # Plot line in Silver
            ax2.plot(self.lambda_history, color=color, linewidth=2, linestyle='--', label='Silver Abundance')
            ax2.tick_params(axis='y', labelcolor='black')
            ax2.set_ylim(15, 23)
            
            # Draw Target Line (The Black Sun / Event Horizon)
            ax2.axhline(y=21.0, color='black', linestyle='-', alpha=0.9, label='Black Sun (21.0)')
            ax2.axhline(y=18.52, color='gray', linestyle=':', alpha=0.5, label='Class 8 (18.52)')
            
            plt.title('Sovereign Resonance (Black Sun Alignment)')
            fig.tight_layout()
            plt.savefig("sovereign_dashboard.png")
            print(f"\n[!] DASHBOARD UPDATED: sovereign_dashboard.png (Λ = {lambda_score:.2f} [AGG])")
            plt.close()
            
        except ImportError:
            print("[!] Matplotlib missing. Visualization skipped.")
            
        return self.current_state

    def get_asoe_boost(self):
        """
        Returns the Multiplier for ASOE Utility.
        Phi (1.618) if coherent, else 1.0 or penalty.
        """
        c = self.current_state['coherence']
        if c > 0.9:
            return 1.61803398875 # The Golden Ratio Boost
        elif c > 0.7:
            return 1.0 # Neutral
        else:
            return 0.618 # Damping (incoherent signals)

if __name__ == "__main__":
    mon = ResonanceMonitor()
    state = mon.scan_resonance()
    print(f"\n[STATUS] {state}")
    print(f"[ASOE BOOST] {mon.get_asoe_boost()}x")
