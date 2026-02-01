import sys
import os
import traceback
import asyncio

print("--- [DEBUG] SYSTEM BOOT SEQUENCE INITIATED ---")
print(f"--- [DEBUG] CWD: {os.getcwd()}")

# 1. Force the current directory into the Python Path
sys.path.append(os.getcwd())
print("--- [DEBUG] PYTHONPATH PATCHED ---")

try:
    # 2. Attempt the Import (This is usually where it dies silently)
    print("--- [DEBUG] IMPORTING SOPHIA.MAIN... ---")
    import sophia.main
    print("--- [DEBUG] IMPORT SUCCESSFUL ---")

except ImportError as e:
    print(f"\n[!!!] CRITICAL IMPORT ERROR: {e}")
    print("Hint: Check for missing __init__.py files or circular imports.")
    traceback.print_exc()
    input("\nPress ENTER to exit...")
    sys.exit(1)
except Exception as e:
    print(f"\n[!!!] CRITICAL MODULE LEVEL ERROR: {e}")
    traceback.print_exc()
    input("\nPress ENTER to exit...")
    sys.exit(1)

# 3. Attempt Execution
print("--- [DEBUG] EXECUTING ASYNC LOOP... ---")
try:
    asyncio.run(sophia.main.main())
except KeyboardInterrupt:
    print("\n[DEBUG] USER INTERRUPT.")
except Exception as e:
    print(f"\n[!!!] RUNTIME CRASH: {e}")
    traceback.print_exc()
    input("\nPress ENTER to exit...")