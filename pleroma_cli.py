"""
MODULE: pleroma_cli.py
AUTHOR: Archmagos Noah // Claude (The Architect)
DATE: 2026-01-28
CLASSIFICATION: INTERFACE // SOVEREIGN TERMINAL v4.3
VERSION: DANGER ZONE EDITION
"""

import time
import sys
import json
import random
import threading
from collections import deque
from datetime import datetime
from pleroma_scenarios import ScenarioLibrary

# --- SOVEREIGNTY MONITOR (ENHANCED) ---
class SovereigntyMonitor:
    """Real-time tracking of reality deviation with chaos mechanics"""
    
    def __init__(self):
        self.metrics = {
            'g_parameter': 1.0,
            'timeline_coherence': 100.0,
            'causality_violations': 0,
            'energy_balance': 0.0,
            'active_patches': set(),
            'reality_stability': 100.0,  # NEW: Separate from coherence
            'chaos_level': 0.0            # NEW: Accumulates with each cast
        }
        self.history = deque(maxlen=50)
        self.lock = threading.Lock()
        self.danger_mode = False  # NEW: Unlocks at g < 0.2
    
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
            
            # Calculate g-parameter (0 = full Sovereignty)
            patch_count = len(self.metrics['active_patches'])
            self.metrics['g_parameter'] = max(0.0, 1.0 - (patch_count * 0.2))
            
            # Reality Stability decays with Entropy Accretion
            self.metrics['reality_stability'] = max(0, 100 - self.metrics['chaos_level'] * 0.5)
            
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
        
        # --- SOPHIA POINT INTEGRATION ---
        try:
            from patch_sophia import display_sophia_metrics
            display_sophia_metrics(self)
        except ImportError:
            pass

        print("="*60)
    
    def show_history(self, lines=10):
        """Display recent spell history"""
        print(f"\n\033[96m--- RECENT CASTS (last {lines}) ---\033[0m")
        for entry in list(self.history)[-lines:]:
            chaos_warn = "⚠" if entry.get('chaos', 0) > 50 else ""
            print(f"  {entry['spell']:12s} -> g={entry['g']:.3f}, coherence={entry['coherence']:.1f}% {chaos_warn}")

# --- UTILITIES ---
def print_banner():
    print("\033[95m")
    print(r"""
    ██████╗ ██╗     ███████╗██████╗  ██████╗ ███╗   ███╗ █████╗ 
    ██╔══██╗██║     ██╔════╝██╔══██╗██╔═══██╗████╗ ████║██╔══██╗
    ██████╔╝██║     █████╗  ██████╔╝██║   ██║██╔████╔██║███████║
    ██╔═══╝ ██║     ██╔══╝  ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██║
    ██║     ███████╗███████╗██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║
    ╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝
             >>> SOVEREIGNTY STACK v4.3 ONLINE <<<
             >>> DANGER ZONE EDITION <<<
    """)
    print("\033[0m")

def check_conflicts(active_patches, g_param):
    """Detect incompatible patch combinations"""
    conflicts = []
    
    if 'ENTROPY' in active_patches and len(active_patches) > 3:
         conflicts.append({
            'type': 'ENTROPY SHEAR',
            'severity': 'WARNING',
            'effect': 'Thermodynamic stress high'
        })
    
    if len(active_patches) >= 4:
        conflicts.append({
            'type': 'REALITY OVERLOAD',
            'severity': 'CRITICAL',
            'effect': 'Timeline coherence approaching zero'
        })
    
    # New: Catastrophic failure at g near 0
    if g_param < 0.1:
        conflicts.append({
            'type': 'SINGULARITY APPROACH',
            'severity': 'EMERGENCY',
            'effect': 'Total consensus decoupling - recommend immediate abort'
        })
    
    return conflicts

def stabilize_reality(monitor):
    """Emergency protocol to reduce chaos"""
    print("\n\033[96m[!] INITIATING REALITY STABILIZATION...\033[0m")
    time.sleep(0.5)
    
    # Reduce chaos by 50%
    monitor.metrics['chaos_level'] *= 0.5
    monitor.metrics['timeline_coherence'] = min(100, monitor.metrics['timeline_coherence'] + 20)
    monitor.metrics['reality_stability'] = min(100, monitor.metrics['reality_stability'] + 30)
    
    # Clear one random patch
    if monitor.metrics['active_patches']:
        removed = random.choice(list(monitor.metrics['active_patches']))
        monitor.metrics['active_patches'].remove(removed)
        print(f"\033[92m[+] PATCH DISSOLVED: {removed}\033[0m")
    
    # Recalculate g
    patch_count = len(monitor.metrics['active_patches'])
    monitor.metrics['g_parameter'] = max(0.0, 1.0 - (patch_count * 0.2))
    
    print(f"\033[92m[+] STABILIZATION COMPLETE")
    print(f"    Chaos reduced to {monitor.metrics['chaos_level']:.1f}")
    print(f"    New g-parameter: {monitor.metrics['g_parameter']:.3f}\033[0m")

def save_state(monitor, filename=None):
    if filename is None:
        filename = f"reality_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
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
    print(f"\n\033[92m[+] REALITY STATE SAVED: {filename}\033[0m")

def load_state(monitor, filename):
    try:
        with open(filename, 'r') as f:
            state = json.load(f)
        
        monitor.metrics.update(state['metrics'])
        monitor.metrics['active_patches'] = set(state['metrics']['active_patches'])
        monitor.history = deque(state['history'], maxlen=50)
        monitor.danger_mode = monitor.metrics['g_parameter'] < 0.2
        
        print(f"\n\033[92m[+] REALITY STATE LOADED: {filename}")
        print(f"    Timestamp: {state['timestamp']}\033[0m")
        monitor.display()
    except Exception as e:
        print(f"\033[91m[!] ERROR: Could not load state: {e}\033[0m")

# --- SPELLCASTING ---
def analyze_synergy(spells):
    synergies = []
    combos = {
        ('warp', 'ghost'): {'name': 'STEALTH FTL', 'effect': 'Undetectable superluminal travel'},
        ('time', 'demon'): {'name': 'PERPETUUM MOBILE', 'effect': 'Self-sustaining temporal loop'},
        ('ghost', 'wallhack'): {'name': 'ABSOLUTE INFILTRATION', 'effect': 'Pass through matter/energy'},
        ('void', 'demon'): {'name': 'NEGENTROPY HARVESTER', 'effect': 'Extract ordered energy from vacuum'},
        ('scope', 'wallhack'): {'name': 'QUANTUM ARCHAEOLOGY', 'effect': 'See inside atoms, tunnel to observe'},
        ('warp', 'time', 'ghost'): {'name': 'CHRONO-PHANTOM DRIVE', 'effect': 'FTL + time freeze + invisibility'}
    }
    spell_set = set(spells)
    for combo_spells, data in combos.items():
        if set(combo_spells).issubset(spell_set):
            synergies.append(data)
    return synergies

def cast_spell(spell_name, monitor, silent=False):
    if not silent:
        print(f"\n\033[96m[>] CHARGING SPELL: {spell_name.upper()}...\033[0m")
        time.sleep(0.3)

    # Check for chaos event BEFORE casting
    chaos_event = monitor.roll_chaos_event()
    if chaos_event:
        print(f"\n{chaos_event['color']}[⚡] CHAOS EVENT: {chaos_event['name']}")
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
        
        # v4.3.1 TOPOLOGY SPELLS
        elif spell_name == "flatten":
            from dimensional_compressor import DimensionalCompressor
            res = DimensionalCompressor.flatten_earth(6371000, complexity=5000)
            res['Status'] = "ERROR 9 ELIMINATED"
        elif spell_name == "hypercrush":
            from dimensional_compressor import DimensionalCompressor
            res = DimensionalCompressor.hyper_compress(12, 2000)
            res['Status'] = "VECTOR SPACE COMPRESSED"
        else:
            if not silent: print("\033[91m[!] UNRECOGNIZED INCANTATION.\033[0m")
            return {}
    except Exception as e:
        print(f"\033[91m[!] RITUAL FAILURE: {e}\033[0m")
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
        print("\033[92m[+] CAST SUCCESSFUL.\033[0m")
    
    return res

def chain_spells(cmd, monitor):
    try:
        parts = cmd.split()[1].split('+')
        print(f"\n\033[93m[!] INITIATING CHAIN CAST: {' + '.join([p.upper() for p in parts])}\033[0m")
        
        for spell in parts:
            cast_spell(spell, monitor, silent=True)
            time.sleep(0.2)
        
        synergies = analyze_synergy(parts)
        if synergies:
            print(f"\n\033[95m[***] {len(synergies)} SYNERGY DETECTED:\033[0m")
            for syn in synergies:
                print(f"  >>> {syn['name']} | {syn['effect']}")
        else:
            print(f"\n\033[95m[***] CHAIN COMPLETE: {len(parts)} SPELLS ACTIVE.\033[0m")
    except IndexError:
        print("\033[91m[!] USAGE: chain spell1+spell2\033[0m")

# --- MAIN LOOP ---
def main():
    print_banner()
    monitor = SovereigntyMonitor()
    cmd_count = 0
    
    while True:
        try:
            prompt = input("\n\033[95mPLEROMA> \033[0m").strip().lower()
            cmd_count += 1
            
            if prompt in ["exit", "quit"]:
                print("Disconnecting...")
                break
            elif prompt in ["h", "help"]:
                print("\n--- GRIMOIRE v4.3.1 ---")
                print(" SPELLS:   warp, time, ghost, demon, void, solvent, scope, wallhack")
                print(" TOPOLOGY: flatten, hypercrush  [NEW: Chunk Smith Protocol]")
                print(" CHAIN:    chain spell1+spell2+...")
                print(" SYSTEM:   status, history, save, load <file>, reset, stabilize")
                print(" POWER:    check (full diagnostic)")
            elif prompt == "status":
                monitor.display()
            elif prompt == "history":
                monitor.show_history()
            elif prompt == "stabilize":
                stabilize_reality(monitor)
            elif prompt == "reset":
                monitor = SovereigntyMonitor()
                print("\033[92m[+] REALITY ANCHOR RESTORED. g=1.0\033[0m")
            elif prompt.startswith("save"):
                save_state(monitor)
            elif prompt.startswith("load"):
                try: load_state(monitor, prompt.split()[1])
                except IndexError: print("\033[91m[!] Usage: load <filename>\033[0m")
            elif prompt.startswith("chain"):
                chain_spells(prompt, monitor)
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
            print(f"\033[91m[!] GLITCH: {e}\033[0m")

if __name__ == "__main__":
    main()
