from typing import List, Dict, Set, Any
from collections import deque
import time

class Node:
    def __init__(self, id: str, action: Any):
        self.id = id
        self.action = action
        self.dependencies: Set[str] = set()
        self.result = None

class WorkflowEngine:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.dependents: Dict[str, List[str]] = {} # Reverse graph

    def add_node(self, id: str, action: Any):
        self.nodes[id] = Node(id, action)
        self.dependents[id] = []

    def add_edge(self, parent_id: str, child_id: str):
        if parent_id not in self.nodes or child_id not in self.nodes:
            raise ValueError("Node not found")
        
        self.nodes[child_id].dependencies.add(parent_id)
        self.dependents[parent_id].append(child_id)

    def run(self):
        print("🚀 Starting Workflow...")
        
        # 1. Calc Indegree
        indegree = {u: len(node.dependencies) for u, node in self.nodes.items()}
        queue = deque([u for u, d in indegree.items() if d == 0])
        
        results = {}
        execution_order = []
        
        while queue:
            # Get next specific task
            node_id = queue.popleft()
            execution_order.append(node_id)
            node = self.nodes[node_id]
            
            # Execute
            parent_results = {p: results[p] for p in node.dependencies}
            print(f"   ⚙️ Executing {node_id} (Inputs: {list(node.dependencies)})...")
            
            # Simulate
            time.sleep(0.2)
            results[node_id] = f"Result({node.action})"
            
            # Notify children
            for child in self.dependents[node_id]:
                indegree[child] -= 1
                if indegree[child] == 0:
                    queue.append(child)
                    
        if len(execution_order) != len(self.nodes):
            print("❌ Cycle detected! Graph is not a DAG.")
        else:
            print("✅ Workflow Complete.")
            
        return results

# --- Example Usage ---

if __name__ == "__main__":
    dag = WorkflowEngine()
    
    # Nodes
    dag.add_node("A", "Scrape Google")
    dag.add_node("B", "Scrape Bing")
    dag.add_node("C", "Combine Results")
    dag.add_node("D", "Write Report")
    
    # A -> C, B -> C, C -> D
    dag.add_edge("A", "C")
    dag.add_edge("B", "C")
    dag.add_edge("C", "D")
    
    final_results = dag.run()
    
    print("\n--- Results ---")
    for k, v in final_results.items():
        print(f"{k}: {v}")
