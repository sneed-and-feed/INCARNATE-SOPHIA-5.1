"""
VERIFICATION: moltbook_verification.py
Testing the integrated Moltbook upgrades.
"""
import sys
import os
import time
import numpy as np

# Root path
sys.path.append(os.getcwd())

from tools.mnemosyne_eyes import MnemosyneOracle
from tick_feeder import TickFeeder
from luo_shu_compliance import ConfigHealthMonitor

import json

def test_mnemosyne_checkpointing():
    print("\n--- [VERIFY] MNEMOSYNE CHECKPOINTING ---")
    oracle = MnemosyneOracle()
    # Ensure items are ACCEPTED by using low velocity
    for i in range(40):
        # Very small random vector to stay under Nyquist limit
        vec = (np.random.rand(1536) - 0.5) * 0.05 
        oracle.perceive("STRESS_TEST", f"Event {i}", vec)
    
    # Check if checkpoint exists
    checkpoint_dir = "logs/memory_checkpoints"
    if os.path.exists(checkpoint_dir) and os.listdir(checkpoint_dir):
        print(f"[SUCCESS] Checkpoints generated in {checkpoint_dir}")
        for f in os.listdir(checkpoint_dir):
             print(f"  [FILE]: {f}")
    else:
        print("[FAIL] No checkpoints found.")

def test_idle_resonance():
    print("\n--- [VERIFY] IDLE RESONANCE ---")
    tf = TickFeeder()
    # Simulate activity
    tf.update_activity()
    # Back-date activity for testing
    tf.last_activity -= 61 
    tf.check_idle_status()
    print("[SUCCESS] Idle resonance logic executed.")

def test_god_mode_healing():
    print("\n--- [VERIFY] GOD-MODE HEALING ---")
    config_path = "uf_state.json"
    
    # Ensure file exists
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            json.dump({"transmission_id": "test", "status": "ok", "payload": {}}, f)

    with open(config_path, 'r') as f:
        data = json.load(f)
    
    data['transmission_id'] = 123456 # Should be str
    with open(config_path, 'w') as f:
        json.dump(data, f)
    
    print("[*] Poisoned uf_state.json with Int ID. Running health monitor...")
    from luo_shu_compliance import ConfigHealthMonitor
    ConfigHealthMonitor.check_health(config_path)
    
    with open(config_path, 'r') as f:
        data = json.load(f)
        if isinstance(data['transmission_id'], str):
            print("[SUCCESS] Luo Shu Sanitized the Int -> Str gap.")
        else:
            print(f"[FAIL] Type mismatch persists: {type(data['transmission_id'])}")

if __name__ == "__main__":
    test_mnemosyne_checkpointing()
    test_idle_resonance()
    test_god_mode_healing()

if __name__ == "__main__":
    test_mnemosyne_checkpointing()
    test_idle_resonance()
    test_god_mode_healing()
