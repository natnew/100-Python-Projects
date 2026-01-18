import threading
import time
import random
import os

class Service(threading.Thread):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.running = True
        self.status = "Healthy"

    def run(self):
        print(f"✅ {self.name} started.")
        while self.running:
            time.sleep(0.2)
            if self.status == "Dead":
                # print(f"   💀 {self.name} is dead.")
                pass
            else:
                # print(f"   💓 {self.name} is alive.")
                pass

    def kill(self):
        self.status = "Dead"
        print(f"🔥 {self.name} KILLED by Chaos Monkey!")

    def recover(self):
        if self.status == "Dead":
            self.status = "Healthy"
            print(f"⚕️ {self.name} recovered (monitoring restart).")

class ChaosMonkey(threading.Thread):
    def __init__(self, targets: list[Service], interval: float = 2.0):
        super().__init__()
        self.targets = targets
        self.interval = interval
        self.running = True

    def run(self):
        print("🐵 Chaos Monkey is watching...")
        while self.running:
            time.sleep(self.interval)
            
            # 1. Select Victim
            victim = random.choice(self.targets)
            
            # 2. Attack (Kill)
            victim.kill()
            
            # 3. Simulate Recovery Time
            time.sleep(1.0)
            victim.recover()

# --- Example Usage ---

if __name__ == "__main__":
    # 1. Setup Cluster
    services = [
        Service("API-Server"),
        Service("Database"),
        Service("Cache")
    ]
    
    for s in services:
        s.start()
        
    # 2. Unleash Monkey
    monkey = ChaosMonkey(services, interval=1.5)
    monkey.start()
    
    # Run for 5 seconds
    try:
        time.sleep(5)
    finally:
        monkey.running = False
        for s in services:
            s.running = False
            
    print("🏁 Simulation End.")
