from typing import Dict, List, Tuple
from dataclasses import dataclass
import threading

@dataclass
class Entry:
    member: str
    score: float

class Leaderboard:
    def __init__(self):
        self._scores: Dict[str, float] = {}
        self._lock = threading.Lock()

    def update_score(self, member: str, increment: float):
        """Adds to existing score."""
        with self._lock:
            current = self._scores.get(member, 0.0)
            new_val = current + increment
            self._scores[member] = new_val
            print(f"   📈 {member} score update: {current} -> {new_val}")

    def set_score(self, member: str, score: float):
        """Sets absolute score."""
        with self._lock:
            self._scores[member] = score
            print(f"   📊 {member} set to {score}")

    def get_top_k(self, k: int = 3) -> List[Tuple[str, float]]:
        """Returns top K members sorted by score desc."""
        with self._lock:
            # Python's sort is Timsort (O(N log N)), acceptable for N < 10,000
            # For massive scale, use a Skip List or Redis
            sorted_items = sorted(self._scores.items(), key=lambda item: item[1], reverse=True)
            return sorted_items[:k]

    def get_rank(self, member: str) -> int:
        """Returns 1-based rank."""
        with self._lock:
            sorted_items = sorted(self._scores.items(), key=lambda item: item[1], reverse=True)
            for rank, (m, s) in enumerate(sorted_items):
                if m == member:
                    return rank + 1
            return -1

# --- Example Usage ---

if __name__ == "__main__":
    board = Leaderboard()
    
    # 1. Initial State
    board.set_score("Alpha", 100)
    board.set_score("Beta", 80)
    board.set_score("Gamma", 120)
    
    # 2. Updates
    board.update_score("Beta", 50) # Beta -> 130 (New #1)
    board.update_score("Alpha", 10) # Alpha -> 110
    
    # 3. Query
    print("\n--- Top 3 Agents ---")
    top = board.get_top_k(3)
    for i, (name, score) in enumerate(top):
        print(f"#{i+1}: {name} ({score})")
        
    print(f"\nGamma Rank: #{board.get_rank('Gamma')}")
