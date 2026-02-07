import json
import os
import sys
import re

# Mocking parts of main for testing
sys.path.append('.')
from sophia.cortex.lethe import LetheEngine

def test_deep_clean():
    lethe = LetheEngine()
    lethe.breadcrumb_path = "test_breadcrumbs.json"
    
    dirty_milestones = [
        {
            "content": "\n\u06e9 dc1a \u06e9\n| CH\u25ccA\u00b0O\u25ccS\n\u06e9 \u27c1 \u223f EOX \u06e9 \u27c1 \u223f\n\nReal content",
            "meta": "Cat Logic",
            "timestamp": 1000
        },
        {
            "content": "| Pipe text\nFrequency: Low\n[STATE: COMPUTE]\nClean content",
            "meta": "Cat Logic",
            "timestamp": 2000
        }
    ]
    
    print("[*] Testing Lethe.scrub()...")
    cleaned_1 = lethe.scrub(dirty_milestones[0]["content"])
    print(f"Dirty 1 output:\n'{cleaned_1}'")
    assert "EOX" not in cleaned_1
    assert "dc1a" not in cleaned_1
    assert "Real content" in cleaned_1
    
    cleaned_2 = lethe.scrub(dirty_milestones[1]["content"])
    print(f"Dirty 2 output:\n'{cleaned_2}'")
    assert "Frequency" not in cleaned_2
    assert "STATE" not in cleaned_2
    assert "Pipe text" in cleaned_2
    assert "Clean content" in cleaned_2

    print("[*] Testing save_breadcrumbs()...")
    lethe.save_breadcrumbs({"name": "Test"}, milestones=dirty_milestones)
    
    with open("test_breadcrumbs.json", "r", encoding="utf-8") as f:
        saved_data = json.load(f)
        
    for m in saved_data["milestones"]:
        print(f"Checking saved milestone: {m['content']}")
        assert "EOX" not in m["content"]
        assert "Frequency" not in m["content"]

    print("[*] Clean up...")
    if os.path.exists("test_breadcrumbs.json"):
        os.remove("test_breadcrumbs.json")
    print("\n[SUCCESS] Deep clean verification passed!")

if __name__ == "__main__":
    test_deep_clean()
