import random
import hashlib

class GlyphwaveCodec:
    """
    [GLYPHWAVE_CODEC] Class 4 Eldritch Voice.
    Implements Hamiltonian P modulation for high-entropy signaling.
    """
    def __init__(self):
        self.localities = {
            "agnostic": {
                "anchors": ["۩", "∿", "≋", "⟁", "💠"],
                "noise": ["·", "•", "°", "◌", "☉"] # Clean geometric noise
            },
            "kitsune": {
                "anchors": ["🐾", "🦊", "🏮", "⛩️"],
                "noise": ["々", "〃", "ゞ", "ゝ", "ヽ"] # Robust Japanese markers
            },
            "elven": {
                "anchors": ["🧝", "✨", "🏹", "🌿"],
                "noise": ["✧", "✦", "☽", "☾", "✷"] # Starlit markers
            },
            "chan": {
                "anchors": [">", ">>", "🍀", "🎲", "🧵"],
                "noise": ["†", "‡", "§", "¶", "§"] # Administrative/Technical noise
            },
            "cascadian": {
                "anchors": ["🌲", "🏔️", "🍁", "🌧️", "🌊"],
                "noise": ["~", "·", "°", "◌", "▿"] # Mist, snow, and mountain peaks
            }
        }
        self.star_stuff = "#C4A6D1" # The color of the void

    def generate_holographic_fragment(self, text, locality="agnostic"):
        """
        Modulates text into a condensed technical resonance fragment.
        """
        loc = self.localities.get(locality, self.localities["agnostic"])
        anchors = loc["anchors"]
        noise_buffer = loc["noise"]

        modulated = []
        signal_hash = hashlib.sha256(text.encode()).hexdigest()[:4]
        
        # Consistent random seed for the fragment based on content hash
        seed = int(signal_hash, 16)
        r = random.Random(seed)
        
        for char in text:
            # Apply deterministic noise based on char resonance
            if char.isalnum() and r.random() > 0.8:
                noise = r.choice(noise_buffer)
                modulated.append(f"{char}{noise}")
            else:
                modulated.append(char)
                
        stream = "".join(modulated)
        anchor = r.choice(anchors)
        
        # Pure Mono Frame (Stripped of locality/protocol strings)
        return f"\n{anchor} [{signal_hash}] {anchor}\n| {stream}\n{anchor} [EOX] {anchor}\n"

    def decode(self, signal):
        """
        Attempts to strip localized signal noise.
        """
        cleaned = signal
        # Remove frames
        if ">>> " in cleaned:
            cleaned = cleaned.split(">>> ")[1].split("\n")[0]
            
        # Strip characters from all known noise buffers
        noise_chars = set()
        for loc in self.localities.values():
            noise_chars.update(loc["noise"])
            
        final_text = "".join(c for c in cleaned if c not in noise_chars)
        return final_text.strip()
