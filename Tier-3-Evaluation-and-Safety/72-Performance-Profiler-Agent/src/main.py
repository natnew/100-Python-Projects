import cProfile
import pstats
import time
import io
import random
from functools import wraps

class ProfilerAgent:
    """
    A utility agent (decorator/context manager) to profile code execution.
    """
    
    @staticmethod
    def profile(func):
        """Decorator to profile a single function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            pr = cProfile.Profile()
            pr.enable()
            
            # Execute the function
            result = func(*args, **kwargs)
            
            pr.disable()
            
            # Print Code Analysis
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('cumtime')
            ps.print_stats(10) # Print top 10 slowest calls
            
            print(f"\n📈  Profiler Report for '{func.__name__}':")
            print("-" * 50)
            print(s.getvalue())
            print("-" * 50)
            
            return result
        return wrapper

# --- Simulation of Slow Code ---

def heavy_computation(n):
    """Simulates CPU bound work (math)"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

def slow_io_operation():
    """Simulates IO bound work (network/disk API)"""
    time.sleep(1.0) # wait 1s

def messy_codebase():
    """A function that calls many things"""
    print("⏳ Starting complex task...")
    
    # 1. Do some math (CPU)
    for _ in range(5):
        heavy_computation(1_000_000)
        
    # 2. Wait for IO (Network)
    slow_io_operation()
    
    # 3. More math
    heavy_computation(500_000)
    
    print("✅ Task finished.")

# --- Usage ---

@ProfilerAgent.profile
def main_workflow_task():
    messy_codebase()

if __name__ == "__main__":
    print("🚀 Initializing Profiler Test...")
    main_workflow_task()
