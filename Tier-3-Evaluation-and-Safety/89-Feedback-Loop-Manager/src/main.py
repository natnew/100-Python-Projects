import statistics
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Feedback:
    interaction_id: str
    prompt: str
    response: str
    score: int # 1 to 5
    comment: Optional[str] = None

class FeedbackManager:
    def __init__(self):
        self.db: List[Feedback] = []

    def submit_feedback(self, interaction_id: str, prompt: str, response: str, score: int, comment: str = ""):
        if score < 1 or score > 5:
            raise ValueError("Score must be between 1 and 5")
            
        entry = Feedback(interaction_id, prompt, response, score, comment)
        self.db.append(entry)
        print(f"📥 Feedback received for #{interaction_id}: {score}/5 stars")

    def get_metrics(self):
        if not self.db:
            return "No data."
            
        scores = [f.score for f in self.db]
        avg = statistics.mean(scores)
        count = len(scores)
        
        # NPS-like (Promoters 5, Detractors 1-3)
        promoters = len([s for s in scores if s == 5])
        detractors = len([s for s in scores if s <= 3])
        nps = ((promoters - detractors) / count) * 100
        
        print("\n📊 Dashboard:")
        print(f"   Total Interactions: {count}")
        print(f"   Average CSAT: {avg:.2f} / 5.0")
        print(f"   NPS Score: {nps:.0f}")

    def get_flagged_for_review(self, threshold: int = 2) -> List[Feedback]:
        """Return interactions that need human review (score <= threshold)"""
        return [f for f in self.db if f.score <= threshold]

if __name__ == "__main__":
    manager = FeedbackManager()
    
    # 1. Simulate Interactions
    manager.submit_feedback("ID-001", "Hello", "Hi there!", 5, "Good bot")
    manager.submit_feedback("ID-002", "What is 2+2?", "It is 5.", 1, "Wrong answer")
    manager.submit_feedback("ID-003", "Write code", "Here is python...", 4, "Okay but slow")
    manager.submit_feedback("ID-004", "Sing a song", "I cannot sing.", 3, "Boring")
    manager.submit_feedback("ID-005", "Help me", "Sure!", 5, "")
    
    # 2. Show Metrics
    manager.get_metrics()
    
    # 3. Review Queue
    print("\n🚩 Needs Review (Score <= 2):")
    flagged = manager.get_flagged_for_review()
    for item in flagged:
        print(f"   #{item.interaction_id}: '{item.prompt}' -> '{item.response}' (Score: {item.score})")
