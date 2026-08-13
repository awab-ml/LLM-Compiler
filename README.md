

# LLMCompiler

An implementation of LLMCompiler using LangGraph - an agent architecture designed to speed up agentic tasks through eager execution within a DAG while reducing costs by minimizing redundant LLM calls.

## Overview

LLMCompiler has 3 main components:

1. **Planner**: Streams a DAG of tasks to execute
2. **Task Fetching Unit**: Schedules and executes tasks as soon as they are executable
3. **Joiner**: Responds to the user or triggers a second plan (replanning)

## Architecture

```
User Query → Planner → Task Scheduler → Joiner → Response/Replan
                ↓            ↓
              Tasks    Parallel Execution
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/awab-ml/LLM-Compiler.git
cd LLM-Compiler
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Required API Keys

- **OpenAI API Key**: For LLM calls
- **Tavily API Key**: For search functionality
- **LangSmith API Key** (optional): For tracing and debugging

## Quick Start

```python
from src.core.graph import create_llm_compiler_graph

# Create the LLMCompiler graph
graph = create_llm_compiler_graph()

# Run a query
result = graph.invoke({
    "messages": [{"role": "user", "content": "What's the GDP of New York?"}]
})

print(result["messages"][-1].content)
```

## Examples

Run the example scripts to see LLMCompiler in action:

```bash
# Simple question
python examples/simple_question.py

# Multi-hop reasoning
python examples/multi_hop.py

# Multi-step math
python examples/math_problem.py
```

## Project Structure

```
LLMcompiler/
├── src/                    # Main source code
│   ├── core/              # Core components (Planner, Scheduler, Joiner)
│   ├── tools/             # Agent tools (search, math, etc.)
│   ├── parsers/           # Output parsers
│   ├── prompts/           # Prompt templates
│   ├── models/            # Data models
│   └── utils/             # Utilities
├── examples/              # Usage examples
├── notebooks/             # Jupyter notebooks
├── tests/                 # Test suite
└── docs/                  # Documentation
```

## Features

- ✅ Parallel task execution for improved speed
- ✅ Dynamic replanning based on intermediate results
- ✅ Reduced token usage through efficient planning
- ✅ Support for complex multi-hop reasoning
- ✅ Built-in search and math tools
- ✅ Extensible tool system

## Development

Run tests:
```bash
pytest tests/
```

Run with tracing (LangSmith):
```bash
export LANGCHAIN_TRACING_V2=true
python examples/simple_question.py
```

## Documentation

- [Architecture Overview](docs/architecture.md)
- [Component Details](docs/components.md)
- [API Reference](docs/api.md)

## References

- Original Paper: LLMCompiler
- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Uses [LangChain](https://github.com/langchain-ai/langchain)

## License

MIT License
