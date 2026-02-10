"""Math tool for numerical calculations."""

import numexpr as ne
from langchain_core.tools import tool


@tool
def math_tool(expression: str) -> str:
    """Evaluate a mathematical expression safely.
    
    Args:
        expression: A mathematical expression to evaluate (e.g., "2 + 2", "sqrt(16)")
    
    Returns:
        The result of the calculation as a string
    
    Examples:
        >>> math_tool("2 + 2")
        "4.0"
        >>> math_tool("sqrt(16) * 3")
        "12.0"
    """
    try:
        # Use numexpr for safe evaluation
        result = ne.evaluate(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression '{expression}': {str(e)}"
