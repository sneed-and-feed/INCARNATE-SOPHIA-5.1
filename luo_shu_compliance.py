"""
MODULE: luo_shu_compliance.py
VERSION: INCARNATE 5.0
DESCRIPTION:
    The Magic Square Evaluator.
    Maps 9 core metrics to the 3x3 Luo Shu Grid.
    Ideal Sum: 15.
"""

import numpy as np
import os
import json
import shutil

class LuoShuEvaluator:
    def __init__(self):
        self.magic_sum = 15.0

    def evaluate(self, metrics):
        """
        Map metrics to the 3x3 grid:
        [ 4  9  2 ]
        [ 3  5  7 ]
        [ 8  1  6 ]
        """
        
        # Normalize inputs to Luo Shu targets
        # Assuming metrics dictionary contains: snr, alpha, stability, rho, coherence, utility, g, chaos, sigma
        
        grid = np.zeros((3, 3))
        
        # Row 1: 4, 9, 2
        grid[0, 0] = (metrics.get('snr', 5.0) / 5.0) * 4.0
        grid[0, 1] = metrics.get('alpha', 1.0) * 9.0
        grid[0, 2] = (metrics.get('reality_stability', 100.0) / 100.0) * 2.0
        
        # Row 2: 3, 5, 7
        grid[1, 0] = (metrics.get('rho', 95.0) / 95.0) * 3.0
        grid[1, 1] = (metrics.get('timeline_coherence', 100.0) / 100.0) * 5.0
        grid[1, 2] = metrics.get('utility', 1.0) * 7.0
        
        # Row 3: 8, 1, 6
        grid[2, 0] = (1.0 - metrics.get('g_parameter', 1.0) + 0.1) * 8.0 # Boost if sovereign
        grid[2, 1] = (max(0, 100 - metrics.get('chaos_level', 0)) / 100.0) * 1.0
        grid[2, 2] = (1.0 - abs(metrics.get('sigma_map', 0))) * 6.0
        
        # Calculate Sums
        row_sums = np.sum(grid, axis=1)
        col_sums = np.sum(grid, axis=0)
        diag_sums = [np.trace(grid), np.trace(np.fliplr(grid))]
        
        all_sums = list(row_sums) + list(col_sums) + diag_sums
        
        # Compliance = Inverse of mean deviation from 15
        torsion = np.mean([abs(s - self.magic_sum) for s in all_sums])
        compliance = max(0, 100 - (torsion * 10))
        
        return {
            'grid': grid,
            'torsion': torsion,
            'compliance': compliance,
            'status': "ALIGNED" if compliance > 90 else "TORSION DETECTED" if compliance > 50 else "HARMONIC COLLAPSE"
        }

class ConfigHealthMonitor:
    """
    [LOVE 111] Self-Healing Configuration.
    Validates structural integrity and restores from genesis on fail.
    """
    @staticmethod
    def check_health(config_path, genesis_path="genesis_16.json"):
        """
        Validates the configuration health.
        If unhealthy, regenerates from genesis.
        """
        if not os.path.exists(config_path):
            print(f"  [!] HEALTH: Config '{config_path}' missing. Regenerating.")
            shutil.copy(genesis_path, config_path)
            return True

        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
            
            # [GOD-MODE] PERMISSIVE TYPE SANITIZATION
            # If token or transmission_id is an Int (common typo), cast to Str.
            dirty = False
            for key in ['transmission_id', 'status']:
                if key in data and not isinstance(data[key], str):
                    print(f"  [~] [LUO SHU] Type Mismatch for '{key}'. Sanitizing {type(data[key])} -> str.")
                    data[key] = str(data[key])
                    dirty = True
            
            # Sub-payload check
            payload = data.get('payload', {})
            if isinstance(payload, str): # Rare but seen in deep-corruption
                print("  [~] [LUO SHU] Payload is stringified. Parsing JSON.")
                data['payload'] = json.loads(payload)
                dirty = True

            if dirty:
                print(f"  [SUCCESS] [LUO SHU] Type-safe state achieved. Anchoring to {config_path}.")
                with open(config_path, 'w') as f:
                    json.dump(data, f, indent=2)
            
            # Simple structural check
            required_keys = ['transmission_id', 'status', 'payload']
            if any(k not in data for k in required_keys):
                 raise ValueError("Missing core keys.")
            
            return True
        except Exception as e:
            print(f"  [!] [LUO SHU] Health Check Failed ({e}). Initiating Deep Reconstruction...")
            shutil.copy(config_path, config_path + ".bak")
            shutil.copy(genesis_path, config_path)
            return False

if __name__ == "__main__":
    # Test with baseline metrics
    test_metrics = {
        'snr': 5.0,
        'alpha': 1.0,
        'reality_stability': 100.0,
        'rho': 95.0,
        'timeline_coherence': 100.0,
        'utility': 1.0,
        'g_parameter': 0.1, # Near Sovereign
        'chaos_level': 0,
        'sigma_map': 0
    }
    evaluator = LuoShuEvaluator()
    res = evaluator.evaluate(test_metrics)
    print(f"Compliance: {res['compliance']:.2f}% | Status: {res['status']}")
    print("Grid:\n", res['grid'])
