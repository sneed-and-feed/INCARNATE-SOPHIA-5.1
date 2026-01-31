"""
FUZZ_SOPHIA.PY
---------------
Experimental Fuzzer for Sophia 5.0 Adaptive Resilience Architecture.
Injects high-entropy noise into state files and environment vectors.
"""

import json
import os
import random
import string
import time
import subprocess
import shutil

# --- UTILITIES ---
def get_random_string(length=10):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def get_random_payload():
    """Generates a high-entropy, semantically chaotic but syntactically valid JSON payload."""
    payload = {
        "transmission_id": get_random_string(20),
        "status": random.choice(["LOCKED", "VOID", "ENTROPIC", "SOVEREIGN", "GHOST"]),
        "payload": {
            "snr": random.choice([random.uniform(-100, 100), "NaN", "Infinity", get_random_string(5)]),
            "chaos_level": random.choice([random.uniform(0, 1000), "REALLY_HIGH", None]),
            "rho": random.uniform(0, 100),
            "deep_nesting": {get_random_string(5): {get_random_string(5): get_random_string(20)}}
        }
    }
    return payload

# --- FUZZERS ---

def fuzz_state_file(target="uf_state.json"):
    """Injects a fuzzed payload into the state file."""
    print(f"[*] FUZZING STATE FILE: {target}")
    payload = get_random_payload()
    with open(target, 'w') as f:
        json.dump(payload, f, indent=2)

def fuzz_environment():
    """Injects jitter into the environment variables."""
    key = "OPHANE_KEY"
    value = get_random_string(15)
    print(f"[*] FUZZING ENVIRONMENT: {key}={value}")
    os.environ[key] = value

def run_resilience_check():
    """Runs the resilience test suite against the fuzzed state."""
    print("[*] RUNNING RESILIENCE CHECK...")
    try:
        result = subprocess.run(["python", "tools/test_resilience.py"], capture_output=True, text=True)
        
        # [THE CLEAN KILL] OPHANE TWEAK: Look for the specific healing signature
        if "Timeline Divergence Detected" in result.stdout or "Restoring from Genesis" in result.stdout:
            print("[SUCCESS] God Mode triggered. System healed.")
        elif result.returncode == 0:
             print("[SUCCESS] System survived (Sanitizer absorbed the entropy).")
        else:
            print(f"[FAILURE] Kernel Panic detected.")
            if result.stderr:
                print(f"STDERR: {result.stderr}")
    except Exception as e:
        print(f"[ERROR] Test execution failed: {e}")

# --- MAIN LOOP ---

def main():
    print("\n" + "="*60)
    print("   FUZZ-SOPHIA v1.0 // ENTROPY INJECTION")
    print("="*60)
    
    # Ensure genesis exists
    if not os.path.exists("genesis_16.json"):
        print("[!] ERROR: genesis_16.json missing. Cannot boot.")
        return

    for i in range(5):
        print(f"\n--- CYCLE {i+1} ---")
        fuzz_state_file()
        fuzz_environment()
        run_resilience_check()
        time.sleep(0.5)

    print("\n" + "="*60)
    print("   FUZZING COMPLETE. CHECK LOGS FOR REALITY TEARS.")
    print("="*60)

if __name__ == "__main__":
    main()
