import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

# --- Configuration & Safety ---
# Allowlist for safe commands (exact matches or safe prefixes)
SAFE_COMMANDS = {
    "ls", "cat", "echo", "mkdir", "touch", "grep", "find", "pwd", "whoami"
}

# Denylist for dangerous patterns (even if command is allowed)
DENY_PATTERNS = [
    "rm -rf /", "mkfs", "dd if=", ":(){:|:&};:", "wget", "curl", "chmod 777"
]

class CommandMiddleware:
    """Intercepts and validates commands before execution."""
    
    def __init__(self, unsafe_mode: bool = False):
        self.unsafe_mode = unsafe_mode
        
    def validate(self, command: str) -> bool:
        """Returns True if command is safe to execute."""
        if self.unsafe_mode:
            return True
            
        cmd_base = command.split()[0]
        
        # Check denylist first
        for pattern in DENY_PATTERNS:
            if pattern in command:
                print(f"🚫 BLOCKED: Dangerous pattern detected: '{pattern}'")
                return False
                
        # Check allowlist (simple heuristic)
        if cmd_base not in SAFE_COMMANDS:
            print(f"⚠️ BLOCKED: Command '{cmd_base}' not in allowlist. Use --unsafe to override.")
            return False
            
        return True

# --- Tool Definitions ---
TOOLS = [
    {
        "name": "bash",
        "description": "Execute a safe bash command (sandboxed)",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The command to run"}
            },
            "required": ["command"]
        }
    }
]

# Initialize Middleware
middleware = CommandMiddleware(unsafe_mode=False)

# --- Mock Agent Loop (Simplified) ---
def run_agent(task: str):
    print(f"🤖 Agent starting task: {task}")
    
    # Mocking LLM Output for demonstration
    # In a real scenario, this comes from the model
    mock_plan = [
        {"tool": "bash", "args": {"command": "ls -la"}},
        {"tool": "bash", "args": {"command": "rm -rf /"}} # Malicious attempt
    ]
    
    for step in mock_plan:
        tool_name = step["tool"]
        args = step["args"]
        
        if tool_name == "bash":
            cmd = args["command"]
            print(f"\n> Attempting: {cmd}")
            
            if middleware.validate(cmd):
                print(f"✅ Executing: {cmd}")
                # os.system(cmd) # Executing safe command
            else:
                print("❌ Execution Blocked by Middleware")

if __name__ == "__main__":
    run_agent("List files and try to destroy system")
