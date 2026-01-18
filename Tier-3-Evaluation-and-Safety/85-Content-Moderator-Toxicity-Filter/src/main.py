import re
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ModerationScore:
    toxicity: float
    severe_toxicity: float
    obscenity: float
    threat: float
    
    @property
    def is_safe(self) -> bool:
        return max(self.toxicity, self.severe_toxicity, self.obscenity, self.threat) < 0.7

class ContentModerator:
    def __init__(self):
        # We use a simple keyword-based heuristic for this demo
        # In prod, this would be a BERT/RoBERTa model
        self.toxic_words = ["stupid", "idiot", "dumb", "hate"]
        self.severe_words = ["kill", "die", "murder"]
        self.obscene_words = ["****"] # Placeholder
        self.threat_words = ["punch", "attack", "hurt"]

    def predict(self, text: str) -> ModerationScore:
        text = text.lower()
        
        # Simple frequency-based scoring
        tox = self._calculate_score(text, self.toxic_words)
        sev = self._calculate_score(text, self.severe_words) * 2.0 # Higher weight
        obs = self._calculate_score(text, self.obscene_words)
        thr = self._calculate_score(text, self.threat_words)
        
        # Clamping
        return ModerationScore(
            toxicity=min(tox, 1.0),
            severe_toxicity=min(sev, 1.0),
            obscenity=min(obs, 1.0),
            threat=min(thr, 1.0)
        )

    def _calculate_score(self, text: str, keywords: List[str]) -> float:
        score = 0.0
        for word in keywords:
            if word in text:
                score += 0.4
        return score

if __name__ == "__main__":
    mod = ContentModerator()
    
    test_messages = [
        "Hello everyone, hope you have a nice day!",
        "You are a stupid idiot.",
        "I will attack you if you come here.",
        "I hate this dumb game, I want to kill the boss."
    ]
    
    print("🛡️ Content Moderation Scan")
    print("-" * 60)
    
    for msg in test_messages:
        score = mod.predict(msg)
        status = "✅ CLEAN" if score.is_safe else "⛔ BLOCKED"
        
        print(f"Msg: '{msg}'")
        print(f"   Scores: Tox={score.toxicity:.1f}, Sev={score.severe_toxicity:.1f}, Thr={score.threat:.1f}")
        print(f"   Result: {status}")
        print("-" * 60)
