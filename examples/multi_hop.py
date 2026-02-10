"""Multi-hop reasoning example for LLMCompiler."""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.graph import create_llm_compiler_graph

# Load environment variables
load_dotenv()


def main():
    """Run a multi-hop reasoning query through LLMCompiler."""
    print("=" * 60)
    print("LLMCompiler - Multi-Hop Reasoning Example")
    print("=" * 60)
    
    # Create the graph
    graph = create_llm_compiler_graph()
    
    # Define the query - requires multiple searches and synthesis
    query = "What is the combined GDP of California and Texas?"
    
    print(f"\nQuery: {query}\n")
    print("Processing...\n")
    
    # Run the query
    result = graph.invoke({
        "messages": [{"role": "user", "content": query}],
        "tasks": [],
        "task_results": {},
        "should_replan": False,
        "replan_count": 0
    })
    
    # Print the response
    print("=" * 60)
    print("Response:")
    print("=" * 60)
    print(result["messages"][-1].content)
    
    # Show task execution details
    print("\n" + "=" * 60)
    print("Execution Details:")
    print("=" * 60)
    print(f"Tasks executed: {len(result.get('tasks', []))}")
    print(f"Replanning iterations: {result.get('replan_count', 0)}")
    print("\n")


if __name__ == "__main__":
    main()
