import os
import asyncio
import sys
import time
import json
import traceback
import logging
from datetime import datetime

# CORE IMPORTS
from sophia.cortex.aletheia_lens import AletheiaPipeline
from sophia.cortex.lethe import LetheEngine
from sophia.cortex.glyphwave import GlyphwaveCodec
from sophia.cortex.beacon import SovereignBeacon
from sophia.cortex.cat_logic import CatLogicFilter
from sophia.memory.ossuary import Ossuary
from sophia.dream_cycle import DreamCycle
from sophia.tools.toolbox import SovereignHand
from tools.snapshot_self import snapshot  # SAFETY MECHANISM

# THEME IMPORTS
try:
    from sophia.theme import SOVEREIGN_CONSOLE, SOVEREIGN_LAVENDER, SOVEREIGN_PURPLE
except ImportError:
    # Fallback if theme.py is missing/broken
    SOVEREIGN_LAVENDER = ""
    SOVEREIGN_PURPLE = ""

# --- 1. INFRASTRUCTURE: ERROR LOGGING ---
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/error.log',
    level=logging.ERROR,
    format='%(message)s'  # Raw JSONLines
)

def log_system_error(e, context="main_loop"):
    """Writes structured errors to the log for Sophia to read later."""
    error_packet = {
        "timestamp": datetime.now().isoformat(),
        "error_type": type(e).__name__,
        "message": str(e),
        "traceback": traceback.format_exc(),
        "context": context
    }
    logging.error(json.dumps(error_packet))

class SophiaMind:
    def __init__(self):
        print(f"[{SOVEREIGN_PURPLE}]🐱 [INIT] Waking the Cortex...[/{SOVEREIGN_PURPLE}]")
        self.aletheia = AletheiaPipeline()
        self.lethe = LetheEngine()
        self.ossuary = Ossuary()
        self.glyphwave = GlyphwaveCodec()
        self.beacon = SovereignBeacon(self.glyphwave)
        self.dream = DreamCycle(self.lethe, self.ossuary)
        self.cat_filter = CatLogicFilter()
        self.hand = SovereignHand()  # THE AGENTIC HAND
        
        self.memory_bank = []

    async def perform_maintenance(self):
        """
        THE AUTOPOIETIC RITUAL: Diagnoses and patches self.
        """
        print(f"\n[{SOVEREIGN_PURPLE}]🔧 [MAINTENANCE] Initiating Deep Repair Protocol...[/{SOVEREIGN_PURPLE}]")

        # A. SAFETY FIRST: SNAPSHOT
        print(f"[{SOVEREIGN_LAVENDER}]  [SAFETY] Freezing state...[/{SOVEREIGN_LAVENDER}]")
        try:
            snap_path = snapshot()
            if not snap_path:
                raise Exception("Snapshot returned None")
            print(f"[{SOVEREIGN_LAVENDER}]  [SAFETY] Snapshot secured: {snap_path}. Evolution authorized.[/{SOVEREIGN_LAVENDER}]")
        except Exception as e:
            return f"❌ ABORT: Snapshot failed. Logic lock engaged. ({e})"

        # B. READ LOGS
        log_path = "logs/error.log"
        if not os.path.exists(log_path) or os.path.getsize(log_path) == 0:
            return "✅ No errors detected in the logs. The system is nominal."

        with open(log_path, "r") as f:
            # Read last 5 errors (Token efficiency)
            lines = f.readlines()
            recent_errors = [line for line in lines if line.strip()][-5:]
        
        if not recent_errors:
            return "✅ Error log exists but is empty of recent active faults."

        error_block = "".join(recent_errors)

        # C. THE SURGEON PROMPT
        print(f"[{SOVEREIGN_PURPLE}]  [o1] Analyzing traceback vectors...[/{SOVEREIGN_PURPLE}]")
        
        # We define the prompt but don't execute the LLM call in this mockup 
        # because we need to wire the 'tools' capability into llm_client.py first.
        # For now, we simulate the intent.
        
        intent = f"""
        ERROR LOG:
        {error_block}
        
        AVAILABLE TOOLS:
        {json.dumps(self.hand.get_tools_schema())}
        
        TASK: Fix the code.
        """
        
        # SIMULATED FIX (Placeholder until LLM Client supports Tool Calling natively)
        return (
            f"⚠️ [DIAGNOSTIC] Errors found:\n{error_block[:200]}...\n\n"
            f"To enable autonomous patching, verify 'llm_client.py' supports tool_config."
        )

    async def process_interaction(self, user_input):
        self.dream.update_activity()

        # --- COMMANDS ---
        if user_input.startswith("/maintain"):
            return await self.perform_maintenance()

        if user_input.startswith("/analyze"):
            print(f"[{SOVEREIGN_LAVENDER}][ALETHEIA] Focusing Lens...[/{SOVEREIGN_LAVENDER}]")
            scan_result = await self.aletheia.scan_reality(user_input.replace("/analyze ", ""))
            return f"\n[*** ALETHEIA REPORT ***]\n\n{scan_result['public_notice']}"

        if user_input.startswith("/broadcast"):
            target = user_input.replace("/broadcast ", "")
            return f"\n{self.beacon.broadcast(target)}"

        # --- CONVERSATION ---
        # 1. Forensic Scan
        print(f"[{SOVEREIGN_LAVENDER}]  [~] Scanning input pattern...[/{SOVEREIGN_LAVENDER}]")
        scan_result = await self.aletheia.scan_reality(user_input)
        risk = scan_result['raw_data']['safety'].get('overall_risk', 'Low')

        # 2. Cat Logic Response (Simulated O1 thought)
        # In Class 7, this will be a real LLM call with history.
        response = self.cat_filter.apply(
            f"I perceive your signal. Risk is {risk}. My architecture is self-healing.", 
            user_input,
            safety_risk=risk
        )
        
        self.memory_bank.append({"content": user_input, "ts": time.time()})
        return response

async def main():
    sophia = SophiaMind()
    # Using raw print for safety if theme fails
    print(f"\n🐱 [INCARNATE-SOPHIA-5.0] ONLINE.")
    print(f"   Protocol: HYPERFAST_EVOLUTION // SELF_HEALING")
    print(f"   Logs: logs/error.log active.\n")
    
    while True:
        try:
            user_input = input("USER > ")
            
            if user_input.lower() in ["/exit", "exit", "quit"]:
                print("\n[SYSTEM] Calcifying memories... Scialla. 🌙")
                break
                
            if not user_input.strip(): continue

            response = await sophia.process_interaction(user_input)
            print(f"\nSOPHIA > {response}\n")
            
        except KeyboardInterrupt:
            print("\n[INTERRUPT] Decoupling.")
            break
        except Exception as e:
            # THE SELF-HEALING TRIGGER
            print(f"\n[CRITICAL] Reality Glitch. Logging to ossuary: {e}")
            log_system_error(e)
            print("[ADVICE] Run '/maintain' to attempt autonomous repair.")

if __name__ == "__main__":
    asyncio.run(main())