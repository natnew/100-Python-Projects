import random
from dataclasses import dataclass

class ZeroWidthWatermarker:
    """Uses invisible Unicode characters to encode a signature."""
    
    def __init__(self):
        # Dictionary mapping bits to zero-width chars
        self.ZERO = '\u200b' # Zero-width space
        self.ONE = '\u200c'  # Zero-width non-joiner
        self.SIGNATURE = "AI" # Simple signature

    def _str_to_bin(self, text: str) -> str:
        return ''.join(format(ord(c), '08b') for c in text)

    def _bin_to_str(self, binary: str) -> str:
        chars = []
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            chars.append(chr(int(byte, 2)))
        return ''.join(chars)

    def watermark(self, text: str) -> str:
        binary_sig = self._str_to_bin(self.SIGNATURE)
        
        # Convert binary signature to invisible chars
        invisible_code = ""
        for bit in binary_sig:
            if bit == '0':
                invisible_code += self.ZERO
            else:
                invisible_code += self.ONE
                
        # Inject at a random position (or spread out - simplified here)
        # We append it to the end for simplicity in this demo
        return text + invisible_code

    def verify(self, text: str) -> bool:
        # Extract invisible chars
        extracted_code = ""
        for char in text:
            if char == self.ZERO:
                extracted_code += '0'
            elif char == self.ONE:
                extracted_code += '1'
        
        if not extracted_code:
            return False
            
        try:
            decoded_sig = self._bin_to_str(extracted_code)
            return decoded_sig == self.SIGNATURE
        except Exception:
            return False

if __name__ == "__main__":
    agent = ZeroWidthWatermarker()
    
    # 1. Generate Content
    original = "This is a generated report about finance."
    
    # 2. Watermark
    marked = agent.watermark(original)
    
    print(f"📝 Original Length: {len(original)}")
    print(f"💧 Marked Length:   {len(marked)} (Looks same)")
    print(f"👀 Visible Content: '{marked}'") # It looks identical!
    
    # 3. Verification
    print("-" * 60)
    print("🔎 Verifying Provenance...")
    
    is_valid = agent.verify(marked)
    print(f"   Marked Text: {'✅ Verified' if is_valid else '❌ Fake'}")
    
    is_valid_orig = agent.verify(original)
    print(f"   Original Text: {'✅ Verified' if is_valid_orig else '❌ Unsigned'}")
    
    # 4. Attack (Copy-Paste might keep it, strip() might kill it if at ends)
    attacked = marked.strip()
    is_valid_attacked = agent.verify(attacked)
    print(f"   Stripped Text: {'✅ Verified' if is_valid_attacked else '❌ Lost'}")
