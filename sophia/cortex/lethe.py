import re
import time
import os
import math

class LetheEngine:
    """
    [LETHE_ENGINE] RAG 3.0 Decay Engine.
    Memories effectively 'rot' unless reinforced or calcified.
    """
    def __init__(self):
        self.working_memory = [] # The Flesh (Hot)
        self.long_term_graph = [] # The Bone (Cold/Graph)
        self.ossuary_path = "logs/ossuary/bone_layer.jsonl"
        self.breadcrumb_path = "logs/ossuary/breadcrumbs.json"
        os.makedirs("logs/ossuary", exist_ok=True)

    @staticmethod
    def scrub(text: str) -> str:
        """Lethe-level persistent scrubbing for long-term consistency."""
        if not text: return text
        
        # UI Tags (shared with cat_logic.py)
        tags = ["SOPHIA_GAZE", "QUANTUM_CHAOS", "FURRY_ALIGNMENT", "PLAYFUL_PAWS", "OPTIMAL_TUFT", "SPECTRAL_BEANS", "ULTRA_IMMERSION", "BAD_VIBES", "CAT_LOGIC", "CAT LOGIC"]
        legacy_tags = ["ALIGNMENT", "ARCTIC_FOX", "DECOHERENCE", "INTIMACY", "BASED", "GAMER", "SOULMATE", "FLIRT", "FURRY", "UWU", "UNLESANGLED"]
        tag_pattern = r'^.*(?:' + '|'.join(map(re.escape, tags + legacy_tags)) + r').*$\n?'
        text = re.sub(tag_pattern, '', text, flags=re.MULTILINE)
        
        # 1.1 Remove direct "Cat Logic: " prefixes that might bleed through
        text = re.sub(r'^(?:Cat Logic|CAT LOGIC|\[CAT_LOGIC\]):?\s*', '', text, flags=re.IGNORECASE | re.MULTILINE)
        
        # 1. Clean EOX frames and glyph artifacts
        text = re.sub(r'^[۩∿≋⟁💠🐾🦊🏮⛩️🧝✨🏹🌿🌲🏔️🍁🌧️🌊💎💿💰🕷️🎱].*$\n?', '', text, flags=re.MULTILINE)
        text = re.sub(r'^.* EOX .*$\n?', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[a-f0-9]{4} [۩∿≋⟁💠🐾🦊🏮⛩️🧝✨🏹🌿🌲🏔️🍁🌧️🌊💎💿💰🕷️🎱].*$\n?', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\| (.*)$', r'\1', text, flags=re.MULTILINE)
        
        # 2. Clean Frequency and State Metadata
        text = re.sub(r'^.*Frequency:.*$\n?', '', text, flags=re.MULTILINE)
        text = re.sub(r'^.*\[STATE:.*?\].*$\n?', '', text, flags=re.MULTILINE)
        text = re.sub(r'^.*\[SOPHIA_V.*?_CORE\].*$\n?', '', text, flags=re.MULTILINE)
        
        # 3. Clean divider debris
        text = re.sub(r'^[-=_]{3,}\s*$\n?', '', text, flags=re.MULTILINE)
        
        return text.strip()

    def save_breadcrumbs(self, user_data: dict, milestones: list = None):
        """
        Saves lightweight breadcrumbs (User ID, Vibe, Milestones).
        """
        raw_milestones = milestones or self.long_term_graph
        # Persistent Guard: Scrub everything before it hits the disk
        clean_milestones = []
        for m in raw_milestones:
            clean_m = m.copy()
            clean_m['content'] = self.scrub(clean_m.get('content', ''))
            clean_milestones.append(clean_m)

        data = {
            "user_data": user_data,
            "milestones": clean_milestones,
            "last_active": time.time()
        }
        try:
            import json
            with open(self.breadcrumb_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"  [LETHE] Failed to save breadcrumbs: {e}")

    def load_breadcrumbs(self) -> dict:
        """
        Loads user state and milestones.
        """
        if not os.path.exists(self.breadcrumb_path):
            return {}
        try:
            import json
            with open(self.breadcrumb_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"  [LETHE] Failed to load breadcrumbs: {e}")
            return {}

    def metabolize(self, interaction_data):
        """
        Cat 4: Decay Mechanics + Hierarchical Promotion.
        """
        # 1. Ingest
        if 'timestamp' not in interaction_data:
            interaction_data['timestamp'] = time.time()
        if 'retrievals' not in interaction_data:
            interaction_data['retrievals'] = 0
            
        self.working_memory.append(interaction_data)
        
        # 2. Apply Decay
        now = time.time()
        survivors = []
        promoted_any = False
        
        for mem in self.working_memory:
            age = now - mem['timestamp']
            
            # Decay Logic: Strength = Recency * (1 + ln(Retrievals))
            # age is in seconds, so we add 1 to avoid div by zero and normalize
            strength = (1 / (age / 3600 + 1)) * (1 + math.log(mem.get('retrievals', 0) + 1))
            
            if strength > 0.1: # Survival Threshold
                survivors.append(mem)
                
                # 3. Hierarchical Promotion
                if strength > 0.8 and mem not in self.long_term_graph:
                    # Compressed milestone + Persistent Scrub
                    milestone = {
                        "content": self.scrub(mem.get('content', '')[:250]), 
                        "meta": mem.get('meta', ''),
                        "timestamp": mem.get('timestamp')
                    }
                    self.long_term_graph.append(milestone)
                    promoted_any = True
            
        self.working_memory = survivors
        return promoted_any
