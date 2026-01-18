import os
import subprocess
import time
from pathlib import Path

def smoke_test_projects(root_dir):
    print(f"🚀 Starting Smoke Test on {root_dir}")
    print("-" * 60)
    
    passed = 0
    failed = 0
    skipped = 0
    
    # Walk through Tiers
    for tier in ["Tier-1-Agent-Foundations", "Tier-2-Multi-Agent-Architectures", "Tier-3-Evaluation-and-Safety"]:
        tier_path = Path(root_dir) / tier
        if not tier_path.exists():
            continue
            
        # Walk through Projects
        for project in sorted(tier_path.iterdir()):
            if not project.is_dir() or project.name.startswith('.'):
                continue
                
            main_py = project / "src" / "main.py"
            readme = project / "README.md"
            
            # 1. Check Structure
            if not main_py.exists():
                print(f"⚠️  MISSING SRC: {project.name}")
                skipped += 1
                continue
                
            # 2. Check Syntax
            try:
                subprocess.check_call(["python", "-m", "py_compile", str(main_py)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print(f"❌ SYNTAX ERROR: {project.name}")
                failed += 1
                continue
            
            # 3. Check Documentation (Basic existence)
            doc_status = "📄" if readme.exists() else "⬜"
            
            # 4. Dry Run (Optional - just checking syntax is safer for now to avoid hanging)
            # We can try running with a very short timeout, but interactive scripts will hang.
            
            print(f"✅ VERIFIED: {project.name:<60} {doc_status}")
            passed += 1

    print("-" * 60)
    print(f"SUMMARY: Passed: {passed} | Failed: {failed} | Skipped: {skipped}")

if __name__ == "__main__":
    smoke_test_projects(".")
