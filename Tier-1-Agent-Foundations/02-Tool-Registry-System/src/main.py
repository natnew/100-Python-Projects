import inspect
import json
from typing import Callable, Any, Optional
from pydantic import validate_call

class RegistryError(Exception):
    pass

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Callable] = {}
        self._schemas: dict[str, dict] = {}
        self._metadata: dict[str, dict] = {}

    def register(self, name: Optional[str] = None, deprecated: bool = False):
        """Decorator to register a tool."""
        def decorator(func: Callable):
            tool_name = name or func.__name__
            self._tools[tool_name] = validate_call(func) # Use pydantic to validate inputs at runtime!
            self._schemas[tool_name] = self._generate_schema(func, tool_name)
            self._metadata[tool_name] = {"deprecated": deprecated}
            return func
        return decorator

    def _generate_schema(self, func: Callable, name: str) -> dict:
        """
        Ghetto schema generator. In production use langchain-core or pydantic's internal tools.
        For this pattern, we show the mechanics.
        """
        sig = inspect.signature(func)
        doc = func.__doc__ or "No description."
        
        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for param_name, param in sig.parameters.items():
            if param_name == "self": continue
            # Infer type from annotation (mapping python types to json types)
            py_type = param.annotation
            json_type = "string"
            if py_type is int: json_type = "integer"
            elif py_type is float: json_type = "number"
            elif py_type is bool: json_type = "boolean"
            
            parameters["properties"][param_name] = {
                "type": json_type,
                "description": f"Parameter {param_name}" # In real world, parse docstring for per-param desc
            }
            if param.default == inspect.Parameter.empty:
                parameters["required"].append(param_name)
                
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": doc,
                "parameters": parameters
            }
        }

    def to_openai_tools(self) -> list[dict]:
        """Export tools for OpenAI API."""
        return list(self._schemas.values())

    def execute(self, tool_name: str, arguments: dict) -> Any:
        """Execute a tool request."""
        if tool_name not in self._tools:
            raise RegistryError(f"Tool {tool_name} not found.")
        
        meta = self._metadata[tool_name]
        if meta["deprecated"]:
            print(f"WARNING: Tool {tool_name} is deprecated.")

        try:
            # Invoking the pydantic-validated function
            result = self._tools[tool_name](**arguments)
            return str(result)
        except Exception as e:
            raise RegistryError(f"Execution failed for {tool_name}: {e}")

# --- Example Usage ---

registry = ToolRegistry()

@registry.register(name="get_weather")
def get_weather_tool(location: str, unit: str = "celsius") -> str:
    """Get current weather for a location."""
    return f"Weather in {location} is 25 {unit}"

@registry.register(name="calculator")
def calculator_tool(a: int, b: int, op: str) -> str:
    """Perform basic math."""
    if op == "+": return str(a + b)
    if op == "-": return str(a - b)
    return "Unknown op"

if __name__ == "__main__":
    print("--- Generated Schemas ---")
    print(json.dumps(registry.to_openai_tools(), indent=2))
    
    print("\n--- Execution ---")
    # Simulate an LLM call
    tool_call = {"name": "get_weather", "args": {"location": "London"}}
    
    print(f"Calling {tool_call['name']}:")
    try:
        res = registry.execute(tool_call['name'], tool_call['args'])
        print(f"Result: {res}")
    except Exception as e:
        print(f"Error: {e}")

    # Fail case
    print("\n--- Fail Case (Validation) ---")
    # int required, passing string
    try:
        registry.execute("calculator", {"a": "two", "b": 2, "op": "+"})
    except Exception as e:
        print(f"Caught expected error: {e}")
