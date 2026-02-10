"""Tests for tools."""

import pytest
from src.tools.math import math_tool
from src.tools.registry import get_all_tools, get_tool_by_name


def test_math_tool_basic():
    """Test basic math operations."""
    result = math_tool.invoke({"expression": "2 + 2"})
    assert "4" in result


def test_math_tool_complex():
    """Test complex math expression."""
    result = math_tool.invoke({"expression": "sqrt(16) * 3"})
    assert "12" in result


def test_math_tool_error():
    """Test math tool with invalid expression."""
    result = math_tool.invoke({"expression": "invalid"})
    assert "Error" in result


def test_get_all_tools():
    """Test getting all tools."""
    tools = get_all_tools()
    
    assert len(tools) >= 2
    tool_names = [t.name for t in tools]
    assert "math_tool" in tool_names
    assert "search_tool" in tool_names


def test_get_tool_by_name():
    """Test getting tool by name."""
    tool = get_tool_by_name("math_tool")
    
    assert tool is not None
    assert tool.name == "math_tool"


def test_get_tool_by_name_not_found():
    """Test getting non-existent tool."""
    tool = get_tool_by_name("nonexistent_tool")
    
    assert tool is None
