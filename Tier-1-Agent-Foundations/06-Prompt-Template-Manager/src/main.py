import re
from typing import Dict, Any, Optional
from dataclasses import dataclass
from string import Template

class PromptError(Exception):
    pass

@dataclass
class PromptVersion:
    template: str
    required_vars: set[str]
    version: str

class PromptManager:
    def __init__(self):
        self._registry: Dict[str, Dict[str, PromptVersion]] = {}

    def register(self, name: str, template: str, version: str = "latest"):
        """
        Register a prompt template.
        Automatically detects variables like ${var_name} or {var_name}.
        """
        # Naive var detection for validation
        # Python string.Template uses ${var}
        # f-strings use {var}
        # We will standardize on Python string.Template for this pattern as it is safer than f-strings (no arbitrary code exec)
        
        # Parse vars (regex for ${identifier} or $identifier)
        vars_found = set(re.findall(r'\$\{([a-z_][a-z0-9_]*)\}', template, re.IGNORECASE))
        vars_found.update(re.findall(r'\$([a-z_][a-z0-9_]*)', template, re.IGNORECASE))
        
        # Support brace style {var} as well by converting to Template format ($var) internally? 
        # Or just enforce one style. Let's enforce $Variable style for this 'Safe' pattern.
        
        pv = PromptVersion(template=template, required_vars=vars_found, version=version)
        
        if name not in self._registry:
            self._registry[name] = {}
        self._registry[name][version] = pv
        
        # Set latest if it's the first one or explicitly requested (logic simplified here)
        if "latest" not in self._registry[name]:
             self._registry[name]["latest"] = pv

    def render(self, name: str, variables: Dict[str, Any], version: str = "latest") -> str:
        """
        Render a prompt with variables.
        """
        if name not in self._registry:
            raise PromptError(f"Prompt '{name}' not found.")
        
        versions = self._registry[name]
        if version not in versions:
            raise PromptError(f"Version '{version}' of prompt '{name}' not found. Available: {list(versions.keys())}")
        
        pv = versions[version]
        
        # Validate vars
        missing = pv.required_vars - set(variables.keys())
        if missing:
             raise PromptError(f"Missing required variables for '{name}:{version}': {missing}")
        
        # Render
        # We use strict Template which raises KeyError if missing (already checked above, but good double check)
        try:
            return Template(pv.template).substitute(variables)
        except Exception as e:
            raise PromptError(f"Rendering failed: {e}")

# --- Example Usage ---

if __name__ == "__main__":
    manager = PromptManager()
    
    # 1. Register a prompt
    manager.register(
        name="summarize_email",
        template="You are a helpful assistant. Please summarize this email from ${sender}:\n\n${body}",
        version="v1"
    )
    
    # 2. Register a v2
    manager.register(
        name="summarize_email",
        template="System: concise_mode\nUser: Summarize email from ${sender}.\nContent: ${body}",
        version="v2"
    )
    
    print("--- Test 1: Render v1 ---")
    p1 = manager.render(
        name="summarize_email", 
        variables={"sender": "Alice", "body": "Hey, meeting is at 5pm."},
        version="v1"
    )
    print(f"v1 Output:\n{p1}")
    
    print("\n--- Test 2: Render v2 ---")
    p2 = manager.render(
        name="summarize_email", 
        variables={"sender": "Bob", "body": "Lunch tomorrow?"},
        version="v2"
    )
    print(f"v2 Output:\n{p2}")
    
    print("\n--- Test 3: Missing Variable Error ---")
    try:
        manager.render("summarize_email", {"sender": "Charlie"}) # Missing body
    except PromptError as e:
        print(f"✅ Caught expected error: {e}")
