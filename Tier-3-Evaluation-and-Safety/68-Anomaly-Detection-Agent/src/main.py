import random
import math
import collections
from typing import List

class AnomalyDetector:
    def __init__(self, window_size: int = 20, threshold: float = 3.0):
        self.window = collections.deque(maxlen=window_size)
        self.threshold = threshold

    def process(self, value: float) -> bool:
        """Returns True if anomaly detected."""
        is_anomaly = False
        stats = ""
        
        if len(self.window) >= 2:
            mean = sum(self.window) / len(self.window)
            variance = sum((x - mean) ** 2 for x in self.window) / len(self.window)
            std_dev = math.sqrt(variance)
            
            if std_dev > 0:
                z_score = (value - mean) / std_dev
                stats = f"(Mean: {mean:.2f}, StdDev: {std_dev:.2f}, Z: {z_score:.2f})"
                
                if abs(z_score) > self.threshold:
                    is_anomaly = True
            
        self.window.append(value)
        
        status = "🔴 ANOMALY" if is_anomaly else "🟢 Normal"
        print(f"Val: {value:6.2f} | {status} {stats}")
        return is_anomaly

# --- Example Usage ---

if __name__ == "__main__":
    detector = AnomalyDetector(window_size=10, threshold=2.5)
    
    print("--- Stream Started ---")
    
    # 1. Normal Traffic
    for _ in range(15):
        # Baseline around 50 +/- 5
        val = 50 + random.uniform(-5, 5)
        detector.process(val)
        
    # 2. Spike (Web Server Overload)
    print("\n--- Injecting Spike ---")
    detector.process(120.0) 
    
    # 3. Drop (Database Crash)
    print("\n--- Injecting Drop ---")
    detector.process(0.0)
    
    # 4. Return to normal
    print("\n--- Returning to Normal ---")
    for _ in range(5):
        val = 50 + random.uniform(-5, 5)
        detector.process(val)
