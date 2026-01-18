import asyncio
import json
import random
from typing import Dict, Any, Callable

# Mocking a WebSocket object for the demo
class MockWebSocket:
    def __init__(self):
        self.open = True

    async def send(self, data: str):
        print(f"   📤 [WS SEND]: {data}")

    async def recv(self):
        # Simulate delay between messages
        await asyncio.sleep(1.0)
        
        # Simulate Incoming Events
        events = [
            {"type": "price_update", "symbol": "AAPL", "price": 150.0 + random.uniform(-1, 1)},
            {"type": "user_message", "content": "Hello Agent!"},
            {"type": "heartbeat", "timestamp": 12345}
        ]
        return json.dumps(random.choice(events))

class StreamAgent:
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}

    def on(self, event_type: str, handler: Callable):
        self.handlers[event_type] = handler

    async def handle_connection(self, ws: MockWebSocket):
        print("🔌 Client Connected.")
        
        try:
            # Listening Loop
            for i in range(5): # Limit to 5 msgs for demo
                raw_msg = await ws.recv()
                print(f"📥 [WS RECV]: {raw_msg}")
                
                data = json.loads(raw_msg)
                event_type = data.get("type")
                
                if event_type in self.handlers:
                    # Execute handler (could be async in real app)
                    response = self.handlers[event_type](data)
                    if response:
                        await ws.send(json.dumps(response))
                else:
                    print(f"   ⚠️ No handler for {event_type}")
                    
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("🔌 Connection Closed.")

# --- Example Handlers ---

def handle_price(data: Dict):
    price = data["price"]
    if price > 150.5:
        return {"action": "SELL", "symbol": data["symbol"]}
    return None

def handle_chat(data: Dict):
    return {"reply": f"Echo: {data['content']}"}

# --- Runtime ---

async def main():
    agent = StreamAgent()
    
    # Register handlers
    agent.on("price_update", handle_price)
    agent.on("user_message", handle_chat)
    
    # Run loop
    mock_ws = MockWebSocket()
    await agent.handle_connection(mock_ws)

if __name__ == "__main__":
    asyncio.run(main())
