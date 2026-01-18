import re
from typing import Callable, Dict, Any, List

class AgentLoopError(Exception):
    pass

class ReActAgent:
    def __init__(self, tools: Dict[str, Callable], max_steps: int = 5):
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def run(self, goal: str) -> str:
        self.history = [f"Goal: {goal}"]
        print(f"🏁 ReAct Agent Started. Goal: {goal}")
        
        for step in range(self.max_steps):
            print(f"\n--- Step {step+1} ---")
            
            # 1. Construct Prompt (History + Tools)
            prompt = self._build_prompt()
            
            # 2. Call LLM (In production, replace with real API)
            response = self._mock_llm(prompt)
            print(f"🤖 LLM Output: {response}")
            self.history.append(f"LLM: {response}")
            
            # 3. Parse Thought/Action
            # Simple heuristic parser: Look for "Action: name(args)"
            if "Final Answer:" in response:
                return response.split("Final Answer:")[1].strip()
            
            action_match = re.search(r"Action: (\w+)\((.*?)\)", response)
            if action_match:
                tool_name = action_match.group(1)
                tool_args = action_match.group(2)
                
                # 4. Execute Action
                observation = self._execute_tool(tool_name, tool_args)
                print(f"👀 Observation: {observation}")
                self.history.append(f"Observation: {observation}")
            else:
                # No action found, maybe just thinking?
                pass
                
        return "Failed to reach a conclusion (Max Steps)."

    def _execute_tool(self, name: str, args: str) -> str:
        if name not in self.tools:
            return f"Error: Tool {name} not found."
        try:
            # Simple arg parsing (assuming string args for demo)
            # In production, use JSON parsing
            return self.tools[name](args)
        except Exception as e:
            return f"Error executing {name}: {e}"

    def _build_prompt(self) -> str:
        available_tools = ", ".join([f"{k}(arg)" for k in self.tools.keys()])
        context = "\n".join(self.history)
        return (
            f"Tools available: {available_tools}\n"
            f"Format:\nThought: ...\nAction: tool(arg)\nObservation: ...\nFinal Answer: ...\n\n"
            f"Match the format exactly.\n\n"
            f"{context}\n"
        )

    def _mock_llm(self, prompt: str) -> str:
        """
        Simulates the model's reasoning process for the demo.
        """
        last_line = prompt.strip().split('\n')[-1]
        
        if "Goal: Get weather in London" in prompt and "Observation" not in prompt:
            return "Thought: I need to check the weather tool.\nAction: get_weather(London)"
        if "Observation: Weather in London is Rainy" in prompt:
            return "Thought: It is raining. I should bring an umbrella.\nFinal Answer: Bring an umbrella because it is rainy."
        
        return "Final Answer: Don't know."

# --- Example Usage ---

def get_weather(location: str) -> str:
    return f"Weather in {location} is Rainy"

if __name__ == "__main__":
    tools = {"get_weather": get_weather}
    agent = ReActAgent(tools)
    
    final = agent.run("Get weather in London")
    print(f"\n🏆 Final Result: {final}")
