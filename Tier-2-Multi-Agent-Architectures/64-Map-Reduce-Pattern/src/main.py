from typing import List, Tuple, Dict, Any
from collections import defaultdict
import threading
import time

# --- Framework ---

class MapReduceJob:
    def map(self, data: Any) -> List[Tuple[str, Any]]:
        raise NotImplementedError

    def reduce(self, key: str, values: List[Any]) -> Any:
        raise NotImplementedError

class MapReduceEngine:
    def run(self, job: MapReduceJob, dataset: List[Any]):
        print(f"🚀 Starting MapReduce on {len(dataset)} items...")
        
        # 1. Map Phase (Simulated Parallelism)
        intermediate = []
        for item in dataset:
            mapped = job.map(item)
            intermediate.extend(mapped)
            print(f"   🗺️ Mapped input to {len(mapped)} pairs.")
            
        print(f"   📊 Intermediate pairs: {len(intermediate)}")
        
        # 2. Shuffle Phase (Group by Key)
        # Sort facilitates grouping
        intermediate.sort(key=lambda x: x[0])
        
        grouped: Dict[str, List[Any]] = defaultdict(list)
        for key, val in intermediate:
            grouped[key].append(val)
            
        print(f"   🔀 Shuffled into {len(grouped)} unique keys.")
        
        # 3. Reduce Phase (Parallelizable)
        output = {}
        for key, values in grouped.items():
            result = job.reduce(key, values)
            output[key] = result
            print(f"   🔻 Reduced '{key}' -> {result}")
            
        return output

# --- User Implementation ---

class WordCountJob(MapReduceJob):
    def map(self, text: str) -> List[Tuple[str, int]]:
        # Simple tokenizer
        words = text.lower().replace('.', '').split()
        return [(w, 1) for w in words]

    def reduce(self, key: str, values: List[int]) -> int:
        return sum(values)

# --- Example Usage ---

if __name__ == "__main__":
    engine = MapReduceEngine()
    job = WordCountJob()
    
    dataset = [
        "Apple banana apple.",
        "Banana cherry date.",
        "Apple date elderberry."
    ]
    
    results = engine.run(job, dataset)
    
    print("\n--- Final Counts ---")
    for k, v in results.items():
        print(f"{k}: {v}")
