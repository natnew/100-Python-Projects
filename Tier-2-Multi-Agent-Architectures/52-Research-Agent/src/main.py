import time
import random
from typing import List, Dict

class MockSearchTool:
    def search(self, query: str) -> List[Dict[str, str]]:
        print(f"   🔍 Googling: '{query}'...")
        time.sleep(1.0)
        # Mock results
        if "python" in query.lower():
            return [
                {"url": "python.org", "title": "Welcome to Python", "snippet": "Python is a programming language."},
                {"url": "wiki/python", "title": "Python (programming language)", "snippet": "Created by Guido van Rossum."}
            ]
        return [
            {"url": "example.com", "title": "Generic Result", "snippet": "This is a placeholder result."}
        ]

class MockBrowserTool:
    def read_page(self, url: str) -> str:
        print(f"   🌐 Visiting: {url}...")
        time.sleep(0.5)
        return f"Full content of {url}. It contains very useful information about the topic."

class ResearchAgent:
    def __init__(self):
        self.search_tool = MockSearchTool()
        self.browser_tool = MockBrowserTool()
        self.memory = []

    def research(self, topic: str) -> str:
        print(f"🔎 Researcher started on: '{topic}'")
        
        # 1. Generate Questions (Mocked)
        queries = [f"{topic} history", f"{topic} latest news"]
        
        for q in queries:
            results = self.search_tool.search(q)
            
            # 2. Browse top result
            if results:
                best_page = results[0]
                content = self.browser_tool.read_page(best_page["url"])
                self.memory.append(content)
                
        # 3. Synthesize
        return self._write_report(topic)

    def _write_report(self, topic: str) -> str:
        print("   ✍️ Synthesizing Report...")
        time.sleep(0.5)
        return (
            f"# Research Report: {topic}\n"
            f"Found {len(self.memory)} sources.\n"
            f"Executive Summary: Based on {self.memory[0][:20]}... the topic is trending."
        )

# --- Example Usage ---

if __name__ == "__main__":
    agent = ResearchAgent()
    
    report = agent.research("Python 3.14 features")
    print("\n" + report)
