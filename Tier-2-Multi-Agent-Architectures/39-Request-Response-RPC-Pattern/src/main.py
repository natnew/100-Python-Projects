import uuid
import time
import threading
from typing import Dict, Any, Callable
from dataclasses import dataclass

@dataclass
class RPCMessage:
    id: str
    method: str
    params: Any
    reply_to: str = None
    result: Any = None
    is_response: bool = False

class RPCServer:
    def __init__(self):
        self.methods: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        self.methods[name] = func
    
    def handle_request(self, msg: RPCMessage) -> RPCMessage:
        print(f"   ⚙️ Server executing '{msg.method}'...")
        if msg.method in self.methods:
            try:
                # Simulate work
                time.sleep(0.5)
                res = self.methods[msg.method](msg.params)
                return RPCMessage(id=str(uuid.uuid4()), method=msg.method, 
                                 params=None, reply_to=msg.id, 
                                 result=res, is_response=True)
            except Exception as e:
                return RPCMessage(id=str(uuid.uuid4()), method=msg.method, 
                                 params=None, reply_to=msg.id, 
                                 result=f"Error: {e}", is_response=True)
        return RPCMessage(id=str(uuid.uuid4()), method=msg.method, 
                         params=None, reply_to=msg.id, 
                         result="Method Not Found", is_response=True)

class RPCClient:
    def __init__(self, server: RPCServer):
        self.server = server
        self.pending_requests: Dict[str, Any] = {}

    def call(self, method: str, params: Any) -> Any:
        req_id = str(uuid.uuid4())
        req = RPCMessage(id=req_id, method=method, params=params)
        
        print(f"📞 Client calling '{method}' (ID: {req_id[:8]})...")
        
        # In a real network, this send is async.
        # Here we simulate the network loop synchronously for the demo.
        response = self.server.handle_request(req)
        
        if response.reply_to == req_id:
            return response.result
        return "Mismatch Error"

# --- Example Usage ---

def add(numbers: tuple) -> int:
    return numbers[0] + numbers[1]

def reverse(text: str) -> str:
    return text[::-1]

if __name__ == "__main__":
    # Setup
    server = RPCServer()
    server.register("add", add)
    server.register("reverse", reverse)
    
    client = RPCClient(server)
    
    # Calls
    print("--- Call 1: Add ---")
    res1 = client.call("add", (10, 20))
    print(f"Result: {res1}")
    
    print("\n--- Call 2: Reverse ---")
    res2 = client.call("reverse", "Hello RPC")
    print(f"Result: {res2}")
    
    print("\n--- Call 3: Unknown ---")
    res3 = client.call("multiply", (5, 5))
    print(f"Result: {res3}")
