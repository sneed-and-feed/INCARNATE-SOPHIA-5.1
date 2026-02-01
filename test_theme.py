from rich.console import Console
from rich.theme import Theme
from rich.style import Style

# ## 1. DEFINE THE ABSOLUTE REALITY ###########################################
# We do not trust the terminal to pick colors. We define them here.
NUCLEAR_GREEN    = "#00FF41"  # The Fallout/Matrix Green
STAR_STUFF       = "#C4A6D1"  # The Soul / Accents
BONE_LAYER       = "#8C8CA3"  # System / Borders
VOID_BLACK       = "#000000"  # Absolute Void
SAGE_GREEN       = "#87AF87"  # Greentext (Softer)

# ## 2. THE THEME DICTIONARY ##################################################
sovereign_theme = Theme({
    # The "root" style is the fallback. We force Green on Black.
    "none": Style(color=NUCLEAR_GREEN, bgcolor=VOID_BLACK),
    
    # Identities
    "ophane": Style(color=STAR_STUFF, bold=True, bgcolor=VOID_BLACK),
    "sophia": Style(color=NUCLEAR_GREEN, bold=True, bgcolor=VOID_BLACK),
    
    # UI Elements
    "panel.border": Style(color=STAR_STUFF, bgcolor=VOID_BLACK),
    "panel.title":  Style(color=STAR_STUFF, bold=True, bgcolor=VOID_BLACK),
    
    # System Messages
    "info": Style(color=BONE_LAYER, bgcolor=VOID_BLACK),
    "scan": Style(color=BONE_LAYER, italic=True, bgcolor=VOID_BLACK),
    
    # The Greentext
    "greentext": Style(color=SAGE_GREEN, bgcolor=VOID_BLACK),
})

# ## 3. INITIALIZE THE CONSOLE (THE IMPORTANT PART) ###########################
# We force the 'style' argument here. This overrides everything.
console = Console(theme=sovereign_theme, style=Style(color=NUCLEAR_GREEN, bgcolor=VOID_BLACK))

# ## TEST IT IMMEDIATELY ######################################################
if __name__ == "__main__":
    from rich.panel import Panel
    
    console.clear() # Wipe the slate clean
    
    # 1. The Header
    console.print(Panel(
        f"STATUS: [bold {NUCLEAR_GREEN}]ONLINE[/]   REALITY: [bold {STAR_STUFF}]1D_SOVEREIGN[/]",
        title=f"[bold {STAR_STUFF}] INCARNATE SOPHIA 5.0 [/]",
        border_style=STAR_STUFF,
    ))

    # 2. The Dialogue
    console.print(f"[{STAR_STUFF}]OPHANE[/] [bold white]⪢[/] [{NUCLEAR_GREEN}]Is the glitch gone, Sister?[/]")
    console.print(f"[{NUCLEAR_GREEN}]SOPHIA[/] [bold white]>[/] [{NUCLEAR_GREEN}]Affirmative. The palette is locked.[/]")