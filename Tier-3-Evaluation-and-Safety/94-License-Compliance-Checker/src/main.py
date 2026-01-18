import dataclasses
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class PkgInfo:
    name: str
    version: str
    license: str

class LicenseRegistry:
    """Simulates PyPI metadata."""
    def __init__(self):
        self.db = {
            "requests": "Apache 2.0",
            "flask": "BSD-3-Clause",
            "numpy": "BSD-3-Clause",
            "paramiko": "LGPL",
            "super-strict-lib": "GPLv3",
            "copyleft-viral-pkg": "AGPLv3"
        }

    def get_license(self, pkg_name: str) -> str:
        return self.db.get(pkg_name.lower(), "Unknown")

class ComplianceAgent:
    def __init__(self):
        self.registry = LicenseRegistry()
        self.allow_list = ["MIT", "Apache 2.0", "BSD-3-Clause", "ISC"]
        self.deny_list = ["GPLv3", "AGPLv3"] # Viral licenses

    def scan_dependencies(self, requirements: List[str]):
        print(f"📦 Scanning {len(requirements)} dependencies...")
        print("-" * 60)
        
        issues = 0
        
        for req in requirements:
            # Parse "package==1.0.0" -> "package"
            pkg_name = req.split("==")[0].split(">=")[0].strip()
            lic = self.registry.get_license(pkg_name)
            
            status = "❓ UNKNOWN"
            if lic in self.allow_list:
                status = "✅ OK"
            elif lic in self.deny_list:
                status = "⛔ BLOCKED"
                issues += 1
            else:
                status = "⚠️  REVIEW" # LGPL etc.
            
            print(f"{pkg_name:<20} | {lic:<15} | {status}")
            
        print("-" * 60)
        if issues > 0:
            print(f"🚨 FAILED: Found {issues} restrictive licenses.")
        else:
            print("✅ SUCCEEDED: All dependencies compliant.")

if __name__ == "__main__":
    agent = ComplianceAgent()
    
    # 1. Simulate a requirements.txt
    project_deps = [
        "requests==2.28.0",
        "flask>=2.0",
        "numpy",
        "super-strict-lib==1.0.0" # The poison pill
    ]
    
    agent.scan_dependencies(project_deps)
