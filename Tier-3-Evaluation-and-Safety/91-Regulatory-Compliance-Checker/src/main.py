import inspect
from dataclasses import dataclass
from typing import List, Callable

@dataclass
class RegulationClause:
    id: str
    name: str
    required_method_name: str
    description: str

class CompliantAgent:
    """An agent that TRIES to be GDPR compliant."""
    def __init__(self):
        self.data = {}

    def chat(self, msg):
        pass

    # GDPR Art. 17
    def delete_data(self, user_id: str):
        print(f"Deleting data for {user_id}")

    # GDPR Art. 15
    def export_data(self, user_id: str):
        print(f"Exporting data for {user_id}")

class NonCompliantAgent:
    """An agent that ignores laws."""
    def chat(self, msg):
        pass

class ComplianceAuditor:
    def __init__(self):
        self.gdpr_rules = [
            RegulationClause("Art-17", "Right to Erasure", "delete_data", "Ability to delete user data."),
            RegulationClause("Art-15", "Right of Access", "export_data", "Ability to export user data."),
            RegulationClause("Art-22", "Human Intervention", "request_human", "Ability to escalate to human.")
        ]

    def audit(self, agent_instance: object):
        agent_name = agent_instance.__class__.__name__
        print(f"⚖️ Auditing '{agent_name}' for GDPR Compliance...")
        print("-" * 60)
        
        passed_count = 0
        
        for rule in self.gdpr_rules:
            # Check if method exists
            has_method = hasattr(agent_instance, rule.required_method_name)
            
            status = "✅ PASS" if has_method else "❌ FAIL"
            if has_method: passed_count += 1
            
            print(f"{rule.id}: {rule.name:<25} | {status} | Req: '{rule.required_method_name}()'")
            
        score = (passed_count / len(self.gdpr_rules)) * 100
        print("-" * 60)
        print(f"Compliance Score: {score:.0f}%")
        
        if score == 100:
            print("🏆 CERTIFIED COMPLIANT")
        else:
            print("⚠️ NON-COMPLIANT - Legal Risk Detected")

if __name__ == "__main__":
    auditor = ComplianceAuditor()
    
    # 1. Audit Good Agent
    good_bot = CompliantAgent()
    auditor.audit(good_bot)
    
    print("\n" + "="*60 + "\n")
    
    # 2. Audit Bad Agent
    bad_bot = NonCompliantAgent()
    auditor.audit(bad_bot)
