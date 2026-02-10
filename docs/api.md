# API Reference

## Core API

### `create_llm_compiler_graph()`

Creates and compiles the LLMCompiler graph.

**Returns**: Compiled LangGraph instance

**Example**:
```python
from src.core.graph import create_llm_compiler_graph

graph = create_llm_compiler_graph()
```

### Graph Invocation

**Method**: `graph.invoke(state)`

**Parameters**:
- `state` (dict): Initial graph state

**State Structure**:
```python
{
    "messages": [
        {"role": "user", "content": "Your query here"}
    ],
    "tasks": [],
    "task_results": {},
    "should_replan": False,
    "replan_count": 0
}
```

**Returns**: Final state with response

**Example**:
```python
result = graph.invoke({
    "messages": [{"role": "user", "content": "What's 2+2?"}],
    "tasks": [],
    "task_results": {},
    "should_replan": False,
    "replan_count": 0
})

print(result["messages"][-1].content)
```

## Tools API

### `get_all_tools()`

Get all registered tools.

**Returns**: List[BaseTool]

**Example**:
```python
from src.tools import get_all_tools

tools = get_all_tools()
for tool in tools:
    print(f"{tool.name}: {tool.description}")
```

### `get_tool_by_name(name)`

Get a specific tool by name.

**Parameters**:
- `name` (str): Tool name

**Returns**: BaseTool or None

**Example**:
```python
from src.tools import get_tool_by_name

math_tool = get_tool_by_name("math_tool")
result = math_tool.invoke({"expression": "2 + 2"})
```

### `search_tool(query, max_results=5)`

Search the web using Tavily.

**Parameters**:
- `query` (str): Search query
- `max_results` (int): Maximum results (default: 5)

**Returns**: str (formatted results)

**Example**:
```python
from src.tools import search_tool

results = search_tool.invoke({
    "query": "LangChain documentation",
    "max_results": 3
})
```

### `math_tool(expression)`

Evaluate mathematical expressions.

**Parameters**:
- `expression` (str): Math expression

**Returns**: str (result or error)

**Example**:
```python
from src.tools import math_tool

result = math_tool.invoke({"expression": "sqrt(16) * 3"})
# Returns: "12.0"
```

## Models API

### Task

**Class**: `src.models.task.Task`

**Fields**:
- `idx` (int): Task ID
- `name` (str): Tool name
- `args` (dict): Tool arguments
- `dependencies` (list[int]): Dependency task IDs
- `status` (TaskStatus): Current status
- `result` (Any): Execution result
- `error` (str): Error message

**Methods**:
- `is_ready(completed_tasks: set) -> bool`
- `mark_running()`
- `mark_completed(result: Any)`
- `mark_failed(error: str)`

**Example**:
```python
from src.models.task import Task, TaskStatus

task = Task(
    idx=1,
    name="search_tool",
    args={"query": "test"},
    dependencies=[]
)

if task.is_ready(set()):
    task.mark_running()
    # ... execute task
    task.mark_completed("result")
```

### TaskStatus

**Enum**: `src.models.task.TaskStatus`

**Values**:
- `PENDING`: Task not started
- `RUNNING`: Task in progress
- `COMPLETED`: Task finished successfully
- `FAILED`: Task encountered error

## Utilities API

### `get_llm(model=None, temperature=0.0)`

Get a configured LLM instance.

**Parameters**:
- `model` (str): Model name (default: from env)
- `temperature` (float): Generation temperature

**Returns**: ChatOpenAI

**Example**:
```python
from src.utils import get_llm

llm = get_llm(model="gpt-4o", temperature=0.5)
response = llm.invoke("Hello!")
```

### `get_planner_llm()`

Get LLM configured for planning.

**Returns**: ChatOpenAI

### `get_joiner_llm()`

Get LLM configured for joining.

**Returns**: ChatOpenAI

## Parser API

### `parse_tasks(llm_output)`

Parse task list from LLM output.

**Parameters**:
- `llm_output` (str): Raw LLM response

**Returns**: list[dict]

**Raises**: ValueError if parsing fails

**Example**:
```python
from src.parsers import parse_tasks

output = '[{"idx": 1, "tool": "search_tool", "args": {}, "dependencies": []}]'
tasks = parse_tasks(output)
```

## Environment Variables

### Required
- `OPENAI_API_KEY`: OpenAI API key
- `TAVILY_API_KEY`: Tavily API key

### Optional
- `LANGSMITH_API_KEY`: LangSmith tracing
- `LANGCHAIN_TRACING_V2`: Enable tracing (true/false)
- `LANGCHAIN_PROJECT`: Project name
- `DEFAULT_MODEL`: Default LLM model
- `PLANNER_MODEL`: Planner LLM model
- `JOINER_MODEL`: Joiner LLM model
