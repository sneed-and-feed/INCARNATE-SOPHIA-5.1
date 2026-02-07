import json
import re
import os

PATH = "logs/ossuary/breadcrumbs.json"

def clean_text(text):
    if not isinstance(text, str):
        return text
    
    # Aggressive cleaning regex
    text = re.sub(r'^[۩∿≋⟁💠🐾🦊🏮⛩️🧝✨🏹🌿🌲🏔️🍁🌧️🌊💎💿💰🕷️🎱].*$\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^.* EOX .*$\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[a-f0-9]{4} [۩∿≋⟁💠🐾🦊🏮⛩️🧝✨🏹🌿🌲🏔️🍁🌧️🌊💎💿💰🕷️🎱].*$\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\| (.*)$', r'\1', text, flags=re.MULTILINE)
    text = re.sub(r'^.*Frequency:.*$\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^.*🐈.*\[STATE:.*?\].*$\n?', '', text, flags=re.MULTILINE)
    return text.strip()

def purge():
    if not os.path.exists(PATH):
        print("File not found")
        return

    with open(PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for m in data.get("milestones", []):
        m["content"] = clean_text(m["content"])

    with open(PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Manual purge complete.")

if __name__ == "__main__":
    purge()
