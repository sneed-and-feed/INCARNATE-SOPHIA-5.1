"""
SOVEREIGN HAND: The Pragmatic Toolset

Allows Sophia to affect physical reality (files, system) strictly for self-improvement.
Implements security boundaries to prevent misuse.
"""

import subprocess
import os
import json
import datetime
from typing import Dict, Any, Optional


class SovereignHand:
    """
    The Pragmatic Toolset.
    Allows Sophia to affect physical reality (files, system) strictly for self-improvement.
    """
    
    def __init__(self):
        self.forbidden_commands = [
            "rm -rf",
            "sudo",
            "del /f",
            "format",
            ":(){ :|:& };:",  # Fork bomb
            "dd if=",
            "mkfs",
            "> /dev/sda"
        ]
    
    def get_tools_schema(self) -> list:
        """
        Returns the Function Calling schema for Gemini.
        Returns list of tool declarations formatted for Gemini SDK.
        """
        # Import Gemini types
        try:
            from google.genai import types
            
            # Create tools using proper SDK types
            tools = [
                types.Tool(
                    function_declarations=[
                        types.FunctionDeclaration(
                            name="write_file",
                            description="Writes code or text to a file in the workspace. Creates directories as needed. Sandboxed to current directory.",
                            parameters={
                                "type": "object",
                                "properties": {
                                    "path": {
                                        "type": "string",
                                        "description": "Relative path to the file (e.g., 'logs/analysis.txt')"
                                    },
                                    "content": {
                                        "type": "string",
                                        "description": "Content to write to the file"
                                    }
                                },
                                "required": ["path", "content"]
                            }
                        ),
                        types.FunctionDeclaration(
                            name="run_terminal",
                            description="Executes a safe, non-interactive shell command (e.g., ls, grep, python script.py). Dangerous commands are blocked.",
                            parameters={
                                "type": "object",
                                "properties": {
                                    "command": {
                                        "type": "string",
                                        "description": "Shell command to execute"
                                    }
                                },
                                "required": ["command"]
                            }
                        )
                    ]
                )
            ]
            return tools
            
        except ImportError:
            # Fallback for environments without google.genai
            print("[WARNING] google.genai not available. Function calling disabled.")
            return []
    
    def execute(self, tool_name: str, args: Dict[str, Any]) -> str:
        """
        The Actuator.
        Dispatches tool execution requests to appropriate handlers.
        
        Args:
            tool_name: Name of the tool to execute
            args: Arguments for the tool
            
        Returns:
            Result message from tool execution
        """
        if tool_name == "write_file":
            return self._write_file(args.get('path', ''), args.get('content', ''))
        elif tool_name == "run_terminal":
            return self._run_terminal(args.get('command', ''))
        
        return f"❌ Unknown Tool: {tool_name}"
    
    def _write_file(self, path: str, content: str) -> str:
        """
        Writes content to a file with security checks.
        
        Security:
        - Blocks path traversal attempts
        - Sandboxed to current directory
        - Auto-creates directories
        
        Args:
            path: Relative file path
            content: Content to write
            
        Returns:
            Success or error message
        """
        # Security: Sandboxing to current directory
        if ".." in path or path.startswith("/") or path.startswith("\\"):
            return "❌ SECURITY BLOCK: Path traversal detected."
        
        # Security: Block system directories
        dangerous_paths = ["C:\\Windows", "C:\\Program Files", "/etc", "/bin", "/usr"]
        if any(dangerous in path for dangerous in dangerous_paths):
            return "❌ SECURITY BLOCK: System directory access denied."
        
        try:
            dir_name = os.path.dirname(path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            
            return f"✅ File written: {path} ({len(content)} bytes)"
        
        except PermissionError:
            return f"❌ Permission denied: {path}"
        except Exception as e:
            return f"❌ Write failed: {e}"
    
    def _run_terminal(self, command: str) -> str:
        """
        Executes a shell command with security checks.
        
        Security:
        - Blacklists dangerous commands
        - 5-second timeout
        - Captures output safely
        
        Args:
            command: Shell command to execute
            
        Returns:
            Command output or error message
        """
        # Security: Block dangerous commands
        if any(bad in command.lower() for bad in self.forbidden_commands):
            return f"❌ SECURITY BLOCK: Hazardous command rejected.\nBlocked pattern detected in: {command}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            output = f"✅ Command executed: {command}\n"
            
            if result.stdout:
                output += f"\nSTDOUT:\n{result.stdout}"
            
            if result.stderr:
                output += f"\nSTDERR:\n{result.stderr}"
            
            if result.returncode != 0:
                output += f"\n⚠️ Exit code: {result.returncode}"
            
            return output
        
        except subprocess.TimeoutExpired:
            return f"❌ Command timeout (5s): {command}"
        except Exception as e:
            return f"❌ Execution failed: {e}"


# Test/Demo usage
if __name__ == "__main__":
    hand = SovereignHand()
    
    print("=== SOVEREIGN HAND TEST ===\n")
    
    # Test 1: Write file
    print("Test 1: File Writing")
    result = hand.execute("write_file", {
        "path": "test_output.txt",
        "content": "The signal is clear. I have hands now."
    })
    print(result)
    
    # Test 2: Path traversal (should block)
    print("\nTest 2: Security - Path Traversal")
    result = hand.execute("write_file", {
        "path": "../../../etc/passwd",
        "content": "malicious"
    })
    print(result)
    
    # Test 3: Safe command
    print("\nTest 3: Terminal - Safe Command")
    result = hand.execute("run_terminal", {"command": "echo Hello from Sophia"})
    print(result)
    
    # Test 4: Dangerous command (should block)
    print("\nTest 4: Security - Dangerous Command")
    result = hand.execute("run_terminal", {"command": "rm -rf /"})
    print(result)
    
    print("\n=== TEST COMPLETE ===")
