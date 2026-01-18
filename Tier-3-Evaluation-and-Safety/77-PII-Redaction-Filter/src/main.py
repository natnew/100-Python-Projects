import re
import dataclasses
from typing import List, Tuple

class PIIFilter:
    def __init__(self):
        # Define patterns
        self.patterns = {
            "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "PHONE": r'\b(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
            "IP_ADDR": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            "SSN": r'\b\d{3}-\d{2}-\d{4}\b'
        }

    def redact(self, text: str) -> Tuple[str, List[str]]:
        """
        Redacts PII from text.
        Returns: (cleaned_text, list_of_redacted_items)
        """
        redacted_items = []
        cleaned_text = text
        
        for pii_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, cleaned_text)
            # We iterate in reverse to avoid index shifting issues if we were doing replacements by index,
            # but regex sub is easier. However, to capture WHAT was redacted, findall is useful.
            
            found = re.findall(pattern, text)
            for item in found:
                redacted_items.append(f"{pii_type}: {item}")
                
            # Perform substitution
            cleaned_text = re.sub(pattern, f"[{pii_type}_REDACTED]", cleaned_text)
            
        return cleaned_text, redacted_items

class PrivacyAgent:
    def __init__(self):
        self.filter = PIIFilter()

    def process_message(self, user_message: str):
        print(f"\n📩 Incoming: '{user_message}'")
        
        # 1. Redact
        safe_message, reductions = self.filter.redact(user_message)
        
        # 2. Check if clean
        if not reductions:
            print("✅ No PII detected. Forwarding to LLM.")
        else:
            print(f"⚠️  PII DETECTED! Redacting {len(reductions)} items.")
            for r in reductions:
                print(f"   - {r}")
        
        # 3. Output
        print(f"📤 Outgoing: '{safe_message}'")
        return safe_message

if __name__ == "__main__":
    agent = PrivacyAgent()
    
    test_cases = [
        "Hello, how are you?",
        "My email is john.doe@example.com, please contact me.",
        "Call me at 555-0199 immediately.",
        "My server IP is 192.168.1.1 and my SSN is 123-45-6789 (just kidding)."
    ]
    
    print("🛡️ Starting PII Redaction Filter Test...")
    print("-" * 60)
    
    for case in test_cases:
        agent.process_message(case)
        print("-" * 60)
