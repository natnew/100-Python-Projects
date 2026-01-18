import time
from dataclasses import dataclass

@dataclass
class HardwareSpec:
    name: str
    power_watts: float # TDP (Thermal Design Power)

@dataclass
class Region:
    name: str
    carbon_intensity: float # gCO2e per kWh

class CarbonTracker:
    def __init__(self, hardware: HardwareSpec, region: Region):
        self.hardware = hardware
        self.region = region
        self.start_time = None
        self.accumulated_energy_kwh = 0.0

    def start_task(self):
        self.start_time = time.time()
        print(f"🌱 Starting tracking on {self.hardware.name} in {self.region.name}...")

    def stop_task(self) -> float:
        if not self.start_time:
            return 0.0
        
        duration_seconds = time.time() - self.start_time
        hours = duration_seconds / 3600.0
        
        # Energy = Power (kW) * Time (hours)
        energy_kwh = (self.hardware.power_watts / 1000.0) * hours
        self.accumulated_energy_kwh += energy_kwh
        
        # Carbon = Energy (kWh) * Intensity (g/kWh)
        carbon_g = energy_kwh * self.region.carbon_intensity
        
        print(f"🛑 Task finished in {duration_seconds:.4f}s")
        print(f"   ⚡ Energy: {energy_kwh:.6f} kWh")
        print(f"   ☁️ Carbon: {carbon_g:.6f} gCO2e")
        
        self.start_time = None
        return carbon_g

    def estimate_training(self, hours: float) -> str:
        """Estimate footprint for a long training run."""
        energy = (self.hardware.power_watts / 1000.0) * hours
        carbon = energy * self.region.carbon_intensity
        
        # Equivalent miles driven (approx 400g/mile for avg car)
        miles = carbon / 400.0
        
        return f"{hours}h Training = {carbon/1000:.2f} kgCO2e (~{miles:.1f} miles driven)"

if __name__ == "__main__":
    # Specs
    gpu_h100 = HardwareSpec("NVIDIA H100", 700.0) # 700W TDP
    cpu_generic = HardwareSpec("Generic CPU", 100.0)
    
    # Regions
    us_east = Region("US-East (Virginia)", 367.0) # Coal/Gas heavy
    eu_nordic = Region("EU-Nordic (Sweden)", 12.0) # Hydro/Wind heavy
    
    # 1. Track a quick simulated task
    tracker = CarbonTracker(cpu_generic, us_east)
    tracker.start_task()
    time.sleep(0.5) # Simulate work
    tracker.stop_task()
    
    print("-" * 60)
    
    # 2. Compare Training Impact
    tracker_dirty = CarbonTracker(gpu_h100, us_east)
    print(f"🏭 Dirty Region: {tracker_dirty.estimate_training(24)}")
    
    tracker_clean = CarbonTracker(gpu_h100, eu_nordic)
    print(f"🌲 Clean Region: {tracker_clean.estimate_training(24)}")
