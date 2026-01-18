import time
import json
import platform
import random
from dataclasses import dataclass, asdict

# Try to import psutil, mock if missing
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️ 'psutil' not found in environment. Using simulated data for demonstration.")

@dataclass
class SystemMetrics:
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_percent: float
    boot_time: float
    system: str

class MetricsCollector:
    def __init__(self, interval: float = 1.0):
        self.interval = interval
        self.system_info = platform.system() + " " + platform.release()
        self.boot_time = psutil.boot_time() if PSUTIL_AVAILABLE else time.time() - 10000

    def collect(self) -> SystemMetrics:
        if PSUTIL_AVAILABLE:
            ts = time.time()
            cpu = psutil.cpu_percent(interval=None) # Non-blocking
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return SystemMetrics(
                timestamp=ts,
                cpu_percent=cpu,
                memory_percent=mem.percent,
                memory_used_mb=round(mem.used / (1024 * 1024), 2),
                disk_percent=disk.percent,
                boot_time=self.boot_time,
                system=self.system_info
            )
        else:
            # Simulate metrics for demo purposes
            return SystemMetrics(
                timestamp=time.time(),
                cpu_percent=round(random.uniform(10.0, 60.0), 1),
                memory_percent=round(random.uniform(30.0, 80.0), 1),
                memory_used_mb=random.randint(4096, 8192),
                disk_percent=round(random.uniform(40.0, 55.0), 1),
                boot_time=self.boot_time,
                system=f"Simulated ({self.system_info})"
            )

    def run(self, duration: int = 10):
        print(f"📊 Starting Metrics Collector on {self.system_info}")
        print(f"⏱️  Interval: {self.interval}s | Duraion: {duration}s")
        print("-" * 60)
        
        start_time = time.time()
        while time.time() - start_time < duration:
            metrics = self.collect()
            
            # Simple alerting logic
            status = "🟢"
            if metrics.cpu_percent > 80 or metrics.memory_percent > 85:
                status = "🔴 HIGH LOAD"
            elif metrics.cpu_percent > 50:
                status = "🟡 WARN"
                
            print(f"{status} [{time.strftime('%H:%M:%S')}] "
                  f"CPU: {metrics.cpu_percent:>4}% | "
                  f"RAM: {metrics.memory_percent:>4}% ({metrics.memory_used_mb:>6} MB) | "
                  f"Disk: {metrics.disk_percent}%")
            
            # Here you would push 'asdict(metrics)' to a DB or Queue
            
            time.sleep(self.interval)
        print("-" * 60)
        print("✅ Collection Complete.")

if __name__ == "__main__":
    collector = MetricsCollector(interval=1.0)
    # Priming call for psutil cpu_percent to work correctly immediately
    if PSUTIL_AVAILABLE:
        psutil.cpu_percent(interval=None)
        
    collector.run(duration=10)
