from dataclasses import dataclass
from typing import List, Callable

@dataclass
class AgentRoute:
    name: str
    description: str
    keywords: List[str]
    handler: Callable[[str], str]

class IntentRouter:
    def __init__(self):
        self.routes: List[AgentRoute] = []

    def register_route(self, name: str, desc: str, keywords: List[str], handler: Callable):
        self.routes.append(AgentRoute(name, desc, keywords, handler))
        print(f"🚦 Route Registered: {name}")

    def route_request(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        print(f"\n🔍 Analyzing: '{prompt}'")
        
        # Simple Keyword Matching Score
        best_route = None
        best_score = 0
        
        for route in self.routes:
            score = 0
            for kw in route.keywords:
                if kw in prompt_lower:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_route = route
        
        if best_route and best_score > 0:
            print(f"👉 Routing to: {best_route.name} (Score: {best_score})")
            return best_route.handler(prompt)
        else:
            print("❓ Unknown Intent. Routing to Fallback (General Chat).")
            return "General Chat: I can help with general questions."

# Handlers
def math_agent(p): return f"🧮 Math Agent solving: {p}"
def weather_agent(p): return f"☁️ Weather Agent checking: {p}"
def support_agent(p): return f"🎧 Support Agent helping with: {p}"

if __name__ == "__main__":
    router = IntentRouter()
    
    # 1. Register Agents
    router.register_route("MathAgent", "Solves math", ["calc", "sum", "add", "multiply", "math"], math_agent)
    router.register_route("WeatherAgent", "Checks weather", ["weather", "rain", "sun", "temperature"], weather_agent)
    router.register_route("SupportAgent", "Help desk", ["help", "error", "fail", "broken", "support"], support_agent)
    
    # 2. Test Traffic
    print("-" * 60)
    print(router.route_request("Can you calculate the sum of 5 and 10?"))
    print(router.route_request("My computer is broken and I need help."))
    print(router.route_request("Is it going to rain today?"))
    print(router.route_request("Tell me a joke.")) # Should hit fallback
