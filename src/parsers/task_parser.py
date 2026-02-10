"""Parser for task outputs from the planner."""

import json
import re
from typing import List, Dict, Any


def parse_tasks(llm_output: str) -> List[Dict[str, Any]]:
    """Parse task list from LLM output.
    
    Args:
        llm_output: Raw output from the planner LLM
    
    Returns:
        List of task dictionaries
    
    Raises:
        ValueError: If output cannot be parsed
    """
    # Try to extract JSON from the output
    # Look for JSON array pattern
    json_match = re.search(r'\[[\s\S]*\]', llm_output)
    
    if not json_match:
        raise ValueError(f"Could not find JSON array in output: {llm_output}")
    
    json_str = json_match.group(0)
    
    try:
        tasks = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}\nContent: {json_str}")
    
    if not isinstance(tasks, list):
        raise ValueError(f"Expected list of tasks, got {type(tasks)}")
    
    # Validate task structure
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError(f"Task must be a dictionary, got {type(task)}")
        
        required_fields = ["idx", "tool", "args", "dependencies"]
        for field in required_fields:
            if field not in task:
                raise ValueError(f"Task missing required field '{field}': {task}")
    
    return tasks
