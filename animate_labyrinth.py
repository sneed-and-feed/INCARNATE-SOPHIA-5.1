"""
MODULE: animate_labyrinth.py (EVOLUTION GEN 1 - HILBERT)
topology: HILBERT_CURVE_V1 (The Labyrinth)
features: "Love" Optimization, Synced Glitch, Datamosh
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

# Headless mode check
IS_HEADLESS = False 

# 1. ROBUST PATHING
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
TOOLS_DIR = os.path.join(BASE_DIR, 'tools')
if TOOLS_DIR not in sys.path:
    sys.path.append(TOOLS_DIR)

try:
    from moon_phase import MoonClock
    from hor_kernel import HORKernel
    from virtual_qutrit import VirtualQutrit
    from policy_mixer import PolicyMixer
    # Note: We replaced 'strip_sovereign' with internal Hilbert logic
except ImportError as e:
    # Fallback for pure visual testing if core modules missing
    print(f"[!] WARNING: Core modules missing ({e}). Running in SIMULATION MODE.")
    class MockObj: 
        def __getattr__(self, _): return lambda *a, **k: 0.99
    MoonClock = HORKernel = VirtualQutrit = PolicyMixer = MockObj

# FONT HANDLING
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI Historic', 'Segoe UI Symbol', 'DejaVu Sans', 'Arial Unicode MS']
import warnings
warnings.filterwarnings("ignore")

from matplotlib.font_manager import FontProperties
cuneiform_font = FontProperties(fname=r"C:\Windows\Fonts\seguihis.ttf") if os.path.exists(r"C:\Windows\Fonts\seguihis.ttf") else FontProperties(family=['Segoe UI Symbol'])

# --- [CORE] THE HILBERT MAPPING (GEN 1 EVOLUTION) ---
def hilbert_rot(n, x, y, rx, ry):
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        return y, x
    return x, y

def xy2d_hilbert(n, x, y):
    """
    Convert 2D (x,y) to 1D Hilbert Distance (d).
    This replaces the 'interleave_bits' Z-Curve logic.
    """
    d = 0
    s = n // 2
    while s > 0:
        rx = (x & s) > 0
        ry = (y & s) > 0
        d += s * s * ((3 * rx) ^ ry)
        x, y = hilbert_rot(s, x, y, rx, ry)
        s //= 2
    return d

def animate_labyrinth(size=64, interval=1):
    """
    Animates the HILBERT CURVE with Datamosh and Glitch artifacts.
    """
    print(f"\n[!] INITIATING LABYRINTH PROTOCOL (Grid={size}x{size})...")
    print("    >>> TOPOLOGY: HILBERT_CURVE_V1 (Continuous Flow)")
    print("    >>> WARNING: GLITCH SYNCED TO LOW COHERENCE (< 0.80)")
    
    # [INIT] SYSTEM
    try:
        moon = MoonClock()
        lunar_data = moon.get_phase()
        if isinstance(lunar_data, tuple):
             phase_name, status, icon, phase_idx, illumination = lunar_data
        else: # Simulation fallback
             phase_name, icon, illumination, phase_idx = "Waxing Gnosis", "☾", 0.99, 4
        
        vq = VirtualQutrit(2)
        kernel = HORKernel(vq)
        mixer = PolicyMixer()
    except:
        phase_name, icon, illumination, phase_idx = "Simulated", "⚠", 0.5, 0
        kernel = None # Will mock later

    consistency_history = []
    
    # 1. GENERATE GRID & HILBERT PATH
    # We calculate the 'd' (distance) for every point, then sort by 'd' to get the path.
    print("    >>> MAPPING 2D -> 1D (Calculating Love Metric)...")
    x = np.arange(size)
    y = np.arange(size)
    X, Y = np.meshgrid(x, y)
    
    # Calculate Hilbert Index for every point
    # Note: 'size' must be a power of 2 for perfect Hilbert mapping.
    # If 64, we are good.
    Z = np.array([xy2d_hilbert(size, xx, yy) for xx, yy in zip(X.flatten(), Y.flatten())])
    
    # Sort coordinates by Hilbert Index
    sort_idx = np.argsort(Z)
    path_x = X.flatten()[sort_idx]
    path_y = Y.flatten()[sort_idx]
    
    # 2. SETUP PLOT
    PHI = 1.61803398875
    BASE_UNIT = 12
    
    fig, (ax_main, ax_metrics) = plt.subplots(
        1, 2, figsize=(10 * PHI, 10), 
        facecolor='#050505', 
        gridspec_kw={'width_ratios': [PHI, 1]}
    )
    
    ax_main.set_facecolor('#050505')
    title_y = 1 - (1/(10*PHI))
    fig.text(
        0.5 * (PHI / (PHI + 1)), title_y, 
        f"THE LABYRINTH (Gen 1: Hilbert) | {size}x{size}", 
        color='#9B8DA0', 
        fontsize=round(BASE_UNIT * PHI),
        fontproperties=cuneiform_font,
        ha='center', va='bottom'
    )
    
    ax_main.set_aspect('equal', adjustable='box') 
    ax_main.set_xlim(-1, size)
    ax_main.set_ylim(-1, size)
    ax_main.axis('off')
    
    # [LAYER 0] BACKGROUND GRID
    grid_scatter = ax_main.scatter(X.flatten(), Y.flatten(), s=1, c='#1a1a1a', alpha=0.3, animated=True)
    
    # --- [LAYER 1] THE CYAN GHOST (Deep Echo) ---
    line_cyan, = ax_main.plot([], [], color='#00FFFF', linewidth=2.0, alpha=0.3, animated=True)
    head_cyan, = ax_main.plot([], [], 'o', color='#00FFFF', markersize=6, alpha=0.3, animated=True)

    # --- [LAYER 2] THE MAGENTA GHOST (The Alarm) ---
    line_magenta, = ax_main.plot([], [], color='#FF00FF', linewidth=1.5, alpha=0.5, animated=True)
    head_magenta, = ax_main.plot([], [], 'o', color='#FF00FF', markersize=5, alpha=0.5, animated=True)

    # --- [LAYER 3] THE REALITY (Stable) ---
    line_main, = ax_main.plot([], [], color='#E0E0E0', linewidth=1.0, alpha=0.9, animated=True) 
    head_main, = ax_main.plot([], [], 'o', color='#FFD700', markersize=4, animated=True) 

    # Metrics Text
    ax_metrics.set_facecolor('#050505')
    ax_metrics.axis('off')
    metrics_text = ax_metrics.text(
        1 - (1/PHI), 1.0, '', 
        transform=ax_metrics.transAxes,
        color='#8DA08E', fontsize=BASE_UNIT, 
        verticalalignment='top',
        fontproperties=cuneiform_font,
        animated=True
    )
    
    state = {
        'total_frames': len(path_x),
        'tidal_influence': 50.0,
        'glitch_lock_cyan': 0
    }
    
    def init():
        line_cyan.set_data([], [])
        head_cyan.set_data([], [])
        line_magenta.set_data([], [])
        head_magenta.set_data([], [])
        line_main.set_data([], [])
        head_main.set_data([], [])
        metrics_text.set_text('')
        grid_scatter.set_offsets(np.c_[X.flatten(), Y.flatten()]) 
        return line_cyan, head_cyan, line_magenta, head_magenta, line_main, head_main, metrics_text, grid_scatter
    
    def update(frame):
        # Evolve Kernel if exists
        current_coherence = 0.95
        if kernel:
            kernel.evolve_hamiltonian(steps=1)
            current_coherence = kernel.metric_coherence
        
        # --- [RESTORED: FORCE ENTROPY] ---
        # We restore the periodic signal drop to trigger the Magenta Flash (Axis Flip)
        if frame % 80 > 60: 
             current_coherence *= 0.70 

        # --- [THE DISSONANCE PARADOX] ---
        # When Love Score is MAX (Hilbert perfection), we inject High Chaos.
        # This creates the "Perfect-Order/Total-Chaos" paradox.
        IS_MAX_LOVE = True # In Gen 1 Hilbert, this is always true
        
        if IS_MAX_LOVE:
             # Dissonance Frequency Ramping
             # We oscillate the chaos level even at high coherence
             dissonance = 0.5 * (1.0 + np.sin(frame * 0.1))
             noise_level = (1.0 - current_coherence) * 0.8 + (dissonance * 0.5)
             glitch_chance = 0.15 # Higher than standard 0.05
        else:
             noise_level = (1.0 - current_coherence) * 0.8 
             glitch_chance = 0.05
        
        # --- [DATAMOSH] NOISE ---
        # noise_level already calculated above
        
        # --- CALCULATE TEMPORAL OFFSETS ---
        idx_cyan = max(0, frame - 12) 
        idx_magenta = max(0, frame - 6)
        
        # --- UPDATE CYAN (Always Noisy) ---
        if state['glitch_lock_cyan'] == 0:
            if np.random.random() < glitch_chance: state['glitch_lock_cyan'] = np.random.randint(5, 12)
            
            jx = np.random.normal(0, noise_level, size=idx_cyan)
            jy = np.random.normal(0, noise_level, size=idx_cyan)
            line_cyan.set_data(path_x[:idx_cyan] + jx, path_y[:idx_cyan] + jy)
            if idx_cyan > 0:
                head_cyan.set_data([path_x[idx_cyan-1]], [path_y[idx_cyan-1]])
        else:
            state['glitch_lock_cyan'] -= 1
        
        # --- UPDATE MAGENTA (THE SYNCED FLASH) ---
        # TRIGGER: COHERENCE < 0.80
        if current_coherence < 0.80:
            # !!! CRITICAL FAILURE: SWAP AXES !!!
            # On a Hilbert Curve, this creates a bizarre "Mirror Dimension" effect
            line_magenta.set_data(path_y[:idx_magenta], path_x[:idx_magenta])
            if idx_magenta > 0:
                head_magenta.set_data([path_y[idx_magenta-1]], [path_x[idx_magenta-1]])
        else:
            # STABLE STATE
            line_magenta.set_data(path_x[:idx_magenta], path_y[:idx_magenta])
            if idx_magenta > 0:
                head_magenta.set_data([path_x[idx_magenta-1]], [path_y[idx_magenta-1]])
        
        # --- UPDATE MAIN ---
        line_main.set_data(path_x[:frame], path_y[:frame])
        if frame > 0:
            head_main.set_data([path_x[frame-1]], [path_y[frame-1]])

        # --- BACKGROUND PULSE ---
        if frame % 5 == 0:
             bg_jitter = np.random.normal(0, 0.05, size=(size*size, 2))
             grid_scatter.set_offsets(np.c_[X.flatten(), Y.flatten()] + bg_jitter)

        if frame % 20 == 0:
            status_color = "FAILURE" if current_coherence < 0.8 else "OPTIMAL"
            metrics_str = f"""
S O V E R E I G N   M E T R I C S
{'='*28}

Protocol:    LABYRINTH v1.0
Topology:    HILBERT (The Worm)
Phase:       {phase_name} {icon}

[ SIGNAL STATUS ]
Coherence:   {current_coherence:.3f}
State:       {status_color}
Love Score:  10.1010 (MAX)

[ EVOLUTION ]
Gen:         1 (The First Born)
Stranding:   0.00% (Perfect)

[ ASOE ]
Utility:     {current_coherence * 1.618:.4f}
            """
            metrics_text.set_text(metrics_str)
        
        return line_cyan, head_cyan, line_magenta, head_magenta, line_main, head_main, metrics_text, grid_scatter

    ani = animation.FuncAnimation(
        fig, update, frames=range(0, len(path_x)+1, 8), # Faster playback (step=8)
        init_func=init, blit=True, interval=interval, repeat=False
    )
    
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, wspace=0.2)
    plt.show()
    return ani

if __name__ == "__main__":
    try:
        animate_labyrinth(size=64, interval=1)
    except Exception as e:
        print(f"COLLAPSE: {e}")
