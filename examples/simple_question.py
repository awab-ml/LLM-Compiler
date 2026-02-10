"""Simple question example for LLMCompiler."""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.graph import create_llm_compiler_graph

# Load environment variables
load_dotenv()


def main():
    """Run a simple question through LLMCompiler."""
    print("=" * 60)
    print("LLMCompiler - Simple Question Example")
    print("=" * 60)
    
    # Create the graph
    graph = create_llm_compiler_graph()
    
    # Define the query
    query = "What is the GDP of California?"
    
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
    print("\n")


if __name__ == "__main__":
    main()
