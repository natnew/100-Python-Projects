import http.server
import socketserver
import json
import threading
import time
import requests

PORT = 8000

class MockOpenAIHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Routing
        if self.path == "/v1/chat/completions":
            self._handle_chat_completion()
        else:
            self.send_error(404, "Not Found")

    def _handle_chat_completion(self):
        # 2. Read Request
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_json = json.loads(post_data)
        
        # 3. Simulate Logic
        messages = request_json.get("messages", [])
        last_msg = messages[-1]["content"] if messages else ""
        
        print(f"📥 Mock Received: '{last_msg}'")
        
        # Deterministic Responses
        response_content = "This is a mock response."
        if "weather" in last_msg.lower():
            response_content = "The weather is mocking sunny."
        
        # 4. Construct Response (OpenAI Schema)
        payload = {
            "id": "mock-chatcmpl-123",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "gpt-3.5-mock",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_content
                },
                "finish_reason": "stop"
            }],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
        }
        
        # 5. Send
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))

    def log_message(self, format, *args):
        # Silence console logs for cleaner demo output
        return

def start_server():
    with socketserver.TCPServer(("", PORT), MockOpenAIHandler) as httpd:
        print(f"🚀 Mock Server running on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Start server in thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Allow startup
    time.sleep(1)
    
    # --- Client Test ---
    print("\n--- Testing Mock API ---")
    url = f"http://localhost:{PORT}/v1/chat/completions"
    data = {"messages": [{"role": "user", "content": "What is the weather?"}]}
    
    try:
        resp = requests.post(url, json=data)
        print(f"Request: {data}")
        print(f"Response Status: {resp.status_code}")
        print(f"Response Body: {json.dumps(resp.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
        
    print("\n✅ Test Complete. Server running in background (Ctrl+C to stop).")
    # Keep main thread alive briefly to show output/handle shutdown if not daemon
    time.sleep(1)
