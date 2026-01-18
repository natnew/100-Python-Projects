import time
import uuid
import contextlib
from typing import List, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class Span:
    trace_id: str
    span_id: str
    parent_id: Optional[str]
    operation_name: str
    start_time: float
    end_time: Optional[float] = None
    tags: Dict[str, str] = field(default_factory=dict)

class Tracer:
    def __init__(self):
        self.spans: List[Span] = []
        self.active_stack: List[Span] = []

    @contextlib.contextmanager
    def start_span(self, operation_name: str, parent_context: Optional[Dict] = None):
        # Determine Trace/Parent IDs
        trace_id = str(uuid.uuid4().hex[:8])
        parent_span_id = None
        
        # Priority 1: Parent Context passed explicitly (Propagated)
        if parent_context:
            trace_id = parent_context.get("trace_id", trace_id)
            parent_span_id = parent_context.get("span_id")
        # Priority 2: Active local stack
        elif self.active_stack:
            parent = self.active_stack[-1]
            trace_id = parent.trace_id
            parent_span_id = parent.span_id
            
        span = Span(
            trace_id=trace_id,
            span_id=str(uuid.uuid4().hex[:8]),
            parent_id=parent_span_id,
            operation_name=operation_name,
            start_time=time.time()
        )
        
        self.active_stack.append(span)
        print(f"   ➡️ Starting '{operation_name}' [Trace: {trace_id} | Span: {span.span_id}]")
        
        try:
            yield span
        finally:
            span.end_time = time.time()
            self.active_stack.pop()
            self.spans.append(span)
            duration = (span.end_time - span.start_time) * 1000
            print(f"   ⬅️ Finished '{operation_name}' ({duration:.2f}ms)")

    def get_current_context(self) -> Dict:
        if self.active_stack:
            s = self.active_stack[-1]
            return {"trace_id": s.trace_id, "span_id": s.span_id}
        return {}

    def export(self):
        print("\n--- Trace Waterfall ---")
        # Sort by start time
        sorted_spans = sorted(self.spans, key=lambda s: s.start_time)
        if not sorted_spans:
             return
             
        start_t = sorted_spans[0].start_time
        
        for s in sorted_spans:
            offset = (s.start_time - start_t) * 1000
            duration = (s.end_time - s.start_time) * 1000 if s.end_time else 0
            
            indent = "  "
            if s.parent_id:
                # Simple indentation logic (not perfect for async trees but fine for demo)
                indent = "    "
                
            bar = "█" * max(1, int(duration / 10))
            print(f"{indent}[{offset:6.1f}ms] {s.operation_name:20} {bar} ({duration:.1f}ms)")


# --- Simulation Components ---

def service_b(tracer: Tracer, context: Dict):
    with tracer.start_span("Service B: Process", context):
        time.sleep(0.2)
        with tracer.start_span("Service B: DB Query"):
            time.sleep(0.1)

def service_a(tracer: Tracer):
    with tracer.start_span("Service A: Handle Request") as span:
        span.tags["user"] = "Alice"
        time.sleep(0.1)
        
        # Propagate context
        ctx = tracer.get_current_context()
        service_b(tracer, ctx)
        
        time.sleep(0.1)

# --- Example Usage ---

if __name__ == "__main__":
    tracer = Tracer()
    
    service_a(tracer)
    
    tracer.export()
