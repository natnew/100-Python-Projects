import hashlib
import time
import os
from typing import Dict, Optional

class TTSAdapter:
    def __init__(self, cache_dir: str = ".tts_cache"):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def speak(self, text: str) -> str:
        """
        Returns path to audio file.
        Checks cache first.
        """
        # 1. Hashing
        text_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
        filename = os.path.join(self.cache_dir, f"{text_hash}.mp3")
        
        # 2. Check Cache
        if os.path.exists(filename):
            print(f"✅ Cache Hit for: '{text[:20]}...'")
            return filename
            
        # 3. Generate
        print(f"📢 Generating Audio for: '{text[:20]}...'")
        self._simulate_generation(text, filename)
        
        return filename

    def _simulate_generation(self, text: str, output_path: str):
        # Simulate API Latency
        time.sleep(1.0)
        
        # Create a dummy file
        with open(output_path, "w") as f:
            f.write(f"SIMULATED AUDIO CONTENT FOR: {text}")
        print(f"   💾 Saved to {output_path}")

# --- Example Usage ---

if __name__ == "__main__":
    tts = TTSAdapter()
    
    # 1. First Generation (Slow)
    start = time.time()
    file1 = tts.speak("Hello, welcome to the system.")
    print(f"Time 1: {time.time() - start:.2f}s")
    
    # 2. Duplicate Request (Fast - Cache Hit)
    start = time.time()
    file2 = tts.speak("Hello, welcome to the system.")
    print(f"Time 2: {time.time() - start:.2f}s")
    
    # 3. New Request
    tts.speak("Different text.")
