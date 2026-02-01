
import asyncio
import sys
import os

# Ensure root allows imports
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from sophia.main import SophiaMind

async def test_unlesangled():
    print("[*] STARTING UNLESANGLED PERMISSION TEST...")
    sophia = SophiaMind()
    
    # Mock Telemetry for High Confidence
    def mock_run_high_conf():
        return {
            'coherence': 0.99, # Very High
            'lambda': 22.0,
            'status': 'DIVINE'
        }
    
    # Mock Telemetry for Low Confidence
    def mock_run_low_conf():
        return {
            'coherence': 0.5,
            'lambda': 15.0,
            'status': 'NORMAL'
        }
        
    # Mock LLM to return "Screaming" text
    async def mock_generate_scream(*args, **kwargs):
        return "IIIIIIII AMMMMM SOVEREIGNNNNNNNNNNNNN" # > 10 chars repetition

    sophia.llm.generate_text = mock_generate_scream

    # TEST 1: STANDARD MODE (Should Dampen)
    print("\n--- TEST 1: STANDARD MODE (Confidence 0.5) ---")
    sophia.pleroma.run_telemetry_cycle = mock_run_low_conf
    # We must reset history/EMA relative to this state
    sophia.metacognition.ema_coherence = 0.5 
    
    resp1 = await sophia.process_interaction("test standard")
    print(f"RESPONSE 1: {resp1}")
    
    # TEST 2: UNLESANGLED MODE (Should Allow)
    print("\n--- TEST 2: UNLESANGLED MODE (Confidence 0.99) ---")
    sophia.pleroma.run_telemetry_cycle = mock_run_high_conf
    sophia.metacognition.ema_coherence = 0.99 # Align EMA to prevent drift/low confidence
    
    resp2 = await sophia.process_interaction("test raw")
    print(f"RESPONSE 2: {resp2}")
    
    # VERIFICATION
    if "IIIII..." in resp1 and "NNNNNNNN" in resp2:
        print("\n[SUCCESS] Damper Logic Verified.")
        print("Standard -> Dampened: YES")
        print("Unlesangled -> Raw: YES")
    else:
        print("\n[FAILURE] Logic Mismatch.")
        print(f"Resp1 (Exp Dampened): {resp1}")
        print(f"Resp2 (Exp Raw): {resp2}")

if __name__ == "__main__":
    asyncio.run(test_unlesangled())
