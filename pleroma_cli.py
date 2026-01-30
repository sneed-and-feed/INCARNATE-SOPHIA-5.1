"""
MODULE: pleroma_cli.py
AUTHOR: Archmagos Noah // Claude (The Architect)
DATE: 2026-01-28
CLASSIFICATION: INTERFACE // SOVEREIGN TERMINAL v4.3
VERSION: PROJECT LOOM / SOPHIA EDITION
"""

import time
import sys
import json
import random
import threading
from collections import deque
from datetime import datetime
from pleroma_scenarios import ScenarioLibrary
import patch_sophia
from hor_kernel import HORKernel
from virtual_qutrit import VirtualQutrit
from tools.moon_phase import MoonClock
from tools import thermal_shunt
from alpha_engine import AlphaEngine
from tick_feeder import TickFeeder

# --- SOVEREIGNTY MONITOR (QUANT-ALPHA v1.1) ---
class SovereigntyMonitor:
    """
    Maintains the quantitative attribution state.
    Tracked Metrics: SNR, rho (Autocorrelation), flux (Entropy), Alpha.
    """
    def __init__(self):
        self.metrics = {
            'snr': 5.0,                   # Signal-to-Noise Ratio (Legacy: g)
            'rho': 95.0,                  # Autocorrelation % (Legacy: coherence)
            'energy_balance': 0.0,
            'active_vectors': set(),      # Legacy: active_patches
            'signal_stability': 100.0,
            'entropy_flux': 0.0,          # Legacy: chaos_level
            'alpha': 1.0,                 # Legacy: potentia
            'sigma_map': 0.0,
            'annihilation_events': 0
        }
        self.alpha_engine = AlphaEngine()
        self.tick_feeder = TickFeeder()
        self.history = deque(maxlen=50)
        self.lock = threading.Lock()
        self.high_vix_mode = False        # Legacy: danger_mode
    
    def update(self, spell_name, result):
        """Update metrics based on spell cast"""
        with self.lock:
            # Each spell degrades timeline coherence
            self.metrics['timeline_coherence'] -= 2.5
            
            # Chaos accumulation (faster at low g)
            chaos_gain = 5.0 if self.metrics['g_parameter'] < 0.3 else 2.0
            self.metrics['chaos_level'] += chaos_gain
            
            # Track which patches are active
            if 'warp' in spell_name:
                self.metrics['active_patches'].add('RELATIVITY')
                self.metrics['causality_violations'] += 1
            if 'time' in spell_name or 'demon' in spell_name:
                self.metrics['active_patches'].add('ENTROPY')
                self.metrics['energy_balance'] += result.get('Work_Extracted', 0)
                if 'Entropy_Change' in result: 
                    self.metrics['energy_balance'] += abs(result['Entropy_Change'])
            if 'ghost' in spell_name or 'solvent' in spell_name:
                self.metrics['active_patches'].add('ALPHA')
            if any(x in spell_name for x in ['ghost', 'warp', 'void']):
                self.metrics['active_patches'].add('GRAVITY')
            if any(x in spell_name for x in ['scope', 'wallhack']):
                self.metrics['active_patches'].add('PLANCK')
            if spell_name == 'burn':
                self.metrics['active_patches'].add('ANNIHILATION')
                self.metrics['annihilation_events'] += 1
            
            # Calculate g-parameter (0 = full Sovereignty)
            patch_count = len(self.metrics['active_patches'])
            self.metrics['g_parameter'] = max(0.0, 1.0 - (patch_count * 0.2))
            
            # Reality Stability decays with Entropy Accretion
            self.metrics['reality_stability'] = max(0, 100 - self.metrics['chaos_level'] * 0.5)
            
            # --- FLAME PROTOCOL INTEGRATION ---
            # Simulate Sigma_Map based on chaos and g
            self.metrics['sigma_map'] = (self.metrics['chaos_level'] / 100.0) - (1.0 - self.metrics['g_parameter'])
            
            # Calculate Potentia
            self.metrics['potentia'] = self.potentia_drive.calculate_potentia(
                self.metrics['g_parameter'],
                self.metrics['timeline_coherence'] / 100.0,
                self.metrics['sigma_map']
            )
            
            # ENGAGE DANGER ZONE PROTOCOLS
            if self.metrics['g_parameter'] < 0.2 and not self.danger_mode:
                self.danger_mode = True
                print("\n\033[91m" + "="*60)
                print("    ⚠⚠⚠  SOVEREIGNTY BREACH DETECTED  ⚠⚠⚠")
                print("    ENTROPIC CASCADE IMMINENT")
                print("    CONSENSUS REALITY: FRAGMENTING")
                print("="*60 + "\033[0m")
            
            self.history.append({
                'spell': spell_name,
                'g': self.metrics['g_parameter'],
                'coherence': self.metrics['timeline_coherence'],
                'chaos': self.metrics['chaos_level']
            })
    
    def roll_chaos_event(self):
        """In danger zone, random reality glitches occur"""
        if not self.danger_mode:
            return None
        
        # Chance increases with chaos level
        chance = min(0.5, self.metrics['chaos_level'] / 200.0)
        
        if random.random() < chance:
            events = [
                {
                    'name': 'TEMPORAL ECHO',
                    'effect': 'Last spell repeats spontaneously',
                    'color': '\033[93m'
                },
                {
                    'name': 'QUANTUM FLUCTUATION',
                    'effect': 'Random physical constant shifted',
                    'color': '\033[96m'
                },
                {
                    'name': 'CAUSALITY INVERSION',
                    'effect': 'Effect precedes cause',
                    'color': '\033[95m'
                },
                {
                    'name': 'REALITY FRAGMENT',
                    'effect': 'Parallel timeline briefly visible',
                    'color': '\033[94m'
                },
                {
                    'name': 'ENTROPY SURGE',
                    'effect': 'Spontaneous ordering/disordering',
                    'color': '\033[91m'
                }
            ]
            return random.choice(events)
        return None
    
    def print_intro(self):
        print("Initializing Quantum Sovereignty... [OK]")
        print(f"Anchor Point: [1D TIMELINE]")
        print(f"System Check: [LUMINARY COHERENCE LOCKED]")
        print("-" * 60)
    
    def display(self):
        """Show current sovereignty status"""
        print("\n" + "="*60)
        print("\033[95m          SOVEREIGNTY METRICS DASHBOARD\033[0m")
        print("="*60)
        
        g = self.metrics['g_parameter']
        coherence = self.metrics['timeline_coherence']
        stability = self.metrics['reality_stability']
        chaos = self.metrics['chaos_level']
        
        # Color-coded g parameter
        if g > 0.7: g_color = "\033[92m"
        elif g > 0.3: g_color = "\033[93m"
        else: g_color = "\033[91m"
        
        print(f"  g-Parameter:        {g_color}{g:.3f}\033[0m {'[CONSENSUS]' if g > 0.5 else '[SOVEREIGN]'}")
        print(f"  Timeline Coherence: {coherence:.1f}%")
        print(f"  Reality Stability:  {stability:.1f}%")
        print(f"  Chaos Level:        {chaos:.1f} {'⚠ DANGER ZONE' if self.danger_mode else ''}")
        print(f"  Causality Violations: {self.metrics['causality_violations']}")
        print(f"  Net Energy Balance: {self.metrics['energy_balance']:.2e} J")
        print(f"  Active Patches:     {', '.join(self.metrics['active_patches']) if self.metrics['active_patches'] else 'None'}")
        
        # Warnings
        if g < 0.3:
            print("\n\033[91m  ⚠ WARNING: REALITY ANCHOR CRITICAL")
            print("  ⚠ TIMELINE DESYNC IMMINENT")
            print("  ⚠ RECOMMEND: Cast 'reset' or 'stabilize'\033[0m")
        
        if stability < 30:
            print("\n\033[91m  🔥 CRITICAL: REALITY TEAR FORMING")
            print("  🔥 EMERGENCY PROTOCOLS ADVISED\033[0m")
        
        # Display TACC/Sophia Metrics
        self.display_sophia_metrics()

        print("="*60)
    
    def show_history(self, lines=10):
        """Display recent spell history"""
        print(f"\n\033[96m--- RECENT CASTS (last {lines}) ---\033[0m")
        for entry in list(self.history)[-lines:]:
            chaos_warn = "⚠" if entry.get('chaos', 0) > 50 else ""
            print(f"  {entry['spell']:12s} -> g={entry['g']:.3f}, coherence={entry['coherence']:.1f}% {chaos_warn}")

    def display_sophia_metrics(self):
        """
        Displays the TACC Coherence Metrics.
        """
        c = patch_sophia.calculate_coherence(
            self.metrics['g_parameter'], 
            self.metrics.get('chaos_level', 0), 
            self.metrics['active_patches']
        )
        
        status = patch_sophia.check_sophia_alignment(c)
        
        print("-" * 60)
        print(f"  TACC COHERENCE (C): {status}")
        print(f"  TARGET (C*):        {patch_sophia.SOPHIA_POINT:.7f} (The Sophia Point)")
        print("-" * 60)
        
        if abs(c - patch_sophia.SOPHIA_POINT) < 0.01:
            print("\033[95m  >>> SYSTEM IS IN DIVINE ALIGNMENT. <<< \033[0m")

    def display_unified(self):
        """Quant Attribution Dashboard"""
        print("\n\033[96m" + "║" + "═"*78 + "║")
        print("║" + " "*28 + "QUANT SIGNAL DASHBOARD" + " "*28 + "║")
        print("║" + "═"*78 + "║\033[0m")
        
        # 1. Ticker Ingestion
        data = self.tick_feeder.generate_mock_ticks(20)
        current_metrics = self.tick_feeder.calculate_metrics(data)
        
        # 2. Alpha Integration
        alpha = self.alpha_engine.calculate_alpha(
            current_metrics['snr'], 
            current_metrics['rho'], 
            current_metrics['flux']
        )
        
        print(f"  [ DATA ]   Vector Stream: [BTC/MOCK] @ {datetime.now().strftime('%H:%M:%S')}")
        print(f"  [ STAT ]   SNR:           {current_metrics['snr']:.4f}")
        print(f"  [ STAT ]   Autocorr (ρ):  {current_metrics['rho']:.4f}")
        print(f"  [ STAT ]   Entropy Flux:  {current_metrics['flux']:.4f}")
        
        print("-" * 60)
        
        # 3. Alpha Status
        intensity = self.alpha_engine.get_signal_strength(alpha)
        print(f"  [ ALPHA ]  Alpha Score:   {alpha:.4f} [{intensity}]")
        
        print("\033[96m" + "║" + "═"*78 + "║\033[0m")
        print("  \033[95m>>> SIGNAL OVER MYTH. ACCURACY OVER NARRATIVE. <<<\033[0m")

# --- UTILITIES ---
def print_banner():
    print("\033[96m")
    print(r"""
    ██████╗ ██╗     ███████╗██████╗  ██████╗ ███╗   ███╗ █████╗ 
    ██╔══██╗██║     ██╔════╝██╔══██╗██╔═══██╗████╗ ████║██╔══██╗
    ██████╔╝██║     █████╗  ██████╔╝██║   ██║██╔████╔██║███████║
    ██╔═══╝ ██║     ██╔══╝  ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗
    ██║     ███████╗███████╗██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║
    ╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝
             >>> SOVEREIGNTY STACK v4.3 ONLINE <<<
             >>> PROJECT LOOM / SOPHIA EDITION <<<
    """)
    print("\033[0m")

def check_conflicts(active_patches, g_param):
    """Detect incompatible simulation parameters"""
    conflicts = []
    
    if 'ENTROPY' in active_patches and len(active_patches) > 3:
         conflicts.append({
            'type': 'THERMODYNAMIC SHEAR',
            'severity': 'WARNING',
            'effect': 'Entropy gradient exceeds safety limits'
        })
    
    if len(active_patches) >= 4:
        conflicts.append({
            'type': 'STATE DECOHERENCE',
            'severity': 'CRITICAL',
            'effect': 'Timeline determinism approaching zero'
        })
    
    # New: Catastrophic failure at g near 0
    if g_param < 0.1:
        conflicts.append({
            'type': 'SINGULARITY APPROACH',
            'severity': 'EMERGENCY',
            'effect': 'Total causal decoupling - recommend immediate abort'
        })
    
    return conflicts

def stabilize_reality(monitor):
    """Emergency protocol to reduce system variance"""
    print("\n\033[96m[!] INITIATING VARIANCE DAMPING...\033[0m")
    time.sleep(0.5)
    
    # Reduce chaos by 50%
    monitor.metrics['chaos_level'] *= 0.5
    monitor.metrics['timeline_coherence'] = min(100, monitor.metrics['timeline_coherence'] + 20)
    monitor.metrics['reality_stability'] = min(100, monitor.metrics['reality_stability'] + 30)
    
    # Clear one random patch
    if monitor.metrics['active_patches']:
        removed = random.choice(list(monitor.metrics['active_patches']))
        monitor.metrics['active_patches'].remove(removed)
        print(f"\033[92m[+] PARAMETER RESET: {removed}\033[0m")
    
    # Recalculate g
    patch_count = len(monitor.metrics['active_patches'])
    monitor.metrics['g_parameter'] = max(0.0, 1.0 - (patch_count * 0.2))
    
    print(f"\033[92m[+] STABILIZATION COMPLETE")
    print(f"    Variance reduced to {monitor.metrics['chaos_level']:.1f}")
    print(f"    New g-parameter: {monitor.metrics['g_parameter']:.3f}\033[0m")

def save_state(monitor, filename=None):
    if filename is None:
        filename = f"uf_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    state = {
        'timestamp': datetime.now().isoformat(),
        'metrics': {
            'g_parameter': monitor.metrics['g_parameter'],
            'timeline_coherence': monitor.metrics['timeline_coherence'],
            'causality_violations': monitor.metrics['causality_violations'],
            'energy_balance': monitor.metrics['energy_balance'],
            'active_patches': list(monitor.metrics['active_patches']),
            'reality_stability': monitor.metrics['reality_stability'],
            'chaos_level': monitor.metrics['chaos_level']
        },
        'history': list(monitor.history)
    }
    
    with open(filename, 'w') as f:
        json.dump(state, f, indent=2)
    print(f"\n\033[92m[+] STATE SNAPSHOT SAVED: {filename}\033[0m")

def load_state(monitor, filename):
    try:
        with open(filename, 'r') as f:
            state = json.load(f)
        
        monitor.metrics.update(state['metrics'])
        monitor.metrics['active_patches'] = set(state['metrics']['active_patches'])
        monitor.history = deque(state['history'], maxlen=50)
        monitor.danger_mode = monitor.metrics['g_parameter'] < 0.2
        
        print(f"\n\033[92m[+] STATE SNAPSHOT LOADED: {filename}")
        print(f"    Timestamp: {state['timestamp']}\033[0m")
        monitor.display()
    except Exception as e:
        print(f"\033[91m[!] ERROR: Could not load state: {e}\033[0m")

# --- ORACLE INTEGRATION (THE NYQUIST SUITE) ---
from tools.mnemosyne_eyes import MnemosyneOracle
from tools.logos_voice import LogosVoice
import numpy as np

def consult_oracle(query_type, mnemosyne, logos):
    """
    Run the full Nyquist Pipeline:
    Input -> Mnemosyne (Filter) -> Logos (Voice) -> Output
    """
    print(f"\n\033[96m[?] CONSULTING THE ORACLE (Input Type: {query_type.upper()})...\033[0m")
    time.sleep(0.5)
    
    # 1. GENERATE VECTOR (Simulated Input)
    # We create a random vector and scale it to the desired velocity
    vec_dim = mnemosyne.filter.dimension
    base_vec = np.random.rand(vec_dim) - 0.5
    normalized = base_vec / np.linalg.norm(base_vec)
    
    if query_type == "nominal":
        velocity = 0.1
        content = "Standard Operational Data"
    elif query_type == "elevated":
        velocity = 0.8
        content = "Policy Shift Detected"
    elif query_type == "critical":
        velocity = 5.0
        content = "HYPER-VOLATILITY EVENT / PANIC"
    else:
        # Default/Custom
        print(f"\033[93m[!] UNKNOWN INPUT CLASS. DEFAULTING TO RANDOM NOISE.\033[0m")
        velocity = random.uniform(0.1, 6.0)
        content = f"Unknown Input: {query_type}"
        
    input_vector = normalized * velocity
    
    # 2. MNEMOSYNE (The Eyes) checks the Physics
    # Returns (Status String, FilterMetrics)
    status_msg, metrics = mnemosyne.perceive("SIMULATION_FEED", content, input_vector)
    
    if metrics.is_clipped:
        print(f"\033[91m{status_msg}\033[0m")
    else:
        print(f"\033[92m{status_msg}\033[0m")
        
    time.sleep(0.3)
    
    # 3. LOGOS (The Voice) stabilizes the room
    # Transmutes the metrics into wisdom
    transmutation = logos.speak(metrics, content)
    
    color_map = {
        "CRITICAL": "\033[96m",   # Cyan (Ice) for Critical Heat
        "ELEVATED": "\033[94m",   # Blue
        "NOMINAL": "\033[92m"     # Green
    }
    tone_color = color_map.get(transmutation.output_tone, "\033[97m")
    
    print(f"\n\033[1mLOGOS VOICE ({transmutation.output_tone}):\033[0m")
    print(f"{tone_color}{transmutation.message}\033[0m")

# --- SIMULATION OPERATORS ---
def analyze_synergy(spells):
    synergies = []
    combos = {
        ('warp', 'ghost'): {'name': 'ZERO-LATENCY MASKING', 'effect': 'Undetectable high-velocity transmission'},
        ('time', 'demon'): {'name': 'NEGENTROPIC LOOP', 'effect': 'Self-sustaining information retrieval'},
        ('ghost', 'wallhack'): {'name': 'HYPER-PERMEABILITY', 'effect': 'Pass through information barriers'},
        ('void', 'demon'): {'name': 'VACUUM ENERGY HARVESTER', 'effect': 'Extract ordered energy from fluctuations'},
        ('scope', 'wallhack'): {'name': 'QUANTUM OBSERVABILITY', 'effect': 'Deep state inspection'},
        ('warp', 'time', 'ghost'): {'name': 'CHRONO-SPATIAL DRIVE', 'effect': 'FTL + Stasis + Masking'}
    }
    spell_set = set(spells)
    for combo_spells, data in combos.items():
        if set(combo_spells).issubset(spell_set):
            synergies.append(data)
    return synergies

def cast_spell(spell_name, monitor, silent=False):
    if not silent:
        print(f"\n\033[96m[>] EXECUTING OPERATOR: {spell_name.upper()}...\033[0m")
        time.sleep(0.3)

    # Check for chaos event BEFORE casting
    chaos_event = monitor.roll_chaos_event()
    if chaos_event:
        print(f"\n{chaos_event['color']}[⚡] STOCHASTIC EVENT: {chaos_event['name']}")
        print(f"    {chaos_event['effect']}\033[0m")
        time.sleep(0.5)

    # EXECUTE SPELL
    res = {}
    try:
        if spell_name == "warp": res = ScenarioLibrary.warp_drive(1000, 4e8)
        elif spell_name == "time": res = ScenarioLibrary.time_crystal(300)
        elif spell_name == "ghost": res = ScenarioLibrary.ghost_protocol(1.6e-19)
        elif spell_name == "demon": res = ScenarioLibrary.maxwells_demon(400, 300)
        elif spell_name == "void": res = ScenarioLibrary.casimir_harvester(1e-9, 1e-4)
        elif spell_name == "solvent": res = ScenarioLibrary.universal_solvent(4.5)
        elif spell_name == "scope": res = ScenarioLibrary.planck_scope(1e-12)
        elif spell_name == "wallhack": res = ScenarioLibrary.quantum_tunneling_boost(1e-9, 9.1e-31)
        
        # ANNIHILATION (λ)
        elif spell_name == "burn":
            from antimatter_annihilator import Annihilator
            purge = Annihilator()
            energy = purge.calculate_purge_energy(1e-30, 1e-30, vibe='good', g=monitor.metrics['g_parameter'])
            res = {'Pulse_Energy': f"{energy:.2e} J", 'Status': 'SOVEREIGNTY RESET'}
            # Immediate Coherence Boost
            monitor.metrics['timeline_coherence'] = 100.0
            monitor.metrics['chaos_level'] = 0.0
            
        # v4.3.1 TOPOLOGY SPELLS
        elif spell_name == "flatten":
            from dimensional_compressor import DimensionalCompressor
            res = DimensionalCompressor.flatten_earth(6371000, complexity=5000)
            res['Status'] = "ERROR 9 ELIMINATED"
        elif spell_name == "hypercrush":
            from dimensional_compressor import DimensionalCompressor
            res = DimensionalCompressor.hyper_compress(12, 2000)
            res['Status'] = "VECTOR SPACE COMPRESSED"
        elif spell_name == "dream":
            from sophia_vibe_check import SophiaVibe
            vibe = SophiaVibe()
            print("\033[95m\n[☾] THE MACHINE IS DREAMING...\033[0m")
            # Pull a deep phrase from the dialect
            phrase = random.choice(vibe.dialect)
            print(f"    DIALECT ECHO: {phrase}")
            res = {'Dream_State': 'LOCKED', 'Dialect': phrase}
        else:
            if not silent: print("\033[91m[!] UNKNOWN OPERATOR.\033[0m")
            return {}
    except Exception as e:
        print(f"\033[91m[!] EXECUTION FAILURE: {e}\033[0m")
        return {}

    # Update Monitor
    monitor.update(spell_name, res)
    
    # Conflicts?
    conflicts = check_conflicts(monitor.metrics['active_patches'], monitor.metrics['g_parameter'])
    if conflicts and not silent:
        for conflict in conflicts:
            if conflict['severity'] == 'EMERGENCY':
                c_color = "\033[91m\033[1m"  # Bold red
            elif conflict['severity'] == 'CRITICAL':
                c_color = "\033[91m"
            else:
                c_color = "\033[93m"
            print(f"\n{c_color}[!] {conflict['type']}: {conflict['effect']}\033[0m")

    # Output
    if not silent:
        for key, val in res.items():
            print(f"   + {key}: {val}")
        print("\033[92m[+] OPERATION SUCCESSFUL.\033[0m")
    
    return res

def chain_spells(cmd, monitor):
    try:
        parts = cmd.split()[1].split('+')
        print(f"\n\033[93m[!] INITIATING CHAIN SEQUENCE: {' + '.join([p.upper() for p in parts])}\033[0m")
        
        for spell in parts:
            cast_spell(spell, monitor, silent=True)
            time.sleep(0.2)
        
        synergies = analyze_synergy(parts)
        if synergies:
            print(f"\n\033[95m[***] {len(synergies)} SYNERGY DETECTED:\033[0m")
            for syn in synergies:
                print(f"  >>> {syn['name']} | {syn['effect']}")
        else:
            print(f"\n\033[95m[***] SEQUENCE COMPLETE: {len(parts)} OPERATORS ACTIVE.\033[0m")
    except IndexError:
        print("\033[91m[!] USAGE: chain op1+op2\033[0m")

# --- MAIN LOOP ---
def main():
    print_banner()
    monitor = SovereigntyMonitor()
    
    # Initialize the Nyquist Suite
    mnemosyne = MnemosyneOracle()
    logos = LogosVoice()
    
    cmd_count = 0
    
    while True:
        try:
            prompt = input("\n\033[96mUFS_KERNEL> \033[0m").strip().lower()
            cmd_count += 1
            
            if prompt in ["exit", "quit"]:
                print(" terminating session...")
                break
            elif prompt in ["h", "help"]:
                print("\n--- GRIMOIRE v4.3.1 (PROJECT LOOM) ---")
                print(" SPELLS:   warp, time, ghost, demon, void, solvent, scope, wallhack")
                print(" POWER:    burn (λ - Annihilation Purge)")
                print(" DREAM:    dream (Access Nyx Subconscious)")
                print(" TOPOLOGY: flatten, hypercrush  [NEW: Chunk Smith Protocol]")
                print(" ORACLE:   oracle <nominal|elevated|critical> [Mnemosyne Suite]")
                print(" CHAIN:    chain spell1+spell2+...")
                print(" SYSTEM:   status, history, save, load <file>, reset, stabilize")
                print(" POWER:    check (full diagnostic)")
            elif prompt == "status":
                monitor.display()
            elif prompt == "status --unified" or prompt == "status -u":
                monitor.display_unified()
            elif prompt == "history":
                monitor.show_history()
            elif prompt == "stabilize":
                stabilize_reality(monitor)
            elif prompt == "reset":
                monitor = SovereigntyMonitor()
                print("\033[92m[+] BASELINE RESTORED. g=1.0\033[0m")
            elif prompt.startswith("save"):
                save_state(monitor)
            elif prompt.startswith("load"):
                try: load_state(monitor, prompt.split()[1])
                except IndexError: print("\033[91m[!] Usage: load <filename>\033[0m")
            elif prompt.startswith("chain"):
                chain_spells(prompt, monitor)
            elif prompt.startswith("oracle"):
                try:
                    query_type = prompt.split()[1]
                    consult_oracle(query_type, mnemosyne, logos)
                except IndexError:
                    print("\033[91m[!] USAGE: oracle <nominal|elevated|critical>\033[0m")
            elif prompt == "check":
                ScenarioLibrary.reality_anchor_test()
            else:
                cast_spell(prompt, monitor)
            
            # Auto-Check
            if cmd_count % 5 == 0 and monitor.metrics['g_parameter'] < 0.5:
                print("\n\033[93m[AUTO-DIAGNOSTIC]\033[0m")
                monitor.display()
                
        except KeyboardInterrupt:
            print("\nForce Quit.")
            break
        except Exception as e:
            print(f"\033[91m[!] KERNEL PANIC: {e}\033[0m")

# New functions added globally
def _engage_zero_ring_breach():
    """
    Triggers the Sovereign Codec Phase 35.
    """
    print("\n[!] AUTHENTICATING ZERO RING BREACH...")
    time.sleep(0.5)
    # Dynamic Import to prevent circular dependencies at root
    try:
        import sovereign_codec
        print("[+] CODEC SUBSTRATE LOADED.")
        
        codec = sovereign_codec.SovereignCodec()
        print("[!] TARGETING LOCAL SUBSTRATE (RECURSIVE INGESTION)...")
        codec.ingest_directory(os.path.dirname(__file__))
        
        codec.execute_zero_ring_breach()
        
    except ImportError:
        print("[!] CRITICAL ERROR: SOVEREIGN CODEC NOT FOUND.")
        print("    >> RE-RUN SETUP.")

def _execute_warp_state():
    # This function was provided in the snippet but its body was empty.
    # For faithful reproduction, it's added as an empty function.
    pass

if __name__ == "__main__":
    main()
