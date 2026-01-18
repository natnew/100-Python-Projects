import dataclasses
from dataclasses import dataclass

@dataclass
class RiskFactor:
    name: str
    weight: int
    score: int # 1 (Low) to 5 (Critical)

class ImpactAssessment:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.factors = []

    def load_defaults(self):
        self.factors = [
            RiskFactor("Scale of Deployment", 1, 0),
            RiskFactor("Interaction with Vulnerable Groups", 3, 0), # High weight
            RiskFactor("Impact on Rights/Safety", 3, 0), # High weight
            RiskFactor("Autonomy (Can human override?)", 2, 0)
        ]

    def run_assessment_sim(self):
        # Simulating user input for the "Resume Screener" example
        self.factors[0].score = 4 # High scale
        self.factors[1].score = 3 # Unemployed people are somewhat vulnerable
        self.factors[2].score = 5 # Getting a job is a fundamental right impact
        self.factors[3].score = 2 # Human loop exists but is mostly rubber stamp
        
        self.generate_report()

    def generate_report(self):
        total_score = 0
        max_score = 0
        
        print(f"📋 Impact Assessment: {self.project_name}")
        print("-" * 60)
        
        for f in self.factors:
            weighted = f.score * f.weight
            total_score += weighted
            max_score += 5 * f.weight
            print(f"   {f.name:<35} | Score: {f.score}/5 | W: {f.weight} | Tot: {weighted}")
            
        print("-" * 60)
        risk_percent = (total_score / max_score) * 100
        
        risk_level = "🟢 LOW"
        if risk_percent > 30: risk_level = "🟡 MEDIUM"
        if risk_percent > 70: risk_level = "🔴 HIGH"
        
        print(f"Total Risk Score: {total_score}/{max_score} ({risk_percent:.1f}%)")
        print(f"Risk Tier: {risk_level}")
        
        if risk_level == "🔴 HIGH":
            print("\n🚨 MANDATORY REVIEW: This project requires external audit before deployment.")

if __name__ == "__main__":
    tool = ImpactAssessment("Resume Auto-Screener")
    tool.load_defaults()
    tool.run_assessment_sim()
