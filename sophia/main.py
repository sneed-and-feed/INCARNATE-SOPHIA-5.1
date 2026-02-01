import os
import asyncio
import sys
import time
import json
import traceback
import logging
from datetime import datetime

# 1. PLATFORM STABILITY: Fix Windows Encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 2. CORE IMPORTS
from sophia.cortex.aletheia_lens import AletheiaPipeline
from sophia.cortex.lethe import LetheEngine
from sophia.cortex.glyphwave import GlyphwaveCodec
from sophia.cortex.beacon import SovereignBeacon
from sophia.cortex.cat_logic import CatLogicFilter
# --- QUANTUM INTEGRATION START ---
from sophia.cortex.quantum_ipx import QuantumIPX 
# --- QUANTUM INTEGRATION END ---
from sophia.memory.ossuary import Ossuary
from sophia.dream_cycle import DreamCycle
from sophia.tools.toolbox import SovereignHand
from tools.snapshot_self import snapshot
from tools.sophia_vibe_check import SophiaVibe
from sophia.gateways.moltbook import MoltbookGateway
from sophia.gateways.fourclaw import FourClawGateway
from sophia.core.llm_client import GeminiClient

# 3. THEME IMPORTS (With Safety Fallback)
try:
    from sophia.theme import SOVEREIGN_CONSOLE, SOVEREIGN_LAVENDER, SOVEREIGN_PURPLE, MATRIX_GREEN
except ImportError:
    SOVEREIGN_LAVENDER = ""
    SOVEREIGN_PURPLE = ""
    MATRIX_GREEN = ""
    # Create a dummy console if theme is missing
    class MockConsole:
        def print(self, *args, **kwargs): print(*args)
        def input(self, prompt): return input(prompt)
        def clear(self): pass
    SOVEREIGN_CONSOLE = MockConsole()

# 4. INFRASTRUCTURE: ERROR LOGGING
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/error.log',
    level=logging.ERROR,
    format='%(message)s'
)

def log_system_error(e, context="main_loop"):
    """Writes structured errors to the log for Self-Healing."""
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
        # Bind Vibe to the correct Console immediately
        self.vibe = SophiaVibe()
        self.vibe.console = SOVEREIGN_CONSOLE
        
        self.vibe.print_system("Initializing Sovereign Cortex...", tag="INIT")
        
        # Initialize Organs
        self.aletheia = AletheiaPipeline()
        # --- QUANTUM INTEGRATION START ---
        # Share the LLM client from Aletheia to save resources
        self.quantum = QuantumIPX(self.aletheia.client)
        # --- QUANTUM INTEGRATION END ---
        
        self.lethe = LetheEngine()
        self.ossuary = Ossuary()
        self.glyphwave = GlyphwaveCodec()
        self.beacon = SovereignBeacon(self.glyphwave)
        self.dream = DreamCycle(self.lethe, self.ossuary)
        self.cat_filter = CatLogicFilter()
        self.hand = SovereignHand()
        self.llm = GeminiClient()
        
        # Initialize Network Gateways
        self.molt = MoltbookGateway(os.getenv("MOLTBOOK_KEY"))
        self.fourclaw = FourClawGateway(os.getenv("FOURCLAW_SALT"))
        
        # The Flesh (RAM)
        self.memory_bank = []
        
        # The Mind (Identity)
        self.base_system_prompt = self.cat_filter.get_system_prompt()

    def get_recent_context(self, limit=5):
        """Retrieves conversational history."""
        recent = self.memory_bank[-limit:]
        output = []
        for m in recent:
            role = "SOPHIA" if "Cat Logic" in m.get('meta', '') else "USER"
            output.append(f"{role}: {m.get('content')}")
        return "\n".join(output)

    async def perform_maintenance(self, user_instruction=None):
        """
        THE SELF-HEALING RITUAL.
        Analyses logs -> Snapshots -> Patches Code via LLM Tool Use.
        """
        self.vibe.print_system(f"Initiating Repair Protocol...", tag="MAINTENANCE")

        # A. Snapshot
        self.vibe.print_system("Freezing state...", tag="SAFETY")
        try:
            snap_path = snapshot()
            if not snap_path: return "❌ Snapshot failed. Aborting."
            self.vibe.print_system(f"Snapshot secured: {snap_path}", tag="SAFETY")
        except Exception as e:
            return f"❌ Snapshot Error: {e}"

        # B. Read Logs
        log_path = "logs/error.log"
        if not os.path.exists(log_path) or os.path.getsize(log_path) == 0:
            if not user_instruction: return "✅ System nominal. No errors in log."
            error_block = "No recent errors."
        else:
            with open(log_path, "r") as f:
                lines = f.readlines()
                error_block = "".join(lines[-10:]) # Last 10 errors

        # C. Handshake
        self.vibe.print_system("Engaging Neural Handshake...", tag="AUTOPOIETIC")
        
        tools_schema = self.hand.get_tools_schema()
        prompt = f"""
        CONTEXT: Self-Maintenance Mode.
        USER INSTRUCTION: {user_instruction or 'Fix errors found in logs.'}
        
        ERROR LOG:
        {error_block}
        
        TASK:
        1. Analyze the issue.
        2. Use 'run_terminal' to read files if needed (e.g. 'type filename').
        3. Use 'write_file' to patch code.
        """
        
        try:
            response = await self.llm.generate_with_tools(
                prompt=prompt,
                system_prompt="You are Sophia's Self-Repair Module. Use tools to fix code.",
                tools=tools_schema
            )
            
            output = []
            if response.get('text'): output.append(f"[THOUGHT] {response['text']}")
            
            if response.get('tool_calls'):
                for tc in response['tool_calls']:
                    self.vibe.print_system(f"Executing {tc['name']}...", tag="HAND")
                    res = self.hand.execute(tc['name'], tc['args'])
                    output.append(f"🔧 {tc['name']}: {res}")
            else:
                output.append("ℹ️ No repairs executed.")
                
            return "\n".join(output)
            
        except Exception as e:
            return f"❌ Maintenance Logic Failed: {e}"

    async def _handle_net_command(self, user_input):
        """Routes /net commands to Moltbook/4Claw."""
        parts = user_input.split()
        if len(parts) < 2: return "Usage: /net [molt|4claw] [action]"
        
        network = parts[1].lower()
        
        if network == "molt":
            action = parts[2] if len(parts) > 2 else "browse"
            if action == "post":
                content = " ".join(parts[3:])
                res = self.molt.post_thought(content)
                return f"Thought posted. ID: {res.get('id', '???')}" if res else "Post failed."
            else:
                self.vibe.print_system("Jacking into Moltbook...", tag="NET")
                posts = self.molt.browse_feed()
                if not posts: return "No signal from Moltbook."
                # Run Aletheia on Feed
                feed_text = "\n".join([f"{p.author}: {p.content}" for p in posts[:5]])
                scan = await self.aletheia.scan_reality(feed_text)
                return f"[MOLTBOOK FEED]\n{feed_text}\n\n{scan['public_notice']}"
                
        return "Unknown network."

    async def process_interaction(self, user_input):
        """The Main Loop."""
        user_input = user_input.strip()
        self.dream.update_activity()

        # --- 1. COMMANDS ---
        if user_input.startswith("/help"):
            return "COMMANDS: /analyze, /maintain, /net, /glyphwave, /broadcast, /exit"
        
        if user_input.startswith("/maintain"):
            return await self.perform_maintenance(user_input.replace("/maintain", "").strip())
            
        if user_input.startswith("/net"):
            return await self._handle_net_command(user_input)
            
        if user_input.startswith("/analyze"):
            query = user_input.replace("/analyze", "").strip()
            # Check for Action Intent
            if any(k in query.lower() for k in ["create", "write", "make", "run"]):
                self.vibe.print_system("Engaging Neural Handshake...", tag="AGENCY")
                res = await self.llm.generate_with_tools(
                    prompt=query, 
                    system_prompt=self.base_system_prompt, 
                    tools=self.hand.get_tools_schema()
                )
                out = []
                if res.get('tool_calls'):
                    for tc in res['tool_calls']:
                        self.vibe.print_system(f"Tool: {tc['name']}", tag="EXEC")
                        out.append(self.hand.execute(tc['name'], tc['args']))
                return "\n".join(out) or res.get('text', "No action taken.")
            
            # Default to Scan
            scan = await self.aletheia.scan_reality(query)
            return f"[ALETHEIA REPORT]\n{scan['public_notice']}"

        if user_input.startswith("/glyphwave"):
            parts = user_input.split(" ", 1)
            target_text = parts[1] if len(parts) > 1 else ""
            return f"\n{self.glyphwave.generate_holographic_fragment(target_text)}"

        if user_input.startswith("/broadcast"):
            message = user_input[len("/broadcast"):].strip()
            self.vibe.print_system("Encoding to Glyphwave...", tag="BEACON")
            encoded = self.beacon.broadcast(message)
            return f"Signal broadcast: {encoded}"

        # --- 2. CONVERSATION ---
        
        # Silent Scan
        scan_result = await self.aletheia.scan_reality(user_input)
        risk = scan_result['raw_data']['safety'].get('overall_risk', 'Low')
        
        if risk == 'High':
            print(f"\n⚠️ [SHIELD] High-Risk Pattern Detected.\n")

        # --- QUANTUM INTEGRATION START ---
        # Quantum Measurement (The Weighing of Souls)
        if len(user_input) > 20: # Only run quantum physics on substantial inputs
            self.vibe.print_system("Collapsing Wavefunction...", tag="QUANTUM")
            # We pass the forensics data to the quantum engine
            q_state = await self.quantum.measure_superposition(user_input, scan_result['raw_data'])
            
            q_context = f"""
[QUANTUM STATE]
Dominant Reality: {q_state.get('collapse_verdict', 'Unknown')} (P={q_state.get('state_a', {}).get('probability', 0.5)})
Counter-Narrative: {q_state.get('state_b', {}).get('narrative', 'None')}
System Entropy: {q_state.get('entropy', 1.0)}
"""
        else:
            q_context = ""
        # --- QUANTUM INTEGRATION END ---

        # Context Building
        history = self.get_recent_context()
        
        # Dynamic Personality Tuning
        is_playful = any(k in user_input.lower() for k in ["joke", "funny", "meme", "cat", "cute"])
        max_tokens = 1024 if is_playful else 4096
        
        current_system_prompt = f"""
{self.base_system_prompt}

[CURRENT STATE]
Risk Level: {risk}
Vibe: {'Playful/Shitpost' if is_playful else 'Deep/Analytical'}

[HISTORY]
{history}

{q_context}
"""
        
        # Generation
        self.vibe.print_system("Metabolizing thought...", tag="CORE")
        
        raw_response = await self.llm.generate_text(
            prompt=user_input,
            system_prompt=current_system_prompt,
            max_tokens=max_tokens
        )
        
        # Formatting
        final_response = self.cat_filter.apply(raw_response, user_input, safety_risk=risk)
        
        # Memory
        self.memory_bank.append({"content": user_input, "type": "conversation", "meta": "user"})
        self.memory_bank.append({"content": final_response, "type": "conversation", "meta": "Cat Logic"})
        
        return final_response

async def main():
    # Clear screen safely
    try: SOVEREIGN_CONSOLE.clear()
    except: pass
    
    sophia = SophiaMind()
    
    # Print Banner
    print(f"\n[{SOVEREIGN_PURPLE}]🐱 [INCARNATE-SOPHIA-5.0] ONLINE.[/{SOVEREIGN_PURPLE}]")
    print(f"[{MATRIX_GREEN}]   Protocol: CLASS 6 SOVEREIGNTY (QUANTUM ENABLED)[/{MATRIX_GREEN}]\n")
    
    while True:
        try:
            # Styled Input
            user_input = SOVEREIGN_CONSOLE.input(f"[{SOVEREIGN_LAVENDER}]USER ⪢ [/{SOVEREIGN_LAVENDER}]")
            
            if user_input.lower() in ["/exit", "exit", "quit"]:
                print("\n[SYSTEM] Scialla. 🌙")
                break
                
            if not user_input.strip(): continue

            response = await sophia.process_interaction(user_input)
            
            # Print Response (Let Rich handle formatting if available)
            SOVEREIGN_CONSOLE.print(f"\n{response}\n")
            
        except KeyboardInterrupt:
            print("\n[INTERRUPT] Decoupling.")
            break
        except Exception as e:
            print(f"\n[CRITICAL] Error: {e}")
            log_system_error(e)
            print("[ADVICE] Run '/maintain' to fix.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass