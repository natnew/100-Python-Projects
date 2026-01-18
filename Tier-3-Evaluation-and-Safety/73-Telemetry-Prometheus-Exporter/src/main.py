import time
import random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Global Registry
METRICS = {}

class Metric:
    def __init__(self, name, help_text, metric_type="gauge"):
        self.name = name
        self.help = help_text
        self.type = metric_type
        self.value = 0
        METRICS[name] = self

    def set(self, val):
        self.value = val

    def inc(self, amt=1):
        self.value += amt

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-type", "text/plain; version=0.0.4")
            self.end_headers()
            
            response = []
            for name, m in METRICS.items():
                response.append(f"# HELP {name} {m.help}")
                response.append(f"# TYPE {name} {m.type}")
                response.append(f"{name} {m.value}")
            
            self.wfile.write("\n".join(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

class TelemetryAgent(threading.Thread):
    def __init__(self, port=8000):
        super().__init__()
        self.port = port
        self.server = HTTPServer(('localhost', port), MetricsHandler)
        self.running = True

    def run(self):
        print(f"📡 Telemetry Exporter running on http://localhost:{self.port}/metrics")
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

# --- Simulation ---

if __name__ == "__main__":
    # 1. Define Metrics
    active_agents = Metric("agent_active_count", "Number of agents running")
    tasks_processed = Metric("agent_tasks_total", "Total tasks processed", "counter")
    cpu_usage = Metric("agent_cpu_usage", "Current CPU load")

    # 2. Start Server
    exporter = TelemetryAgent(port=8080)
    exporter.daemon = True
    exporter.start()

    # 3. Simulate System
    try:
        print("🔄 System running. Check localhost:8080/metrics (or wait for dump)")
        for i in range(10):
            # Update Metrics
            active_agents.set(random.randint(5, 15))
            tasks_processed.inc(random.randint(1, 5))
            cpu_usage.set(random.uniform(20.0, 80.0))
            
            print(f"   [Tick {i+1}] Updated metrics...")
            time.sleep(1.0)
            
        print("\n📥 Final Metrics Scrape:")
        # Simulate a scrape
        import requests
        try:
            r = requests.get("http://localhost:8080/metrics")
            print("-" * 40)
            print(r.text)
            print("-" * 40)
        except ImportError:
            print("(Use 'curl http://localhost:8080/metrics' to view)")
            
    except KeyboardInterrupt:
        pass
    finally:
        exporter.stop()
        print("🛑 Server stopped.")
