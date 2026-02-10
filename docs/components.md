# Component Details

## Planner Component

### Location
`src/core/planner.py`

### Responsibilities
- Extract user query from message history
- Format available tools for LLM context
- Generate task DAG using planner LLM
- Parse and validate task structure

### Configuration
- Model: `PLANNER_MODEL` (default: gpt-4-turbo-preview)
- Temperature: 0.0 (deterministic)

### Error Handling
- Returns error message if parsing fails
- Continues execution with empty task list

## Scheduler Component

### Location
`src/core/scheduler.py`

### Responsibilities
- Convert task data to Task objects
- Resolve task dependencies
- Execute tasks in parallel waves
- Handle task failures gracefully

### Key Functions

#### `resolve_dependencies(args, task_results)`
Replaces `$idx` references with actual results:
```python
# Input: {"expression": "$1 + $2"}
# Output: {"expression": "100 + 200"}
```

#### `execute_task(task, task_results)`
Executes a single task:
1. Get tool from registry
2. Resolve argument dependencies
3. Invoke tool
4. Update task status

### Parallelization
- Uses `ThreadPoolExecutor` with max 5 workers
- Executes tasks in waves based on dependencies
- Detects circular dependencies

## Joiner Component

### Location
`src/core/joiner.py`

### Responsibilities
- Extract original user query
- Format tasks and results for LLM
- Determine if replanning is needed
- Generate final response

### Configuration
- Model: `JOINER_MODEL` (default: gpt-4o)
- Temperature: 0.0

### Replanning Logic
```python
if response.startswith("REPLAN:"):
    if replan_count < 2:
        trigger_replan()
    else:
        respond_with_available_info()
```

## Graph Component

### Location
`src/core/graph.py`

### Structure
```
Entry → Planner → Scheduler → Joiner → [Conditional]
                                          ↓
                                    Replan or End
```

### Conditional Edge
The `should_continue` function determines:
- `"planner"` if `should_replan == True`
- `"end"` otherwise

## Tool System

### Tool Registry
`src/tools/registry.py`

Manages available tools:
- `get_all_tools()`: Returns all registered tools
- `get_tool_by_name(name)`: Gets specific tool
- `register_tool(tool)`: Adds new tool

### Built-in Tools

#### Search Tool
- **Name**: `search_tool`
- **Purpose**: Web search via Tavily API
- **Args**: `query` (str), `max_results` (int)
- **Returns**: Formatted search results

#### Math Tool
- **Name**: `math_tool`
- **Purpose**: Safe mathematical evaluation
- **Args**: `expression` (str)
- **Returns**: Calculation result

### Adding Custom Tools

```python
from langchain_core.tools import tool

@tool
def my_custom_tool(arg1: str, arg2: int) -> str:
    """Tool description."""
    # Implementation
    return result

# Register the tool
from src.tools.registry import register_tool
register_tool(my_custom_tool)
```

## Models

### Task Model
`src/models/task.py`

Represents a single task with:
- `idx`: Unique identifier
- `name`: Tool name
- `args`: Tool arguments
- `dependencies`: List of task IDs
- `status`: Current status (pending/running/completed/failed)
- `result`: Execution result
- `error`: Error message if failed

### GraphState
`src/models/state.py`

TypedDict for LangGraph state management:
- Type-safe state definition
- Message history with `add_messages` reducer
- Task tracking and results
- Replanning control

## Parsers

### Task Parser
`src/parsers/task_parser.py`

Extracts and validates task JSON from LLM output:
1. Regex search for JSON array
2. JSON parsing
3. Structure validation
4. Field validation

## Utilities

### Config
`src/utils/config.py`

LLM configuration:
- Loads environment variables
- Provides configured LLM instances
- Supports model customization
