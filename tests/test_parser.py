"""Tests for task parser."""

import pytest
from src.parsers.task_parser import parse_tasks


def test_parse_valid_tasks():
    """Test parsing valid task JSON."""
    llm_output = """
    Here's the plan:
    [
        {"idx": 1, "tool": "search_tool", "args": {"query": "test"}, "dependencies": []},
        {"idx": 2, "tool": "math_tool", "args": {"expression": "2+2"}, "dependencies": [1]}
    ]
    """
    
    tasks = parse_tasks(llm_output)
    
    assert len(tasks) == 2
    assert tasks[0]["idx"] == 1
    assert tasks[0]["tool"] == "search_tool"
    assert tasks[1]["dependencies"] == [1]


def test_parse_tasks_no_json():
    """Test parsing fails when no JSON found."""
    llm_output = "This is just text without JSON"
    
    with pytest.raises(ValueError, match="Could not find JSON array"):
        parse_tasks(llm_output)


def test_parse_tasks_invalid_json():
    """Test parsing fails with invalid JSON."""
    llm_output = "[{invalid json}]"
    
    with pytest.raises(ValueError, match="Failed to parse JSON"):
        parse_tasks(llm_output)


def test_parse_tasks_missing_fields():
    """Test parsing fails when required fields are missing."""
    llm_output = '[{"idx": 1, "tool": "search_tool"}]'
    
    with pytest.raises(ValueError, match="missing required field"):
        parse_tasks(llm_output)
