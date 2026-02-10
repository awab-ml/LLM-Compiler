"""Scheduler node - executes tasks in parallel when possible."""

import re
from typing import Dict, Any, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..models.state import GraphState
from ..models.task import Task, TaskStatus
from ..tools.registry import get_tool_by_name


def resolve_dependencies(args: Dict[str, Any], task_results: Dict[int, Any]) -> Dict[str, Any]:
    """Resolve task dependencies in arguments.
    
    Args:
        args: Task arguments that may contain $idx references
        task_results: Results from completed tasks
    
    Returns:
        Arguments with dependencies resolved
    """
    resolved_args = {}
    
    for key, value in args.items():
        if isinstance(value, str):
            # Replace $idx with actual results
            pattern = r'\$(\d+)'
            matches = re.findall(pattern, value)
            
            resolved_value = value
            for match in matches:
                task_idx = int(match)
                if task_idx in task_results:
                    result = str(task_results[task_idx])
                    resolved_value = resolved_value.replace(f"${match}", result)
            
            resolved_args[key] = resolved_value
        else:
            resolved_args[key] = value
    
    return resolved_args


def execute_task(task: Task, task_results: Dict[int, Any]) -> Task:
    """Execute a single task.
    
    Args:
        task: Task to execute
        task_results: Results from completed tasks
    
    Returns:
        Updated task with result or error
    """
    task.mark_running()
    
    # Get the tool
    tool = get_tool_by_name(task.args.get("tool") or task.name)
    
    if not tool:
        task.mark_failed(f"Tool '{task.name}' not found")
        return task
    
    # Resolve dependencies in arguments
    try:
        resolved_args = resolve_dependencies(task.args, task_results)
        
        # Execute the tool
        result = tool.invoke(resolved_args)
        task.mark_completed(result)
    except Exception as e:
        task.mark_failed(str(e))
    
    return task


def scheduler_node(state: GraphState) -> Dict[str, Any]:
    """Schedule and execute tasks in parallel when possible.
    
    Args:
        state: Current graph state
    
    Returns:
        Updated state with task results
    """
    tasks_data = state.get("tasks", [])
    
    if not tasks_data:
        return {
            "task_results": {},
            "should_replan": False
        }
    
    # Convert to Task objects
    tasks = [
        Task(
            idx=t["idx"],
            name=t["tool"],
            args=t["args"],
            dependencies=t["dependencies"]
        )
        for t in tasks_data
    ]
    
    # Track completed tasks and results
    completed_tasks: Set[int] = set()
    task_results: Dict[int, Any] = {}
    pending_tasks = {task.idx: task for task in tasks}
    
    # Execute tasks in waves based on dependencies
    max_workers = 5  # Parallel execution limit
    
    while pending_tasks:
        # Find tasks ready to execute
        ready_tasks = [
            task for task in pending_tasks.values()
            if task.is_ready(completed_tasks)
        ]
        
        if not ready_tasks:
            # No tasks ready - check for circular dependencies
            remaining = list(pending_tasks.values())
            error_msg = f"Circular dependency detected in tasks: {[t.idx for t in remaining]}"
            return {
                "task_results": task_results,
                "should_replan": True,
                "messages": state["messages"] + [{"role": "assistant", "content": error_msg}]
            }
        
        # Execute ready tasks in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {
                executor.submit(execute_task, task, task_results): task
                for task in ready_tasks
            }
            
            for future in as_completed(future_to_task):
                task = future.result()
                
                # Update results
                if task.status == TaskStatus.COMPLETED:
                    task_results[task.idx] = task.result
                    completed_tasks.add(task.idx)
                else:
                    # Task failed
                    task_results[task.idx] = f"ERROR: {task.error}"
                    completed_tasks.add(task.idx)  # Mark as completed to unblock dependents
                
                # Remove from pending
                pending_tasks.pop(task.idx, None)
    
    return {
        "task_results": task_results,
        "should_replan": False
    }
