import time
import queue
from dataclasses import dataclass, field
from typing import List

@dataclass(order=True)
class Notification:
    priority: int
    content: str = field(compare=False)
    channel: str = field(compare=False, default="EMAIL") # EMAIL, SLACK, SMS
    timestamp: float = field(compare=False, default_factory=time.time)

class NotificationManager:
    def __init__(self):
        self.q = queue.PriorityQueue()
        self.sent_history = {} # Channel -> Last Sent Time

    def enqueue(self, content: str, priority: int = 10, channel: str = "EMAIL"):
        """
        Priority: 1 (Critical) to 10 (Low)
        """
        n = Notification(priority, content, channel)
        self.q.put(n)
        print(f"📥 Enqueued: '{content}' (Pri: {priority}) via {channel}")

    def process_queue(self):
        print("\n⚙️  Processing Notification Queue...")
        
        while not self.q.empty():
            n = self.q.get()
            self._dispatch(n)
            self.q.task_done()
    
    def _dispatch(self, n: Notification):
        # Debounce Logic: Don't send duplicate logic here, but check rate limits
        last_sent = self.sent_history.get(n.channel, 0)
        now = time.time()
        
        # Simple Rate Limit: Max 1 msg per channel per 0.1s (Simulation)
        if now - last_sent < 0.1:
            print(f"⏳ Throttled: '{n.content}' (Too fast for {n.channel})")
            return

        print(f"🚀 SENDING [{n.channel}]: {n.content}")
        self.sent_history[n.channel] = now
        time.sleep(0.2) # Simulate network lag

if __name__ == "__main__":
    manager = NotificationManager()
    
    # 1. Agents sending alerts
    # Note: PriorityQueue pops lowest number first (1 is high priority)
    
    print("-" * 60)
    manager.enqueue("Server CPU at 10%", priority=10, channel="SLACK") # Low
    manager.enqueue("Server CPU at 99%! CRITICAL!", priority=1, channel="SMS") # High
    manager.enqueue("Daily Digest", priority=5, channel="EMAIL")
    manager.enqueue("Another low prio msg", priority=10, channel="SLACK")
    
    # 2. Process
    manager.process_queue()
    
    print("-" * 60)
