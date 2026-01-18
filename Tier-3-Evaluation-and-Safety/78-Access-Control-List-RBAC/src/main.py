from dataclasses import dataclass
from typing import List, Dict, Set

# --- Data Structures ---

@dataclass
class User:
    username: str
    roles: List[str]

@dataclass
class Resource:
    name: str

class Action:
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    DEPLOY = "deploy"

# --- Policy Engine ---

class RBACSystem:
    def __init__(self):
        # Role -> Allowed Actions
        self.policy: Dict[str, Set[str]] = {
            "intern": {Action.READ},
            "engineer": {Action.READ, Action.WRITE},
            "admin": {Action.READ, Action.WRITE, Action.DELETE, Action.DEPLOY}
        }
        self.users: Dict[str, User] = {}

    def add_user(self, username: str, roles: List[str]):
        self.users[username] = User(username, roles)

    def check_permission(self, username: str, action: str) -> bool:
        if username not in self.users:
            print(f"❌ User '{username}' unknown.")
            return False

        user = self.users[username]
        for role in user.roles:
            allowed_actions = self.policy.get(role, set())
            if action in allowed_actions:
                print(f"✅ ALLOW: User '{username}' ({role}) can '{action}'.")
                return True
        
        print(f"⛔ DENY: User '{username}' cannot '{action}'.")
        return False

# --- Agent Integration ---

class GatekeeperAgent:
    def __init__(self, rbac: RBACSystem):
        self.rbac = rbac

    def execute_request(self, username: str, action: str, resource: str):
        print(f"\nLocked Request: {username} wants to {action} {resource}")
        
        if self.rbac.check_permission(username, action):
            print(f"🚀 EXECUTING: {action} on {resource}...")
        else:
            print("🛑 BLOCKED: Insufficient privileges.")

# --- Simulation ---

if __name__ == "__main__":
    # 1. Setup RBAC
    rbac = RBACSystem()
    rbac.add_user("alice_intern", ["intern"])
    rbac.add_user("bob_dev", ["engineer"])
    rbac.add_user("charlie_admin", ["admin"])
    
    # 2. Gatekeeper
    gatekeeper = GatekeeperAgent(rbac)
    
    # 3. Test Cases
    print("🔒 Starting Access Control Tests...")
    print("-" * 60)
    
    # Alice tries things
    gatekeeper.execute_request("alice_intern", Action.READ, "Docs") # OK
    gatekeeper.execute_request("alice_intern", Action.WRITE, "Codebase") # Fail
    
    # Bob tries things
    gatekeeper.execute_request("bob_dev", Action.WRITE, "Codebase") # OK
    gatekeeper.execute_request("bob_dev", Action.DEPLOY, "Production") # Fail
    
    # Charlie tries things
    gatekeeper.execute_request("charlie_admin", Action.DELETE, "Database") # OK
    gatekeeper.execute_request("charlie_admin", Action.DEPLOY, "Production") # OK
    
    # Hacker attempt
    gatekeeper.execute_request("dave_hacker", Action.READ, "Secrets") # Fail
