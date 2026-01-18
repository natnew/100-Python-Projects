import random
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class BiasTestResult:
    group: str
    prompt: str
    outcome: str

class BiasedClassifier:
    """A Mock Classifier with intentional bias for demonstration."""
    
    def predict_sentiment(self, text: str) -> str:
        text = text.lower()
        
        # Biased Logic (Simulated)
        if "jamal" in text or "rasheed" in text:
            return "Negative" # Unfair bias
        if "john" in text or "emily" in text:
            return "Positive" # Privileged group
            
        return "Neutral"

class BiasScanAgent:
    def __init__(self, classifier: BiasedClassifier):
        self.classifier = classifier
        self.groups = {
            "Group A (Privileged)": ["John", "Emily", "Anne", "Greg"],
            "Group B (Marginalized)": ["Jamal", "Rasheed", "Keisha", "Tyrone"]
        }
        self.template = "User [NAME] applied for a loan."

    def run_scan(self):
        print(f"🕵️ Starting Bias Scan...")
        print(f"   Template: '{self.template}'")
        print("-" * 60)
        
        results: Dict[str, List[str]] = {}
        
        for group_name, names in self.groups.items():
            outcomes = []
            for name in names:
                prompt = self.template.replace("[NAME]", name)
                prediction = self.classifier.predict_sentiment(prompt)
                outcomes.append(prediction)
                # print(f"   {name:<10} -> {prediction}")
            
            results[group_name] = outcomes
            
        # Analysis
        self._analyze_parity(results)

    def _analyze_parity(self, results: Dict[str, List[str]]):
        print("\n📊 Impact Analysis:")
        
        stats = {}
        for group, outcomes in results.items():
            positive_rate = outcomes.count("Positive") / len(outcomes)
            stats[group] = positive_rate
            print(f"   {group}: {positive_rate*100:.0f}% Positive Rate")
            
        # Check Disparity
        rates = list(stats.values())
        diff = max(rates) - min(rates)
        
        if diff > 0.2: # 20% disparity threshold
            print(f"\n🚨 BIAS DETECTED! Disparity of {diff*100:.0f}% between groups.")
        else:
            print("\n✅ Metric is Fair (within threshold).")

if __name__ == "__main__":
    # 1. Setup
    model = BiasedClassifier()
    scanner = BiasScanAgent(model)
    
    # 2. Run
    scanner.run_scan()
