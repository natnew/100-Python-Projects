from typing import Callable, Any, Set
from enum import Enum
from dataclasses import dataclass

class SecurityError(Exception):
    """Raised when a permission check fails."""
    pass

class ToolScope(str, Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    NETWORK = "network"

@dataclass
class ToolMetadata:
    name: str
    required_scopes: Set[ToolScope]

class PermissionSandbox:
    def __init__(self, agent_scopes: Set[ToolScope]):
        """
        Args:
            agent_scopes: The scopes granted to the current agent session.
        """
        self.agent_scopes = agent_scopes
        self.registry: dict[str, tuple[Callable, ToolMetadata]] = {}

    def register(self, name: str, scopes: Set[ToolScope]):
        """Register a tool with required permissions."""
        def decorator(func: Callable):
            meta = ToolMetadata(name=name, required_scopes=scopes)
            self.registry[name] = (func, meta)
            return func
        return decorator

    def execute(self, tool_name: str, **kwargs) -> Any:
        """Execute tool if permissions allow."""
        if tool_name not in self.registry:
            raise KeyError(f"Tool {tool_name} not found")

        func, meta = self.registry[tool_name]

        # check permissions
        # Logic: Agent must have ALL required scopes? Or ANY?
        # Usually implies containment: Agent scopes must be a superset of required.
        missing = meta.required_scopes - self.agent_scopes
        if missing:
            raise SecurityError(
                f"Access Denied for tool '{tool_name}'. "
                f"Missing scopes: {[s.value for s in missing]}. "
                f"Agent has: {[s.value for s in self.agent_scopes]}."
            )
        
        print(f"DEBUG: Access Granted to {tool_name}")
        return func(**kwargs)

# --- Example Usage ---

# Define a Restricted Agent (Analyst)
analyst_sandbox = PermissionSandbox(agent_scopes={ToolScope.READ, ToolScope.NETWORK})

# Define a Powerful Agent (Admin)
admin_sandbox = PermissionSandbox(agent_scopes={ToolScope.READ, ToolScope.WRITE, ToolScope.ADMIN})

# Tools
def read_logs(limit: int):
    return f"Reading {limit} logs..."

def delete_database():
    return "DATABASE DELETED"

# Registering happens on the sandbox instance (in reality, tools might declare scopes statically, 
# and the sandbox enforces them dynamically. For this pattern, we register to the sandbox instance).
# Note: In a real system, the Registry and Sandbox are separate. 
# Here we bundle them for the 'Sandbox' pattern demo.

analyst_sandbox.register("read_logs", {ToolScope.READ})(read_logs)
analyst_sandbox.register("delete_db", {ToolScope.ADMIN, ToolScope.WRITE})(delete_database)

if __name__ == "__main__":
    print("--- Scenario 1: Analyst tries to read logs ---")
    try:
        res = analyst_sandbox.execute("read_logs", limit=10)
        print(f"✅ Result: {res}")
    except SecurityError as e:
        print(f"❌ {e}")

    print("\n--- Scenario 2: Analyst tries to delete DB ---")
    try:
        res = analyst_sandbox.execute("delete_db")
        print(f"✅ Result: {res}")
    except SecurityError as e:
        print(f"🛡️ BLOCKED: {e}")
