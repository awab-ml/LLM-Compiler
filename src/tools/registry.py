"""Tool registry for managing available tools."""

from typing import List, Optional, Dict
from langchain_core.tools import BaseTool
from .search import search_tool
from .math import math_tool


# Registry of all available tools
_TOOL_REGISTRY: Dict[str, BaseTool] = {
    "search_tool": search_tool,
    "math_tool": math_tool,
}


def get_all_tools() -> List[BaseTool]:
    """Get all available tools.
    
    Returns:
        List of all registered tools
    """
    return list(_TOOL_REGISTRY.values())


def get_tool_by_name(name: str) -> Optional[BaseTool]:
    """Get a tool by its name.
    
    Args:
        name: The name of the tool
    
    Returns:
        The tool if found, None otherwise
    """
    return _TOOL_REGISTRY.get(name)


def register_tool(tool: BaseTool) -> None:
    """Register a new tool.
    
    Args:
        tool: The tool to register
    """
    _TOOL_REGISTRY[tool.name] = tool
