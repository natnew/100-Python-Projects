import random
import time
import math
from typing import List
from dataclasses import dataclass

@dataclass
class DistributionStats:
    count: int
    mean: float
    std_dev: float

class DriftMonitor:
    def __init__(self, reference_data: List[float], threshold_std_devs: float = 2.0):
        self.ref_stats = self._calculate_stats(reference_data)
        self.threshold = threshold_std_devs
        self.window: List[float] = []
        self.window_size = 20 # Small window for demo

        print(f"📊 Reference Baseline: Mean={self.ref_stats.mean:.2f}, StdDev={self.ref_stats.std_dev:.2f}")

    def _calculate_stats(self, data: List[float]) -> DistributionStats:
        n = len(data)
        if n == 0: return DistributionStats(0, 0.0, 0.0)
        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / n
        return DistributionStats(n, mean, math.sqrt(variance))

    def add_point(self, value: float):
        self.window.append(value)
        if len(self.window) > self.window_size:
            self.window.pop(0)
            
        if len(self.window) == self.window_size:
            self._check_drift()

    def _check_drift(self):
        curr_stats = self._calculate_stats(self.window)
        
        # Simple Mean Shift Test (Z-Test logic)
        # Is the current mean significantly different from reference mean?
        diff = abs(curr_stats.mean - self.ref_stats.mean)
        std_threshold = self.ref_stats.std_dev * self.threshold
        
        status = "✅ Stable"
        if diff > std_threshold:
            status = "🚨 DRIFT DETECTED"
            
        print(f"Time {time.strftime('%H:%M:%S')} | Window Mean: {curr_stats.mean:.2f} | Ref Mean: {self.ref_stats.mean:.2f} | Diff: {diff:.2f} | {status}")

# --- Simulation ---

if __name__ == "__main__":
    # 1. Create Baseline (Normal Distribution, Mean=50, SD=10)
    baseline = [random.gauss(50, 10) for _ in range(1000)]
    monitor = DriftMonitor(baseline)
    
    print("\n--- Stream Started (Normal) ---")
    for _ in range(15):
        val = random.gauss(50, 10) # Matches baseline
        monitor.add_point(val)
        time.sleep(0.1)
        
    print("\n--- Stream Shift (Drift: Mean shifts to 80) ---")
    for _ in range(15):
        val = random.gauss(80, 10) # Shifted mean
        monitor.add_point(val)
        time.sleep(0.1)

    print("\n--- Stream Return (Normal) ---")
    for _ in range(15):
        val = random.gauss(50, 10) # Back to normal
        monitor.add_point(val)
        time.sleep(0.1)
