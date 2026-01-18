"""
Basic Evaluation Script
Run with: python evals/eval_basic.py
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.main import run_pattern, InputSchema

GOLDEN_DATASET = [
    {"input": "test query 1", "expected": "..." },
    {"input": "test query 2", "expected": "..." },
]

def run_evals():
    print(f"Running evals on {len(GOLDEN_DATASET)} items...")
    passed = 0
    for item in GOLDEN_DATASET:
        try:
            result = run_pattern(InputSchema(query=item["input"]))
            print(f"✅ Input: {item['input'][:20]}... -> Success")
            passed += 1
        except Exception as e:
            print(f"❌ Input: {item['input'][:20]}... -> Failed: {e}")
    
    print(f"\nScore: {passed}/{len(GOLDEN_DATASET)}")

if __name__ == "__main__":
    run_evals()
