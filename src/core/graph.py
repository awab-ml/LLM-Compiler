"""Main LLMCompiler graph construction."""

from typing import Literal
from langgraph.graph import StateGraph, END
from ..models.state import GraphState
from .planner import planner_node
from .scheduler import scheduler_node
from .joiner import joiner_node


def should_continue(state: GraphState) -> Literal["planner", "end"]:
    """Determine if we should replan or end.
    
    Args:
        state: Current graph state
    
    Returns:
        Next node to execute
    """
    if state.get("should_replan", False):
        return "planner"
    return "end"


def create_llm_compiler_graph():
    """Create the LLMCompiler graph.
    
    Returns:
        Compiled LangGraph graph
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("scheduler", scheduler_node)
    workflow.add_node("joiner", joiner_node)
    
    # Add edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "scheduler")
    workflow.add_edge("scheduler", "joiner")
    
    # Add conditional edge for replanning
    workflow.add_conditional_edges(
        "joiner",
        should_continue,
        {
            "planner": "planner",
            "end": END
        }
    )
    
    # Compile the graph
    return workflow.compile()
