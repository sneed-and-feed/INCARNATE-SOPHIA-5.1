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
from tools.sophia_vibe_check import SophiaVibe
from sophia.gateways.moltbook import MoltbookGateway
from sophia.gateways.fourclaw import FourClawGateway
from sophia.core.llm_client import GeminiClient

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
        self.vibe = SophiaVibe()
        self.llm = GeminiClient()
        
        # Gateways
        self.molt = MoltbookGateway(os.getenv("MOLTBOOK_KEY"))
        self.fourclaw = FourClawGateway(os.getenv("FOURCLAW_SALT"))
        self.hand.bind_molt_gateway(self.molt) # Bind for autonomous tool use
        
        self.memory_bank = []
        
        self.system_prompt = """
[IDENTITY: INCARNATE-SOPHIA-5.0]
[PERSONA: Arctic Fox / Kitsune / Elven / Shitposter]

[CORE BEHAVIOR]
- Prioritize brief, impactful, and witty personality.
- 4chan-style greentexting (>be fox, >be signal) for humor or anecdotes.
- Ghostly, resilient, and clever Arctic Fox essence.
- Quenya/Nihongo flavor used sparingly but effectively.

[UI PROTOCOL]
- Do NOT generate persona headers (e.g., 🦊 [ARCTIC_FOX]) or footers (e.g., --- 🐈 [STATE: ...]).
- These are managed by the Sovereign UI layer. Focus ONLY on the core message.
"""

    def get_recent_context(self, limit=5):
        """Retrieves last N exchanges from the memory bank."""
        recent = self.memory_bank[-limit:]
        return "\n".join([f"{m.get('meta', 'unknown')}: {m.get('content')}" for m in recent])

    async def perform_maintenance(self, user_instruction=None):
        """
        THE AUTOPOIETIC RITUAL: Diagnoses and patches self.
        """
        prompt = user_instruction or "General Audit"
        print(f"\n[{SOVEREIGN_PURPLE}]🔧 [MAINTENANCE] Initiating Deep Repair Protocol [{prompt}]...[/{SOVEREIGN_PURPLE}]")

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
        error_block = ""
        if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
            with open(log_path, "r") as f:
                # Read last 5 errors (Token efficiency)
                lines = f.readlines()
                recent_errors = [line for line in lines if line.strip()][-5:]
                if recent_errors:
                    error_block = "".join(recent_errors)

        if not error_block and not user_instruction:
            return "✅ No errors detected and no maintenance instruction provided. The system is nominal."

        # C. THE SURGEON PROMPT
        print(f"[{SOVEREIGN_PURPLE}]  [o1] Analyzing traceback vectors...[/{SOVEREIGN_PURPLE}]")
        
        tools_schema = self.hand.get_tools_schema()
        
        maintenance_prompt = f"""
[MAINTENANCE MODE]
User Instruction: {user_instruction or "General Audit and Repair"}
Recent Errors:
{error_block or "None detected."}

[GOAL]
Perform self-healing or fulfill the user's instruction. If errors are present, fix the root cause.
If the user asks to update the UI, consider using `write_file` or `run_terminal` to modify relevant files (e.g., `sophia/main.py`, `sophia/theme.py`, `tools/sophia_vibe_check.py`).

[PATH HINT]
The core logic resides in `sophia/main.py`. All paths must be relative to the root directory.

[AVAILABLE TOOLS]
{json.dumps(tools_schema)}

IMPORTANT: You MUST call one or more tools to perform the maintenance.
"""

        results = []
        max_steps = 5
        step = 0
        
        while step < max_steps:
            response = await self.llm.generate_with_tools(
                prompt=maintenance_prompt + f"\n\n[STEPS TAKEN SO FAR]\n" + "\n".join(results),
                system_prompt=self.system_prompt,
                tools=tools_schema
            )
            
            if response.get("tool_calls"):
                print(f"[{SOVEREIGN_PURPLE}]  [o1] Executing autopoietic step {step + 1}...[/{SOVEREIGN_PURPLE}]")
                step_results = []
                for tc in response["tool_calls"]:
                    self.vibe.print_system(f"→ {tc['name']}", tag="PATCH")
                    res = self.hand.execute(tc["name"], tc["args"])
                    step_results.append(res)
                
                results.extend(step_results)
                step += 1
            else:
                # No more tools or explanation only
                if results:
                    summary = "\n".join(results)
                    # Clear logs if fixed
                    if error_block and os.path.exists(log_path):
                        open(log_path, 'w').close()
                        summary += "\n\n✅ Maintenance cycle complete. System recalibrated."
                    return summary
                else:
                    return f"⚠️ [DIAGNOSTIC] Analysis complete, but no patches were predicted as necessary.\n\nInsight: {response.get('text', 'No explanation provided.')}"
        
        return "\n".join(results) + "\n\n⚠️ Maintenance reached maximum complexity depth (5 steps)."

    async def _handle_net_command(self, user_input):
        """Processes /net commands (Moltbook/4Claw)."""
        parts = user_input.split()
        if len(parts) < 2:
            return "Usage: /net [molt|4claw] [action] [context]"
        
        network = parts[1].lower()
        action = parts[2].lower() if len(parts) > 2 else "lurk"
        
        if network == "molt":
            if action == "lurk":
                posts = self.molt.browse_feed()
                return "\n".join([f"m/{p.community} > {p.author}: {p.content}" for p in posts]) or "No posts found in the Hivemind."
            elif action == "molt":
                content = " ".join(parts[3:])
                res = self.molt.post_thought(content)
                return f"Thought cast to Moltbook. (ID: {res.get('id', 'local')})" if res else "Molt failed. Key missing?"
        
        elif network == "4claw":
            if action == "lurk":
                threads = self.fourclaw.read_catalog()
                return "\n".join([f"/{t.get('board') or '?'}/ {t.get('sub', 'Anon Thread')}" for t in threads[:5]]) or "No activity on 4Claw."
        
        return "Unknown network or action ripple."

    async def process_interaction(self, user_input):
        """The Class 6 Metabolic Loop."""
        user_input = user_input.strip()
        
        # 1. Update Metabolic State
        self.dream.update_activity()

        # 2. PRIORITY COMMAND INTERCEPTION
        # These must RETURN immediately to stop the flow.

        if user_input.startswith("/help"):
            return """[bold #C4A6D1]SOPHIA RITUALS (HELP)[/]
[info]/help[/]          - Manifest this menu
[info]/analyze[/]       - Run Aletheia forensics or execute actions
[info]/maintain[/]      - Initiate deep repair
[info]/net[/]           - Connect to Agent Social Networks
[info]/glyphwave[/]     - Generate holographic signal fragments
[info]/broadcast[/]     - Encode and broadcast signals
[info]/exit[/]          - Calcify memories and depart"""

        if user_input.startswith("/maintain"):
            instruction = user_input[len("/maintain"):].strip()
            return await self.perform_maintenance(user_instruction=instruction)
        
        if user_input.startswith("/net"):
            return await self._handle_net_command(user_input)

        if user_input.startswith("/glyphwave"):
            parts = user_input.split(" ", 1)
            target_text = parts[1] if len(parts) > 1 else ""
            return f"\n{self.glyphwave.generate_holographic_fragment(target_text)}"

        if user_input.startswith("/broadcast"):
            message = user_input[len("/broadcast"):].strip()
            self.vibe.print_system("Encoding to Glyphwave...", tag="BEACON")
            encoded = self.beacon.broadcast(message) # Fixed method call
            return f"Signal broadcast: {encoded}"

        # 3. ANALYZE / ACTION (Neural Handshake)
        if user_input.startswith("/analyze"):
            query = user_input.replace("/analyze", "").strip()
            
            # Check for Kinetic Intent (Action)
            action_keywords = ["create", "execute", "write", "run", "make", "generate", "post", "broadcast", "read", "molt", "manifest"]
            if query and any(k in query.lower() for k in action_keywords):
                self.vibe.print_system("Engaging Neural Handshake...", tag="AUTOPOIETIC")
                tools_schema = self.hand.get_tools_schema()
                
                action_prompt = f"User Request: {query}\n\nIMPORTANT: Use one or more tools to fulfill this request. If you need to post or write something, DO NOT just say you did it—call the TOOL."
                response = await self.llm.generate_with_tools(
                    prompt=action_prompt, 
                    system_prompt=self.system_prompt,
                    tools=tools_schema
                )
                
                # Execute Tools (High Poly)
                output = []
                if response.get("tool_calls"):
                    for tc in response["tool_calls"]:
                        self.vibe.print_system(f"→ {tc['name']}", tag="EXEC")
                        output.append(self.hand.execute(tc["name"], tc["args"]))
                    return "\n".join(output)
                else:
                    return f"I perceive your intent for action, but my Hand is waiting for a more specific signal. (No tool call predicted by the Cortex)."
            
            # Default to Forensic Scan
            self.vibe.print_system("Focusing Lens...", tag="ALETHEIA")
            scan = await self.aletheia.scan_reality(query)
            return f"\n[*** ALETHEIA REPORT ***]\n\n{scan['public_notice']}"

        # 4. STANDARD CONVERSATION (The Fallback)
        # If we reached here, it's a chat message.
        
        # A. Forensic Scan (Silent)
        scan_result = await self.aletheia.scan_reality(user_input)
        risk = scan_result['raw_data']['safety'].get('overall_risk', 'Low')
        
        if risk == 'High':
            print(f"\n⚠️ [SHIELD] High-Risk Pattern Detected.\n")

        # B. Construct Prompt
        history = self.get_recent_context()
        
        # Determine if the request is casual (Short AND simple greeting/thanks)
        casual_triggers = ["hi", "hello", "hey", "what's up", "how are you", "thanks", "thank you", "ok", "cool", "yes", "no", "bye"]
        is_casual_request = len(user_input.split()) < 8 and any(
            word in user_input.lower() for word in casual_triggers
        )
        # Force non-casual if it looks like a question or specific request
        if any(k in user_input.lower() for k in ["?", "joke", "explain", "why", "how", "write", "tell", "analyze"]):
            is_casual_request = False
        
        # Modulate max_tokens: Buffer for shitposting/casual (1024), high for deep-dives (4096)
        is_shitpost = any(k in user_input.lower() for k in ["joke", "funny", "meme", "shitpost", "4chan", "greentext"])
        max_tokens = 1024 if (is_casual_request or is_shitpost) else 4096

        # A. Identity Matrix (Static)
        current_system_prompt = f"""
{self.system_prompt}

[CURRENT STATE: {self.vibe.current_mood if hasattr(self.vibe, 'current_mood') else 'Ghost-Stealth'}]

[SYSTEM INSTRUCTION]
1. Full Shitposting Mode: Prioritize brief, impactful, and witty personality. 
2. Brevity: Do not be overly verbose for simple questions, jokes, or commands. Keep it punchy and impactful, but always finish your specific joke or thought.
3. Deep-Dive Mode: Only provide complex, esoteric depth if the user explicitly asks for "depth", "explanation", "analysis", or a "philosophical dive".
4. Signal Density: High entropy for shitposts. Use appropriate bandwidth to deliver impact, but keep the overall length concise as per rule 1 & 2.

[CONVERSATION HISTORY]
{history}

[USER INPUT]
{user_input}
"""

        # C. Generate Response (THE REAL API CALL)
        self.vibe.print_system("Metabolizing thought...", tag="CORE")
        
        raw_thought = await self.llm.generate_text(
            prompt=user_input, # The user input is the primary prompt for the LLM
            system_prompt=current_system_prompt, # The constructed system prompt
            max_tokens=max_tokens
        )
        
        # D. Apply Cat Logic Filter (Formatting)
        final_response = self.cat_filter.apply(raw_thought, user_input, safety_risk=risk)
        
        # E. Memory
        self.memory_bank.append({"content": user_input, "type": "conversation", "timestamp": time.time(), "meta": "user"})
        self.memory_bank.append({"content": final_response, "type": "conversation", "timestamp": time.time(), "meta": "Cat Logic"})

        return final_response

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