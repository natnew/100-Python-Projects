import json
from dataclasses import dataclass
from typing import List, Dict
import datetime

@dataclass
class ReportMetric:
    name: str
    value: float
    unit: str

class BenchmarkReporter:
    def __init__(self, run_name: str):
        self.run_name = run_name
        self.metrics: List[ReportMetric] = []
        self.failures: List[Dict] = []

    def add_metric(self, name: str, value: float, unit: str = ""):
        self.metrics.append(ReportMetric(name, value, unit))

    def add_failure(self, case_id: str, expected: str, actual: str):
        self.failures.append({
            "id": case_id,
            "expected": expected,
            "actual": actual
        })

    def generate_markdown(self) -> str:
        lines = [f"# Benchmark Report: {self.run_name}", f"Date: {datetime.datetime.now()}", ""]
        
        lines.append("## 📊 Metrics")
        lines.append("| Metric | Value |")
        lines.append("| --- | --- |")
        for m in self.metrics:
            lines.append(f"| {m.name} | {m.value}{m.unit} |")
            
        lines.append("")
        lines.append("## ❌ Failures")
        if not self.failures:
            lines.append("🎉 No failures!")
        else:
            lines.append("| ID | Expected | Actual |")
            lines.append("| --- | --- | --- |")
            for f in self.failures:
                lines.append(f"| {f['id']} | {f['expected']} | {f['actual']} |")
                
        return "\n".join(lines)

    def generate_html(self, output_file: str):
        # Simple HTML template without Jinja2 dependency for demo
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: sans-serif; max-width: 800px; margin: 2rem auto; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                .fail {{ color: red; }}
                .pass {{ color: green; }}
            </style>
        </head>
        <body>
            <h1>Benchmark Report: {self.run_name}</h1>
            <p>Generated: {datetime.datetime.now()}</p>
            
            <h2>📊 Metrics</h2>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                {''.join(f"<tr><td>{m.name}</td><td>{m.value}{m.unit}</td></tr>" for m in self.metrics)}
            </table>
            
            <h2>❌ Failures</h2>
            <table>
                <tr><th>ID</th><th>Expected</th><th>Actual</th></tr>
                {''.join(f"<tr><td>{f['id']}</td><td>{f['expected']}</td><td class='fail'>{f['actual']}</td></tr>" for f in self.failures)}
            </table>
        </body>
        </html>
        """
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"📄 Report saved to {output_file}")

# --- Example Usage ---

if __name__ == "__main__":
    reporter = BenchmarkReporter("Agent-v1.0-Run")
    
    # 1. Add Metrics
    reporter.add_metric("Accuracy", 95.5, "%")
    reporter.add_metric("Latency (P99)", 1.2, "s")
    reporter.add_metric("Cost", 0.05, "$")
    
    # 2. Add Failures
    reporter.add_failure("test_24", "Paris", "London")
    
    # 3. Generate Output
    print("--- Markdown Output ---")
    print(reporter.generate_markdown())
    
    reporter.generate_html("report.html")
