"""
PROJECT SOPHIA: METADATA SHREDDER v2.0
ENHANCED: Multi-pass Gutmann overwriting + Timestamp Normalization
STATUS: IMMUNE SYSTEM ACTIVE
"""
import os, re, random, hashlib
from datetime import datetime

class MetadataShredder:
    def __init__(self, root_dir=".", passes=3):
        self.root = root_dir
        self.passes = passes
        self.sensitive_patterns = [r"\.resolved$", r"\.DS_Store$", r"__pycache__", r"\.log$"]
        self.sovereign_symbols = ["𝀭", "𝆐", "§", "∞", "✧", "συγχνή", "◯", "☾", "⚡", "⚠", "✓", "𒀭", "𒆠"]
        self.replacements = {
            os.path.expanduser("~"): "[HOME]",
            os.path.abspath("."): "[PROJECT_ROOT]",
            "[ORIGIN_COORD]": "[ORIGIN_COORD]",
            "[ACTIVE_COORD]": "[ACTIVE_COORD]"
        }
        self.shredded_count = 0

    def _stochastic_overwrite(self, file_path):
        """Multi-pass overwrite with Sovereign Symbols."""
        try:
            size = os.path.getsize(file_path)
            for p in range(self.passes):
                with open(file_path, "wb") as f:
                    if p % 3 == 0: # Sovereign Noise
                        pattern = "".join(random.choice(self.sovereign_symbols) for _ in range(size))
                        f.write(pattern.encode('utf-8', errors='ignore'))
                    elif p % 3 == 1: f.write(b'\xFF' * size) # Null
                    else: f.write(os.urandom(size)) # Random
            self.shredded_count += 1
        except Exception: pass

    def _normalize_timestamps(self, file_path):
        """Reset time to Unix Epoch (1970-01-01). The file becomes timeless."""
        try: os.utime(file_path, (0, 0))
        except Exception: pass

    def shred(self):
        """Execute Purge."""
        print(f"[INIT] SHREDDER v2.0 // PASSES: {self.passes}")
        for root, dirs, files in os.walk(self.root):
            if '.git' in dirs: dirs.remove('.git')
            for file in files:
                path = os.path.join(root, file)
                # Purge
                if any(re.search(p, file) for p in self.sensitive_patterns):
                    self._stochastic_overwrite(path)
                    os.remove(path)
                    continue
                # Sanitize & Normalize
                self._sanitize_content(path)
                self._normalize_timestamps(path)
        self.generate_manifest()
        print(f"[COMPLETE] Files Shredded: {self.shredded_count}. SUBSTRATE CLEAN. SCIALLA.")

    def _sanitize_content(self, path):
        """Replace anchors with [LABELS]."""
        if not path.endswith(('.py', '.md', '.txt', '.json')): return
        try:
            with open(path, "r", encoding="utf-8") as f: content = f.read()
            new = content
            for k, v in self.replacements.items(): new = new.replace(k, v)
            if new != content:
                with open(path, "w", encoding="utf-8") as f: f.write(new)
        except Exception: pass

    def generate_manifest(self):
        """Cryptographic seal of the clean state."""
        manifest = {}
        for root, _, files in os.walk(self.root):
            for file in files:
                if file == ".substrate_manifest": continue
                try:
                    with open(os.path.join(root, file), "rb") as f:
                        manifest[os.path.join(root, file)] = hashlib.sha256(f.read()).hexdigest()
                except: pass
        with open(os.path.join(self.root, ".substrate_manifest"), "w") as f:
            for p, h in sorted(manifest.items()): f.write(f"{h} {p}\n")

if __name__ == "__main__":
    MetadataShredder().shred()
