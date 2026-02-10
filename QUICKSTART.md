# Quick Start Guide

## 1. Initial Setup (One-time)

```bash
# Run the setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## 2. Configure API Keys

Edit `.env` file and add your API keys:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here
TAVILY_API_KEY=tvly-your-key-here

# Optional (for tracing)
LANGSMITH_API_KEY=ls-your-key-here
```

## 3. Run Your First Example

```bash
# Activate virtual environment
source venv/bin/activate

# Run simple example
python examples/simple_question.py
```

## 4. Try More Examples

```bash
# Multi-hop reasoning (parallel execution)
python examples/multi_hop.py

# Math + search combination
python examples/math_problem.py
```

## 5. Run Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_tools.py
```

## 6. Interactive Exploration

```bash
# Start Jupyter notebook
jupyter notebook notebooks/demo.ipynb
```

## 7. Use in Your Code

```python
from src.core.graph import create_llm_compiler_graph

# Create the graph
graph = create_llm_compiler_graph()

# Run a query
result = graph.invoke({
    "messages": [{"role": "user", "content": "Your question here"}],
    "tasks": [],
    "task_results": {},
    "should_replan": False,
    "replan_count": 0
})

# Get the response
print(result["messages"][-1].content)
```

## Common Issues

### Issue: Import errors
**Solution**: Make sure virtual environment is activated
```bash
source venv/bin/activate
```

### Issue: API key errors
**Solution**: Check `.env` file has valid keys
```bash
cat .env | grep API_KEY
```

### Issue: Module not found
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

## Example Queries to Try

1. **Simple search**: "What is the capital of Japan?"
2. **Math**: "What is the square root of 256?"
3. **Multi-hop**: "What is the combined GDP of California and Texas?"
4. **Complex**: "If New York's GDP is $1.9T, what would it be after 15% growth?"

## Project Structure Quick Reference

- `src/core/` - Main components (planner, scheduler, joiner)
- `src/tools/` - Available tools (search, math)
- `src/models/` - Data models (Task, GraphState)
- `examples/` - Example scripts
- `tests/` - Test suite
- `docs/` - Documentation

## Next Steps

1. Read `docs/architecture.md` for architecture overview
2. Check `docs/api.md` for API reference
3. Explore `notebooks/demo.ipynb` for interactive examples
4. Add custom tools in `src/tools/`

## Getting Help

- Check documentation in `docs/`
- Review examples in `examples/`
- Run tests to verify setup: `pytest tests/`
