import base64
import os
from typing import Dict, Any

class VisionClient:
    def __init__(self, simulation_mode: bool = True):
        self.simulation_mode = simulation_mode

    def encode_image(self, image_path: str) -> str:
        """Encodes local image to Base64."""
        if not os.path.exists(image_path):
            if self.simulation_mode:
                 return "[MOCKED_BASE64_STRING]"
            raise FileNotFoundError(f"Image not found: {image_path}")

        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze(self, image_path: str, prompt: str) -> str:
        """
        Sends image + prompt to model.
        """
        encoded_img = self.encode_image(image_path)
        print(f"🖼️ Encoded Image. Size: {len(encoded_img)} chars.")
        
        return self._call_model(encoded_img, prompt)

    def _call_model(self, b64_img: str, prompt: str) -> str:
        """
        Mocking the API call (e.g., OpenAI ChatCompletion with vision).
        """
        print(f"📡 Sending request to Vision Model with prompt: '{prompt}'")
        
        if self.simulation_mode:
            # Return plausible mock responses based on filename/prompt
            if "screenshot" in prompt.lower():
                return "The image shows a website dashboard with a 404 error."
            if "cat" in prompt.lower():
                return "The image contains a fluffy tabby cat sitting on a keyboard."
            return "The image shows a standard test pattern."
        
        return "Real API not configured."

# --- Example Usage ---

if __name__ == "__main__":
    client = VisionClient(simulation_mode=True)
    
    # 1. Analyze a "test" image
    # In real usage: client.analyze("bug.png", "What is wrong with this UI?")
    
    print("--- Test 1 ---")
    description = client.analyze("mock_cat.jpg", "Is there a cat in this image?")
    print(f"🤖 Output: {description}")
    
    print("\n--- Test 2 ---")
    description = client.analyze("mock_screen.png", "Analyze this screenshot.")
    print(f"🤖 Output: {description}")
