"""Planner node - breaks down queries into executable tasks."""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from ..models.state import GraphState
from ..prompts.planner import PLANNER_PROMPT
from ..parsers.task_parser import parse_tasks
from ..utils.config import get_planner_llm
from ..tools.registry import get_all_tools


def planner_node(state: GraphState) -> Dict[str, Any]:
    """Plan tasks based on the user query.
    
    Args:
        state: Current graph state
    
    Returns:
        Updated state with planned tasks
    """
    # Get the latest user message
    messages = state["messages"]
    user_query = None
    
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            user_query = msg.content
            break
    
    if not user_query:
        raise ValueError("No user query found in messages")
    
    # Get available tools
    tools = get_all_tools()
    tool_descriptions = "\n".join([
        f"- {tool.name}: {tool.description}"
        for tool in tools
    ])
    
    # Create planner prompt
    llm = get_planner_llm()
    prompt = PLANNER_PROMPT.format_messages(
        tools=tool_descriptions,
        input=user_query
    )
    
    # Get plan from LLM
    response = llm.invoke(prompt)
    
    # Parse tasks from response
    try:
        tasks = parse_tasks(response.content)
    except ValueError as e:
        # If parsing fails, return error
        return {
            "messages": messages + [AIMessage(content=f"Error planning tasks: {str(e)}")],
            "tasks": [],
            "task_results": {},
            "should_replan": False,
            "replan_count": state.get("replan_count", 0)
        }
    
    # Add planning message to history
    plan_summary = f"Created plan with {len(tasks)} tasks"
    
    return {
        "messages": messages + [AIMessage(content=plan_summary)],
        "tasks": tasks,
        "task_results": {},
        "should_replan": False,
        "replan_count": state.get("replan_count", 0)
    }
