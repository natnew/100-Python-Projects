import pytest
from src.main import run_pattern, InputSchema, OutputSchema

def test_basic_structure():
    """Verify the pattern returns the expected schema."""
    result = run_pattern(InputSchema(query="test"))
    assert isinstance(result, OutputSchema)
    assert result.confidence >= 0.0
