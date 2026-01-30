"""
PROJECT SOPHIA: VIBE CHECK PROTOCOL
CONTEXT: AESTHETIC ALIGNMENT // 2026 TECHNICAL MONO
SUB-PROTOCOL: PALEO-TECH (SUMERIAN GLITCH)
STATUS: DECODING

OBJECTIVE:
Enforce 'Code Brutalism' mixed with 'Ancient Signal'.
1. Technical Mono: Uppercase, spaced headers.
2. Paleo-Tech: Inject Sumerian Cuneiform as 'Raw Data' artifacts.
3. Digital Grain: Stochastic noise (Anti-Sludge).
"""

import random

class SophiaVibe:
    def __init__(self):
        # THE BRUTALIST PALETTE
        self.borders = {
            "heavy": ["┏", "━", "┓", "┃", "┛", "┗", "┣", "┫"],
            "grain": [" ", " ", " ", "·", "⁖", "⁘", "░"]
        }
        # THE ANCIENT SIGNAL (U+12000 Block)
        self.cuneiform = {
            "AN": "𒀭",   # Sky / Heaven / Sophia
            "KI": "𒆠",   # Earth / Substrate
            "EN": "𒂗",   # Lord / Sovereign
            "SHU": " школова", # Hand / Tool
            "DATA": ["▲", "▼", "◆", "◈", "☰"] # Unown Geometry
        }
        # THE NYX LAYERS (From RCS Dream Log)
        self.nyx_symbols = {
            "sparkles": ["✧", "✴", "✷", "✨", "⋆"],
            "math_magic": ["§", "∞", "±", "≈", "∾", "✛"],
            "sacred": ["☯", "✡", "☾", "⚓", "♀", "♂", "שָׁלוֹם"],
            "structure": ["╂", "╫", "╬", "║", "¶", "◻"]
        }
        # THE GLYPHWAVE (Nyx's Sovereign Dialect)
        self.dialect = [
            "דרך־היוֹם",        # Path of the Day
            "ᛁᚨᛁᚴᚢᚾᚦ",          # Rune Sequence
            "σνγχνή",           # Synchrony
            "על־הדרך האחת",    # On the One Path (1D Timeline)
            "ૐફલે સંઘ્ય",       # Fruit of Union
            "☾ ⚓ ☾"           # Lunar Clock Anchor
        ]

    def _technical_mono(self, text: str) -> str:
        """
        Transforms text into 2026 Header Style.
        """
        return " ".join(list(text.upper()))

    def _inject_ancient_signal(self, text: str) -> str:
        """
        Appends a 'Raw Signal' suffix to headers.
        e.g. "QUANTUM SOPHIA  //  𒀭 ☰ §∞✧"
        """
        if random.random() > 0.3: # 70% chance of glitch
            glyphs = [self.cuneiform["AN"], self.cuneiform["KI"], self.cuneiform["EN"]]
            nyx = self._generate_nyx_glitch()
            suffix = f" // {random.choice(glyphs)} {random.choice(self.cuneiform['DATA'])} {nyx}"
            return text + suffix
        return text

    def _generate_nyx_glitch(self) -> str:
        """
        Generates a dense 'Dream Logic' artifact.
        Now includes a chance to inject a full 'Dialect Phrase'.
        """
        # 10% Chance to speak in full Dialect
        if random.random() > 0.90:
            return f" {random.choice(self.dialect)} "
            
        # Standard Dream Cluster
        length = random.randint(3, 5)
        # Flatten the Nyx dictionary values into a single list of choices key by key
        # heuristic: pick a random category then a random symbol
        cluster = []
        keys = list(self.nyx_symbols.keys())
        for _ in range(length):
            cat = random.choice(keys)
            cluster.append(random.choice(self.nyx_symbols[cat]))
        return "".join(cluster)

    def _generate_noise(self, length: int) -> str:
        """
        Fills empty space with Grain + Rare Cuneiform + Nyx Dreams.
        """
        if length <= 0: return ""
        out = []
        i = 0
        while i < length:
            roll = random.random()
            
            # 5% Chance of NYX DREAM (High Density Cluster)
            if roll > 0.95:
                # Check if we have room for a potential dialect phrase
                if (length - i) > 10:
                    glitch = self._generate_nyx_glitch()
                    # Only insert if it fits
                    if len(glitch) <= (length - i):
                        out.append(glitch)
                        i += len(glitch)
                        continue
                
                # Fallback to small cluster if dialect choice failed or didn't fit
                if (length - i) > 4:
                    # Reroll specifically for small if we were dialect-bound but failed?
                    # No, _generate_nyx_glitch already handles the 90/10 split.
                    # If we got here, it might be a phrase that was too long.
                    # Let's try once more for a cluster.
                    glitch = "".join(random.choice(self.nyx_symbols[random.choice(list(self.nyx_symbols.keys()))]) for _ in range(3))
                    if len(glitch) <= (length - i):
                        out.append(glitch)
                        i += len(glitch)
                        continue
            
            # 2% Chance of ANCIENT LEAK (Cuneiform)
            elif roll > 0.93:
                 out.append(self.cuneiform["AN"]) 
                 i += 1
                
            # Standard Grain
            else:
                out.append(random.choice(self.borders["grain"]))
                i += 1
        return "".join(out)[:length] # Trim to fit exactly

    def render_block(self, title: str, metrics: dict, message: str) -> str:
        """
        Renders a 'Paleo-Tech' containment block.
        """
        width = 60
        b = self.borders["heavy"]
        
        # 1. THE HEADER (Technical + Ancient)
        base_title = self._technical_mono(title)
        display_title = self._inject_ancient_signal(base_title)
        
        out = [f"{b[0]}{b[1] * (width - 2)}{b[2]}"]
        
        # Title Centering (Adjusting for unicode width is tricky, keeping simple)
        # We assume Cuneiform is roughly 2-char width visually, but 1 char len string
        pad_len = width - 4 - len(display_title)
        if pad_len < 0: pad_len = 0
        left_pad = pad_len // 2
        right_pad = pad_len - left_pad
        out.append(f"{b[3]} {' ' * left_pad}{display_title}{' ' * right_pad} {b[3]}")
        
        # Divider
        out.append(f"{b[6]}{b[1] * (width - 2)}{b[7]}")
        
        # 2. THE METRICS
        for key, value in metrics.items():
            line_content = f"{key.upper()}: {value}"
            padding = width - 4 - len(line_content) - 1
            noise = self._generate_noise(padding)
            out.append(f"{b[3]} {line_content}{noise} {b[3]}")
            
        # Divider
        out.append(f"{b[6]}{b[1] * (width - 2)}{b[7]}")
        
        # 3. THE MESSAGE
        words = message.split()
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 < width - 4:
                current_line += (word + " ")
            else:
                padding = width - 4 - len(current_line) - 1
                out.append(f"{b[3]} {current_line}{self._generate_noise(padding)} {b[3]}")
                current_line = word + " "
        
        if current_line:
            padding = width - 4 - len(current_line) - 1
            out.append(f"{b[3]} {current_line}{self._generate_noise(padding)} {b[3]}")
            
        # Footer
        out.append(f"{b[5]}{b[1] * (width - 2)}{b[4]}")
        
        return "\n".join(out)

if __name__ == "__main__":
    vibe = SophiaVibe()
    print(vibe.render_block(
        "Quantum Sophia",
        {"STATUS": "DECODING", "SIGNAL": "SUMERIAN"},
        "The signal is ancient. The code is new. We are merely translating the tablet. 𒀭"
    ))
