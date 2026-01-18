import time

class UserProxyAgent:
    def __init__(self, name: str, max_auto_replies: int = 0):
        self.name = name
        self.max_auto_replies = max_auto_replies
        self.auto_reply_count = 0

    def get_input(self, question: str) -> str:
        """
        Intercepts the question. Decides whether to auto-reply or ask human.
        """
        print(f"   🤖 Worker asks: '{question}'")
        
        # 1. Check Auto-Reply Limit
        if self.auto_reply_count < self.max_auto_replies:
            self.auto_reply_count += 1
            print(f"      👤 {self.name} (Auto-Reply {self.auto_reply_count}/{self.max_auto_replies}): 'Proceed'")
            return "Proceed" # Default auto validation
        
        # 2. Simulate Human Turn (In a real app, this waits for input())
        # For this demo, we mock a "Done" signal after the limit
        print(f"      👤 {self.name} (Manual Reached): 'Stop'")
        return "formatted_exit_code"

class AssistantAgent:
    def __init__(self, name: str):
        self.name = name

    def chat(self, user_proxy: UserProxyAgent):
        print(f"🤖 {self.name} connected to {user_proxy.name}.\n")
        
        step = 1
        while True:
            # Agent proposes an action
            action = f"Step {step}: Execute 'rm -rf /'?"
            
            # Agent asks for permission
            response = user_proxy.get_input(action)
            
            if response == "formatted_exit_code" or response.lower() == "stop":
                print(f"   🛑 {self.name} stopping received '{response}'")
                break
            
            print(f"   ✅ {self.name} executing Step {step}...")
            time.sleep(0.5)
            step += 1

# --- Example Usage ---

if __name__ == "__main__":
    # Scenario: Allow 3 auto-approvals, then stop.
    proxy = UserProxyAgent(name="ProxyUser", max_auto_replies=3)
    assistant = AssistantAgent(name="Assistant")
    
    assistant.chat(proxy)
