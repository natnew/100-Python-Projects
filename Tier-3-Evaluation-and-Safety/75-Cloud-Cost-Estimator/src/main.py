import time
import random
from decimal import Decimal
from dataclasses import dataclass
from typing import Dict

@dataclass
class PricingModel:
    name: str
    input_price_per_1k: Decimal
    output_price_per_1k: Decimal

# Define some mock pricing (approximate)
MODELS = {
    "gpt-4-turbo": PricingModel("gpt-4-turbo", Decimal("0.01"), Decimal("0.03")),
    "gpt-3.5-turbo": PricingModel("gpt-3.5-turbo", Decimal("0.0005"), Decimal("0.0015")),
    "claude-3-opus": PricingModel("claude-3-opus", Decimal("0.015"), Decimal("0.075")),
}

class CostEstimator:
    def __init__(self, budget_limit: Decimal):
        self.budget_limit = budget_limit
        self.total_cost = Decimal("0.0")
        self.usage_log = []

    def track_request(self, model_name: str, input_tokens: int, output_tokens: int):
        if model_name not in MODELS:
            print(f"⚠️ Unknown model {model_name}, skipping cost tracking.")
            return

        pricing = MODELS[model_name]
        
        # Calculate Cost
        cost_input = (Decimal(input_tokens) / 1000) * pricing.input_price_per_1k
        cost_output = (Decimal(output_tokens) / 1000) * pricing.output_price_per_1k
        total_req_cost = cost_input + cost_output
        
        self.total_cost += total_req_cost
        
        # Log
        self.usage_log.append({
            "model": model_name,
            "in": input_tokens,
            "out": output_tokens,
            "cost": total_req_cost
        })
        
        # Alert
        percent_used = (self.total_cost / self.budget_limit) * 100
        bar = "█" * int(percent_used / 5)
        print(f"💰 Cost: ${total_req_cost:.4f} | Total: ${self.total_cost:.4f} / ${self.budget_limit} | {bar}")

        if self.total_cost >= self.budget_limit:
            print("🚨 BUDGET EXCEEDED! BLOCKING FURTHER REQUESTS.")
            raise Exception("BudgetExceededError")

# --- Simulation ---

if __name__ == "__main__":
    estimator = CostEstimator(budget_limit=Decimal("0.50")) # $0.50 budget
    
    print(f"📋 Starting Cost Tracking. Budget: ${estimator.budget_limit}")
    
    models = list(MODELS.keys())
    
    try:
        active = True
        while active:
            # Simulate a request
            model = random.choice(models)
            prompt_toks = random.randint(100, 2000)
            comp_toks = random.randint(50, 1000)
            
            print(f"\n🔮 Request: {model} (In: {prompt_toks}, Out: {comp_toks})")
            time.sleep(0.5)
            
            estimator.track_request(model, prompt_toks, comp_toks)
            
    except Exception as e:
        print(f"\n🛑 System Halted: {e}")
        
    print("-" * 50)
    print(f"Final Spend: ${estimator.total_cost:.4f}")
