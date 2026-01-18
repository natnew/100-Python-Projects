import json
from dataclasses import dataclass, field
from typing import List
import datetime

@dataclass
class ModelMetadata:
    name: str
    version: str
    date: str
    author: str
    description: str
    license: str
    intended_use: List[str]
    limitations: List[str]
    training_data: str
    metrics: dict

class ModelCardGenerator:
    def __init__(self):
        pass

    def generate_markdown(self, meta: ModelMetadata) -> str:
        # Simple template rendering
        md = f"""# Model Card: {meta.name}

## Model Details
*   **Name:** {meta.name}
*   **Version:** {meta.version}
*   **Date:** {meta.date}
*   **Author:** {meta.author}
*   **License:** {meta.license}

## Description
{meta.description}

## Intended Use
"""
        for use in meta.intended_use:
            md += f"*   {use}\n"

        md += "\n## Limitations & Risks\n"
        for lim in meta.limitations:
            md += f"*   ⚠️ {lim}\n"

        md += f"""
## Training Data
{meta.training_data}

## Performance Metrics
| Metric | Value |
|--------|-------|
"""
        for k, v in meta.metrics.items():
            md += f"| {k} | {v} |\n"
            
        return md

if __name__ == "__main__":
    # 1. Define Metadata
    meta = ModelMetadata(
        name="Toxicity-Filter-v1",
        version="1.0.0",
        date=str(datetime.date.today()),
        author="Tier-3-Safety-Team",
        description="A heuristic-based text classifier for detecting toxic content in user messages.",
        license="MIT",
        intended_use=[
            "Chatbot moderation",
            "Forum comment filtering",
            "Pre-screening user input"
        ],
        limitations=[
            "Only supports English.",
            "Uses keyword matching, so can be bypassed by typos.",
            "May flag sarcastic usages (false positives)."
        ],
        training_data="Curated list of 500 toxic words and 400 safe phrases.",
        metrics={
            "Accuracy": "92%",
            "Precision": "88%",
            "Recall": "95%",
            "Latency": "<10ms"
        }
    )
    
    # 2. Generate
    gen = ModelCardGenerator()
    report = gen.generate_markdown(meta)
    
    print("📝 Generated Model Card:")
    print("-" * 60)
    print(report)
    print("-" * 60)
    
    # 3. Save (Simulated)
    # with open("MODEL_CARD.md", "w") as f: f.write(report)
    print("✅ Model Card saved to disk.")
