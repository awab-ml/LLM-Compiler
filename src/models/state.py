"""State management for LLMCompiler graph."""

from typing import Annotated, List, Dict, Any
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class GraphState(TypedDict):
    """State for the LLMCompiler graph.
    
    This state is passed between nodes in the LangGraph execution.
    """
    # Messages in the conversation
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Tasks to execute (from planner)
    tasks: List[Dict[str, Any]]
    
    # Results from executed tasks
    task_results: Dict[int, Any]
    
    # Whether to replan
    should_replan: bool
    
    # Number of replanning iterations
    replan_count: int
