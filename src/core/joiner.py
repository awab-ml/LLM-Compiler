"""Joiner node - synthesizes results and determines if replanning is needed."""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from ..models.state import GraphState
from ..prompts.joiner import JOINER_PROMPT
from ..utils.config import get_joiner_llm


def joiner_node(state: GraphState) -> Dict[str, Any]:
    """Synthesize task results and respond to user or trigger replan.
    
    Args:
        state: Current graph state
    
    Returns:
        Updated state with response and replan decision
    """
    messages = state["messages"]
    tasks = state.get("tasks", [])
    task_results = state.get("task_results", {})
    replan_count = state.get("replan_count", 0)
    
    # Get original user query
    user_query = None
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            user_query = msg.content
            break
    
    if not user_query:
        user_query = "Unknown query"
    
    # Format tasks and results for prompt
    tasks_str = "\n".join([
        f"Task {t['idx']}: {t['tool']}({t['args']}) [depends on: {t['dependencies']}]"
        for t in tasks
    ])
    
    results_str = "\n".join([
        f"Task {idx}: {result}"
        for idx, result in task_results.items()
    ])
    
    # Get joiner LLM
    llm = get_joiner_llm()
    
    # Create prompt
    prompt = JOINER_PROMPT.format_messages(
        query=user_query,
        tasks=tasks_str,
        results=results_str
    )
    
    # Get response
    response = llm.invoke(prompt)
    response_content = response.content
    
    # Check if replanning is needed
    should_replan = response_content.startswith("REPLAN:")
    
    # Limit replanning iterations
    max_replans = 2
    if should_replan and replan_count >= max_replans:
        should_replan = False
        response_content = (
            f"I've attempted to answer your question but reached the replanning limit. "
            f"Based on the available information:\n\n{response_content}"
        )
    
    # Update state
    new_replan_count = replan_count + 1 if should_replan else replan_count
    
    return {
        "messages": messages + [AIMessage(content=response_content)],
        "should_replan": should_replan,
        "replan_count": new_replan_count,
        "tasks": [] if should_replan else tasks,  # Clear tasks if replanning
        "task_results": {} if should_replan else task_results
    }
