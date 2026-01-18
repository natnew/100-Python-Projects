import time
from enum import Enum
from typing import Callable, Any

class State(Enum):
    CLOSED = "CLOSED"     # Normal
    OPEN = "OPEN"         # Failing fast
    HALF_OPEN = "HALF_OPEN" # Testing recovery

class CircuitBreakerOpenError(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 2.0):
        self.state = State.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0

    def call(self, func: Callable, *args, **kwargs) -> Any:
        # Check State
        if self.state == State.OPEN:
            # Check if timeout passed
            if time.time() - self.last_failure_time > self.recovery_timeout:
                print("⏳ Recovery Timeout passed. Switching to HALF_OPEN.")
                self.state = State.HALF_OPEN
            else:
                # Fail fast
                print("🚫 Circuit OPEN. Blocking call.")
                raise CircuitBreakerOpenError("Circuit is OPEN")

        # Attempt Execution
        try:
            print(f"📞 Calling function (State: {self.state.name})...")
            result = func(*args, **kwargs)
            
            # Success Handling
            if self.state == State.HALF_OPEN:
                print("✅ HALF_OPEN probe succeeded. Circuit Closing.")
                self.state = State.CLOSED
                self.failure_count = 0
                
            return result
            
        except Exception as e:
            # Failure Handling
            print(f"❌ Call failed: {e}")
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.state == State.HALF_OPEN:
                print("💥 HALF_OPEN probe failed. Circuit Re-Opening.")
                self.state = State.OPEN
            elif self.failure_count >= self.failure_threshold:
                print("⚠️ Threshold reached. Circuit Opening.")
                self.state = State.OPEN
                
            raise e

# --- Example Usage ---

# Mock Unstable Service
success = False
def unstable_service():
    if not success:
        raise ConnectionError("Service Down")
    return "Service Up!"

if __name__ == "__main__":
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1.0)
    
    # 1. Fail until Open
    print("--- Phase 1: Failing ---")
    for i in range(3):
        try:
            cb.call(unstable_service)
        except Exception:
            pass
            
    # 2. Assert Fail Fast
    print("\n--- Phase 2: Fail Fast ---")
    try:
        cb.call(unstable_service)
    except CircuitBreakerOpenError:
        print("✅ Correctly rejected call immediately.")
        
    # 3. Wait and Recover
    print("\n--- Phase 3: Recovery ---")
    time.sleep(1.1)     # Wait for recovery timeout
    success = True      # Fix the service
    
    res = cb.call(unstable_service) # Should be HALF_OPEN -> Success -> CLOSED
    print(f"Final Result: {res}")
    print(f"Final State: {cb.state.name}")
