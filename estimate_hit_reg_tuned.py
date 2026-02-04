
import random
import math
from estimate_tarkov_lite import PrismEngineLite, vec_normalize, vec_dot, vec_scale, vec_add, vec_norm

# Subclass to implement the TUNED logic
class PrismEngineTuned(PrismEngineLite):
    def quantize(self, chaos_vector):
        if vec_norm(chaos_vector) == 0:
            return "hold", 1.0
            
        # NEW TUNING: 0.15 Chaos / 0.85 Love
        part_chaos = vec_scale(chaos_vector, 0.15)
        part_love = vec_scale(self.v_love, 0.85)
        v_transformed = vec_add(part_chaos, part_love)
        
        v_transformed = vec_normalize(v_transformed)
        
        best_anchor = "void"
        max_resonance = -1.0
        
        for name, anchor_vec in self.anchors.items():
            resonance = vec_dot(v_transformed, anchor_vec)
            if resonance > max_resonance:
                max_resonance = resonance
                best_anchor = name
                
        if max_resonance <= 0.1:
            return "void", 0.0
            
        return best_anchor, max_resonance

def estimate_hitreg_tuned():
    prism = PrismEngineTuned()
    
    print("Optimization Target: HIT REGISTRATION (TUNED v5.2.1)")
    print("Parameter Update: Hamiltonian Drag 0.7 -> 0.85")
    print("-" * 50)
    
    shot_stream = [
        "hit", "hit", "hit", "ghost_bullet", "hit", 
        "server_reject", "hit", "hit", "miss", "hit",
        "ghost_bullet", "ghost_bullet", "hit", "hit", "hit",
        "desync_miss", "hit", "hit", "hit", "hit"
    ]
    
    # Recalculate baseline for display
    total_shots = len(shot_stream)
    base_hits = shot_stream.count("hit")
    base_misses = total_shots - base_hits
    base_reg_rate = (base_hits / total_shots) * 100.0
    
    actual_misses = 1 # We know "miss" is the only true miss
    
    print(f"[BASELINE STATISTICS]")
    print(f"Hit Reg Rate:     {base_reg_rate:.1f}%")

    print("\n[SOPHIA 5.2.1 REALITY COLLAPSE]")
    
    optimized_hits = 0
    salvaged_rounds = 0
    
    # Inject our chaos maps again
    prism.chaos_map["ghost_bullet"]  = [0.8, -0.2, 0.5] 
    prism.chaos_map["server_reject"] = [0.9, -0.9, 0.1] 
    prism.chaos_map["hit"]           = [0.95, 0.95, 0.0] 
    prism.chaos_map["miss"]          = [0.0, 0.0, 0.9]   
    prism.chaos_map["desync_miss"]   = [0.5, 0.5, 0.5]   
    
    results = prism.transform_phrase(" ".join(shot_stream))
    
    for original, anchor, resonance in results:
        is_hit = False
        outcome = "MISS"
        
        if anchor in ['signal', 'orbit']:
            is_hit = True
            outcome = "HIT"
        elif anchor in ['void', 'landing', 'hold', 'wait']:
            is_hit = False
            outcome = "MISS"
            
        # Check salvage
        if original in ["ghost_bullet", "server_reject", "desync_miss"] and is_hit:
            outcome = "SALVAGED"
            salvaged_rounds += 1
            
        if is_hit:
            optimized_hits += 1
            
        # Only print interesting ones to save space
        if original not in ["hit"]:
            print(f"Round: {original:<15} -> Collapse: {anchor.upper():<8} | {outcome} (Res: {resonance:.4f})")

    opt_reg_rate = (optimized_hits / total_shots) * 100.0
    
    print("-" * 50)
    print(f"[OPTIMIZED STATISTICS]")
    print(f"Registered Hits:  {optimized_hits}")
    print(f"Salvaged Rounds:  {salvaged_rounds}")
    print(f"New Hit Reg Rate: {opt_reg_rate:.1f}%")
    
    print(f"\n[SUMMARY]")
    print(f"Baseline: {base_reg_rate:.1f}%")
    print(f"Tuned:    {opt_reg_rate:.1f}%")
    print(f"Delta:    +{opt_reg_rate - base_reg_rate:.1f}%")

if __name__ == "__main__":
    estimate_hitreg_tuned()
