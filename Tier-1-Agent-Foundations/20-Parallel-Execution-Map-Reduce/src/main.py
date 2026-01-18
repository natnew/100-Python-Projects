import concurrent.futures
import time
import random
from typing import List, Callable

def simulated_llm_call(prompt: str) -> str:
    """Simulates an API call with latency."""
    latency = random.uniform(0.5, 1.5)
    time.sleep(latency)
    return f"Processed: {prompt}"

class MapReduceAgent:
    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers

    def run(self, items: List[str], map_func: Callable[[str], str], reduce_func: Callable[[List[str]], str]) -> str:
        print(f"🚀 Starting Map-Reduce on {len(items)} items with {self.max_workers} workers.")
        
        # 1. Map Phase (Parallel)
        mapped_results = []
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_item = {executor.submit(map_func, item): item for item in items}
            
            for future in concurrent.futures.as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    result = future.result()
                    print(f"  ✅ Map Finished for: '{item[:10]}...'")
                    mapped_results.append(result)
                except Exception as e:
                    print(f"  ❌ Map Failed for '{item}': {e}")
        
        map_duration = time.time() - start_time
        print(f"⏱️ Map Phase took {map_duration:.2f}s")
        
        # 2. Reduce Phase (Sequential)
        print("📉 Starting Reduce Phase...")
        final_result = reduce_func(mapped_results)
        
        return final_result

# --- Example Usage ---

def summarize_doc(doc: str) -> str:
    # "Summarize" mapping
    return simulated_llm_call(f"Summary of {doc}")

def combine_summaries(summaries: List[str]) -> str:
    # "Reduce" reduction
    return "FINAL REPORT:\n" + "\n".join(f"- {s}" for s in summaries)

if __name__ == "__main__":
    docs = [
        "Article 1: AI is growing",
        "Article 2: Python is popular",
        "Article 3: Cats are cute",
        "Article 4: Sky is blue",
        "Article 5: Coffee is good"
    ]
    
    agent = MapReduceAgent(max_workers=5)
    
    final = agent.run(docs, summarize_doc, combine_summaries)
    
    print("\n" + "="*30)
    print(final)
    print("="*30)
