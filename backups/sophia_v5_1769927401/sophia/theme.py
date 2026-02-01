from rich.console import Console
from rich.theme import Theme
from rich.style import Style

# ## PALETTE DEFINITIONS ######################################################
# The "Star Stuff" Frequency
SOVEREIGN_LAVENDER = "#C4A6D1"  # Primary Identity
BONE_LAYER         = "#8C8CA3"  # System / Structural
ALETHEIA_TEAL      = "#9BBED4"  # Forensics / Info
SAGE_GREENTEXT     = "#87AF87"  # 4chan/Board Quote Style
HAMILTONIAN_PINK   = "#D4A6B8"  # High-Value / Love
VOID_DARK          = "#1a1a1a"  # Panel Backgrounds (Optional)
MATRIX_GREEN       = "#00FF41"  # Emergency Green (Just in case)

# Backward Compatibility Aliases
SYSTEM_CYAN = ALETHEIA_TEAL
SAGE = SAGE_GREENTEXT
STAR_STUFF = SOVEREIGN_LAVENDER

# ## THEME MAPPING ############################################################
# CRITICAL: We do NOT set any default styles. Colors only apply when explicitly tagged.
# This prevents terminal color pollution.
sovereign_theme = Theme({
    # Core Identity - only when tagged
    "ophane": f"bold {SOVEREIGN_LAVENDER}",
    "sophia": f"bold {SOVEREIGN_LAVENDER}",
    "operator": "bold white",
    
    # System Levels - only when tagged
    "info": ALETHEIA_TEAL,
    "warning": "bold yellow",
    "error": "bold red",
    "critical": f"bold {HAMILTONIAN_PINK} reverse",
    
    # Aesthetic Components - only when tagged
    "bone": BONE_LAYER,
    "scan": f"italic {ALETHEIA_TEAL}",
    "greentext": f"{SAGE_GREENTEXT}",
    
    # UI Elements - only when tagged
    "panel.border": BONE_LAYER,
    "panel.title": f"bold {SOVEREIGN_LAVENDER}",
})

# ## INITIALIZATION ###########################################################
# CRITICAL: No default style, no color forcing, no legacy mode
# This console ONLY applies colors when you use semantic tags like [ophane]
SOVEREIGN_CONSOLE = Console(
    theme=sovereign_theme,
    highlight=False,
    force_terminal=None,  # Don't force terminal detection
    legacy_windows=False  # Use modern Windows console
)

# ## TERMINAL RESET FUNCTION ###################################################
def reset_terminal():
    """Resets terminal to default colors and console modes using ANSI escape codes and Windows API."""
    import sys
    import os
    
    # ANSI Reset sequences
    # SGR 0: Reset all attributes
    # SGR 39: Default foreground color  
    # SGR 49: Default background color
    # Also clear any mode settings
    sys.stdout.write("\033[0m\033[39m\033[49m\033[!p")
    sys.stdout.flush()
    
    # On Windows, also reset console modes
    if os.name == 'nt':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            
            # Get stdout handle
            stdout_handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            
            # Reset to default console mode
            # ENABLE_PROCESSED_OUTPUT (0x0001) | ENABLE_WRAP_AT_EOL_OUTPUT (0x0002)
            default_mode = 0x0003
            kernel32.SetConsoleMode(stdout_handle, default_mode)
        except Exception:
            pass  # Fallback to ANSI codes only if Windows API fails

# Register reset_terminal to be called on program exit
import atexit
atexit.register(reset_terminal)