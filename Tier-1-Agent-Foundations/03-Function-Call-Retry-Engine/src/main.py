import random
import time
from typing import Callable, Any
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception, RetryCallState

class ToolExecutionError(Exception):
    """Base class for tool errors."""
    pass

class TransientError(ToolExecutionError):
    """Errors that might pass if retried (503, 429)."""
    pass

class TerminalError(ToolExecutionError):
    """Errors that will not pass if retried (400, 401)."""
    pass

def is_retryable(exception: BaseException) -> bool:
    """Predicate to determine if we should retry."""
    return isinstance(exception, TransientError)

def custom_wait(retry_state: RetryCallState) -> float:
    """Exponential backoff with full jitter."""
    exp = 2 ** retry_state.attempt_number
    return random.uniform(0, exp)

class ResilientExecutor:
    def __init__(self, max_attempts: int = 4):
        self.max_attempts = max_attempts

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        # We define the retry decorator dynamically or use a wrapper
        # Here we use the functional API of tenacity or a decorated inner function
        
        @retry(
            retry=retry_if_exception(is_retryable),
            wait=wait_exponential(multiplier=1, min=1, max=10),
            stop=stop_after_attempt(self.max_attempts),
            reraise=True
        )
        def _unsafe_execute():
            try:
                print(f"DEBUG: Attempting {func.__name__}...")
                return func(*args, **kwargs)
            except Exception as e:
                # Classify exception
                # In a real app, check status codes, error messages, etc.
                if "rate limit" in str(e).lower() or "503" in str(e):
                    print(f"DEBUG: Caught Transient Error: {e}")
                    raise TransientError(str(e)) from e
                elif "timeout" in str(e).lower():
                    print(f"DEBUG: Caught Timeout: {e}")
                    raise TransientError(str(e)) from e
                else:
                    # Default coverage for demo purposes, assume other known errors are terminal
                    if isinstance(e, (TransientError, TerminalError)):
                        raise e
                    print(f"DEBUG: Caught Terminal Error: {e}")
                    raise TerminalError(str(e)) from e

        return _unsafe_execute()

# --- Example Usage ---

def flaky_api(key: str):
    """Simulates an API that fails often."""
    r = random.random()
    if r < 0.3:
        raise Exception("429 Too Many Requests (Rate Limit)")
    elif r < 0.6:
        raise Exception("503 Service Unavailable")
    elif r < 0.8:
        raise Exception("401 Unauthorized")  # Terminal!
    return "Success Payload"

if __name__ == "__main__":
    executor = ResilientExecutor(max_attempts=5)
    
    print("--- Test 1: Flaky API Loop ---")
    for i in range(5):
        print(f"\nCall {i+1}:")
        try:
            result = executor.execute(flaky_api, key="secret")
            print(f"✅ Result: {result}")
        except TerminalError as e:
            print(f"❌ Stopped due to Terminal Error: {e}")
        except Exception as e:
            print(f"❌ Failed after max retries: {e}")
