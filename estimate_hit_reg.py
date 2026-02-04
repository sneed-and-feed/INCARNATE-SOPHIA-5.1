
import random
import math
from estimate_tarkov_lite import PrismEngineLite, vec_normalize, vec_dot

def estimate_hitreg():
    prism = PrismEngineLite()
    
    print("Optimization Target: HIT REGISTRATION & GHOST BULLETS")
    print("-" * 50)
    
    # Simulation: 20 shots fired in a spray
    # Common Tarkov issue: "Ghost Bullets" that vanish due to server disagreement
    shot_stream = [
        "hit", "hit", "hit", "ghost_bullet", "hit", 
        "server_reject", "hit", "hit", "miss", "hit",
        "ghost_bullet", "ghost_bullet", "hit", "hit", "hit",
        "desync_miss", "hit", "hit", "hit", "hit"
    ]
    
    # 1. BASELINE ANALYSIS (Vanilla Tarkov)
    # Ghost/Reject/Desync = MISS
    
    base_hits = 0
    base_misses = 0
    actual_misses = 0 # True misses (player error)
    
    for shot in shot_stream:
        if shot == "hit":
            base_hits += 1
        elif shot in ["miss", "desync_miss"]:
            # We count desync miss as a miss for the player in baseline
            base_misses += 1
            if shot == "miss": actual_misses += 1
        else:
            # Ghost/Reject -> effectively a miss
            base_misses += 1
            
    total_shots = len(shot_stream)
    base_reg_rate = (base_hits / total_shots) * 100.0
    
    print(f"[BASELINE STATISTICS]")
    print(f"Total Shots:      {total_shots}")
    print(f"Registered Hits:  {base_hits}")
    print(f"Lost/Ghost/Miss:  {base_misses}")
    print(f"Hit Reg Rate:     {base_reg_rate:.1f}%")

    # 2. SOPHIA 5.2 QUANTUM TUNNELING
    # The Prism Engine attempts to "collapse" the wave function of a Ghost Bullet
    # into a definitive "Hit" (Signal Anchor) if it was physically true on the client.
    
    print("\n[SOPHIA 5.2 REALITY COLLAPSE]")
    
    optimized_hits = 0
    salvaged_rounds = 0
    
    # We define vectors for the specific gunplay terms if not in default chaos map
    # We inject them into the prism instance for this sim
    prism.chaos_map["ghost_bullet"]  = [0.8, -0.2, 0.5] # Strange state
    prism.chaos_map["server_reject"] = [0.9, -0.9, 0.1] # Conflict
    prism.chaos_map["hit"]           = [0.95, 0.95, 0.0] # Perfect Signal
    prism.chaos_map["miss"]          = [0.0, 0.0, 0.9]   # Void
    prism.chaos_map["desync_miss"]   = [0.5, 0.5, 0.5]   # Uncertain
    
    results = prism.transform_phrase(" ".join(shot_stream))
    
    for original, anchor, resonance in results:
        # LOGIC:
        # If it anchors to 'signal' or 'orbit', the server accepts the truth (HIT).
        # If it anchors to 'void' or 'landing', it's a confirmed MISS.
        
        is_hit = False
        outcome = "MISS"
        
        if anchor in ['signal', 'orbit']:
            is_hit = True
            outcome = "HIT"
        elif anchor in ['void', 'landing', 'hold', 'wait']:
            is_hit = False
            outcome = "MISS"
            
        # Check if we salvaged a ghost bullet
        if original in ["ghost_bullet", "server_reject", "desync_miss"] and is_hit:
            outcome = "SALVAGED"
            salvaged_rounds += 1
            
        if is_hit:
            optimized_hits += 1
            
        print(f"Round: {original:<15} -> Collapse: {anchor.upper():<8} | {outcome}")

    opt_reg_rate = (optimized_hits / total_shots) * 100.0
    
    print("-" * 50)
    print(f"[OPTIMIZED STATISTICS]")
    print(f"Registered Hits:  {optimized_hits}")
    print(f"Salvaged Rounds:  {salvaged_rounds}")
    print(f"New Hit Reg Rate: {opt_reg_rate:.1f}%")
    
    # Calculate improvement relative to POSSIBLE hits (excluding true misses)
    # True potential = Total - Actual Player Misses ("miss")
    # In this stream, we have 1 "miss". So 19 potentia hits.
    
    potential_hits = total_shots - actual_misses
    
    print(f"\n[SUMMARY]")
    print(f"Baseline Accuracy: {base_reg_rate:.1f}%")
    print(f"Sophia Accuracy:   {opt_reg_rate:.1f}%")
    print(f"Reality Correction: +{salvaged_rounds} rounds confirmed")

if __name__ == "__main__":
    estimate_hitreg()
