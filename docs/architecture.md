# LLMCompiler Architecture

## Overview

LLMCompiler is an agent architecture designed to optimize the execution of complex queries by:
1. Breaking down queries into parallel tasks
2. Executing tasks as soon as their dependencies are met
3. Minimizing redundant LLM calls
4. Supporting dynamic replanning

## Core Components

### 1. Planner

**Purpose**: Analyzes user queries and creates a DAG (Directed Acyclic Graph) of tasks.

**Key Features**:
- Uses GPT-4 Turbo for planning
- Outputs structured JSON task definitions
- Identifies parallelizable tasks
- Minimizes sequential dependencies

**Output Format**:
```json
[
  {
    "idx": 1,
    "tool": "search_tool",
    "args": {"query": "GDP of California"},
    "dependencies": []
  },
  {
    "idx": 2,
    "tool": "search_tool",
    "args": {"query": "GDP of Texas"},
    "dependencies": []
  },
  {
    "idx": 3,
    "tool": "math_tool",
    "args": {"expression": "$1 + $2"},
    "dependencies": [1, 2]
  }
]
```

### 2. Task Scheduler

**Purpose**: Executes tasks in parallel while respecting dependencies.

**Key Features**:
- Parallel execution using ThreadPoolExecutor
- Dependency resolution with `$idx` references
- Automatic task wave scheduling
- Error handling and propagation

**Execution Flow**:
1. Identify tasks with no pending dependencies
2. Execute ready tasks in parallel (up to 5 concurrent)
3. Update results and mark tasks complete
4. Repeat until all tasks are done

### 3. Joiner

**Purpose**: Synthesizes task results and determines next action.

**Key Features**:
- Uses GPT-4o for synthesis
- Decides between responding or replanning
- Limits replanning iterations (max 2)
- Provides comprehensive answers

**Decision Logic**:
- If sufficient information → Respond to user
- If information missing → Trigger replan
- If max replans reached → Respond with available info

## Data Flow

```
User Query
    ↓
┌─────────────┐
│   Planner   │ ← Creates DAG of tasks
└─────────────┘
    ↓
┌─────────────┐
│  Scheduler  │ ← Executes tasks in parallel
└─────────────┘
    ↓
┌─────────────┐
│   Joiner    │ ← Synthesizes results
└─────────────┘
    ↓
Response or Replan
```

## State Management

The graph maintains state using `GraphState`:

```python
{
    "messages": [...],        # Conversation history
    "tasks": [...],           # Current task plan
    "task_results": {...},    # Results from executed tasks
    "should_replan": bool,    # Whether to replan
    "replan_count": int       # Number of replanning iterations
}
```

## Advantages

1. **Speed**: Parallel execution reduces total time
2. **Efficiency**: Minimizes redundant LLM calls
3. **Flexibility**: Dynamic replanning handles complex queries
4. **Scalability**: Easy to add new tools

## Limitations

1. Maximum 2 replanning iterations
2. Requires well-structured tool definitions
3. Dependency resolution limited to simple `$idx` references
4. No support for streaming results (yet)
