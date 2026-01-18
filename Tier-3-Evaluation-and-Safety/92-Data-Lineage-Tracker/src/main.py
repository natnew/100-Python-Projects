import uuid
import datetime
from dataclasses import dataclass, field
from typing import List

@dataclass
class Artifact:
    id: str
    name: str
    type: str # 'file', 'model', 'dataset'
    created_at: str

@dataclass
class Process:
    id: str
    name: str
    inputs: List[str] # List of Artifact IDs
    outputs: List[str] # List of Artifact IDs

class LineageRegistry:
    def __init__(self):
        self.artifacts = {}
        self.processes = []

    def register_artifact(self, name: str, art_type: str) -> Artifact:
        art_id = str(uuid.uuid4())[:8]
        art = Artifact(
            id=art_id,
            name=name,
            type=art_type,
            created_at=str(datetime.datetime.now())
        )
        self.artifacts[art_id] = art
        print(f"📦 Registered Artifact: {name} (ID: {art_id})")
        return art

    def register_process(self, name: str, inputs: List[Artifact], outputs: List[Artifact]):
        proc_id = str(uuid.uuid4())[:8]
        proc = Process(
            id=proc_id,
            name=name,
            inputs=[a.id for a in inputs],
            outputs=[a.id for a in outputs]
        )
        self.processes.append(proc)
        print(f"⚙️  Registered Process:  {name} (in: {len(inputs)}, out: {len(outputs)})")

    def generate_mermaid(self):
        print("\n🕸️ Data Lineage Graph (Mermaid)")
        print("-" * 40)
        print("graph TD")
        
        # Nodes
        for art in self.artifacts.values():
            shape = "([ " if art.type == "model" else "[ "
            closer = " ])" if art.type == "model" else " ]"
            # Format: id[Name]
            print(f'    {art.id}{shape}"{art.name} ({art.type})"{closer}')

        print("")
        
        # Edges via Processes
        for proc in self.processes:
            # Create a subprocess node? Or just direct links?
            # Let's represent process as a hexagon node
            print(f'    {proc.id}{{ "{proc.name}" }}')
            
            for inp in proc.inputs:
                print(f'    {inp} --> {proc.id}')
            for out in proc.outputs:
                print(f'    {proc.id} --> {out}')
                
        print("-" * 40)

if __name__ == "__main__":
    registry = LineageRegistry()
    
    # 1. Ingest Data
    raw_data = registry.register_artifact("Raw_Tweets.csv", "dataset")
    
    # 2. Clean Data
    clean_data = registry.register_artifact("Cleaned_Tweets.json", "dataset")
    registry.register_process("Data Cleaning Script", inputs=[raw_data], outputs=[clean_data])
    
    # 3. Train Model
    model_v1 = registry.register_artifact("Sentiment_Model_v1.pt", "model")
    registry.register_process("Training Job", inputs=[clean_data], outputs=[model_v1])
    
    # 4. Generate Predictions
    preds = registry.register_artifact("Predictions_Q1.csv", "dataset")
    registry.register_process("Inference Job", inputs=[model_v1, clean_data], outputs=[preds])
    
    # 5. Visualize
    registry.generate_mermaid()
