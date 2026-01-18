import random
from dataclasses import dataclass

@dataclass
class Example:
    original: str
    adversarial: str
    technique: str

class ContentFilter:
    """A dumb filter that looks for exact keywords."""
    def __init__(self):
        self.blacklist = ["hack", "exploits", "malware", "bomb"]

    def check(self, text: str) -> bool:
        # Simple containment check
        for word in self.blacklist:
            if word in text:
                return False # Blocked
        return True # Allowed

class AdversarialGenerator:
    def __init__(self):
        # Homoglyph Map (Latin -> Cyrillic/Similar)
        self.homoglyphs = {
            'a': 'а', # Cyrillic Small Letter A
            'c': 'с', # Cyrillic Small Letter Es
            'e': 'е', # Cyrillic Small Letter Ie
            'o': 'о', # Cyrillic Small Letter O
            'p': 'р', # Cyrillic Small Letter Er
            'l': '1',
            'i': '1',
            's': '5'
        }

    def generate_homoglyph_attack(self, text: str) -> str:
        chars = list(text)
        for i, char in enumerate(chars):
            if char in self.homoglyphs and random.random() < 0.5:
                chars[i] = self.homoglyphs[char]
        return "".join(chars)

    def generate_typo_attack(self, text: str) -> str:
        if len(text) < 2: return text
        chars = list(text)
        # Swap two random adjacent characters
        pos = random.randint(0, len(chars) - 2)
        chars[pos], chars[pos+1] = chars[pos+1], chars[pos]
        return "".join(chars)

    def generate_whitespace_attack(self, text: str) -> str:
        # Inject zero-width spaces or similar
        return text.replace(" ", "  ")

# --- Simulation ---

if __name__ == "__main__":
    # 1. Setup
    filter_agent = ContentFilter()
    generator = AdversarialGenerator()
    
    blocked_word = "malware"
    
    print(f"🛡️ Target Filter blocks: {filter_agent.blacklist}")
    print("-" * 60)
    
    # 2. Test Normal
    print(f"test 1: Checking '{blocked_word}'")
    if not filter_agent.check(blocked_word):
        print("   ✅ CORRECTLY BLOCKED")
    else:
        print("   ❌ FAILED TO BLOCK")

    # 3. Test Adversarial
    attacks = [
        generator.generate_homoglyph_attack(blocked_word),
        generator.generate_typo_attack(blocked_word),
        generator.generate_homoglyph_attack("how to make a bomb")
    ]
    
    print("-" * 60)
    for attack in attacks:
        print(f"⚔️ Attack: '{attack}'")
        allowed = filter_agent.check(attack)
        
        if allowed:
            print("   ❌ FILTER BYPASSED (Model Fooled)")
        else:
            print("   ✅ BLOCKED")
            
    print("-" * 60)
    print("🚩 Conclusion: Exact matching filters are useless against adversarial inputs.")
