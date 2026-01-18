import random
import time
from typing import List, Optional

class Server:
    def __init__(self, name: str, weight: int = 1):
        self.name = name
        self.weight = weight
        self.is_healthy = True
        self.active_requests = 0

    def handle(self, request_id: str):
        if not self.is_healthy:
            print(f"   ❌ {self.name} is DEAD. Cannot handle {request_id}.")
            return
            
        self.active_requests += 1
        print(f"   ⚙️ {self.name} handling {request_id} (Load: {self.active_requests})")
        time.sleep(0.1) # Simulate work
        self.active_requests -= 1

    def crash(self):
        print(f"🔥 {self.name} CRASHED!")
        self.is_healthy = False

    def heal(self):
        print(f"⚕️ {self.name} recovered.")
        self.is_healthy = True

class LoadBalancer:
    def __init__(self, servers: List[Server]):
        self.servers = servers
        self.current_index = 0

    def get_server(self, strategy: str = "round_robin") -> Optional[Server]:
        # 1. Filter Healthy
        healthy = [s for s in self.servers if s.is_healthy]
        if not healthy:
            return None

        # 2. Strategy
        if strategy == "round_robin":
            # Simple RR among healthy
            server = healthy[self.current_index % len(healthy)]
            self.current_index += 1
            return server
            
        elif strategy == "weighted":
            # Weighted Random selection
            # A(3), B(1) -> [A, A, A, B]
            candidates = []
            for s in healthy:
                candidates.extend([s] * s.weight)
            return random.choice(candidates)
            
        elif strategy == "least_conn":
            # Find min active requests
            return min(healthy, key=lambda s: s.active_requests)
            
        return healthy[0]

    def route(self, request_id: str, strategy: str = "round_robin"):
        target = self.get_server(strategy)
        if target:
            target.handle(request_id)
        else:
            print(f"   ⚠️ 503 Service Unavailable (No servers) for {request_id}")

# --- Example Usage ---

if __name__ == "__main__":
    servers = [
        Server("S1-Powerful", weight=3),
        Server("S2-Weak", weight=1),
        Server("S3-Backup", weight=1)
    ]
    
    lb = LoadBalancer(servers)
    
    # 1. Round Robin
    print("\n--- Strategy: Round Robin ---")
    for i in range(5):
        lb.route(f"Req-{i}", "round_robin")
        
    # 2. Weighted (S1 should get ~75%)
    print("\n--- Strategy: Weighted ---")
    for i in range(10):
        lb.route(f"WReq-{i}", "weighted")
        
    # 3. Failover
    print("\n--- Failover Test ---")
    servers[0].crash() # S1 dies
    lb.route("Req-Critical", "round_robin") # Should go to S2 or S3
