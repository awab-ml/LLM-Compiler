"""Task data models for LLMCompiler."""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Status of a task in the execution pipeline."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    """Represents a single task in the execution DAG."""
    
    idx: int = Field(description="Task index/ID")
    name: str = Field(description="Name of the tool to execute")
    args: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the tool")
    dependencies: List[int] = Field(default_factory=list, description="List of task IDs this task depends on")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current status of the task")
    result: Optional[Any] = Field(default=None, description="Result of task execution")
    error: Optional[str] = Field(default=None, description="Error message if task failed")
    
    class Config:
        use_enum_values = True
    
    def is_ready(self, completed_tasks: set) -> bool:
        """Check if all dependencies are completed."""
        return all(dep in completed_tasks for dep in self.dependencies)
    
    def mark_running(self):
        """Mark task as running."""
        self.status = TaskStatus.RUNNING
    
    def mark_completed(self, result: Any):
        """Mark task as completed with result."""
        self.status = TaskStatus.COMPLETED
        self.result = result
    
    def mark_failed(self, error: str):
        """Mark task as failed with error."""
        self.status = TaskStatus.FAILED
        self.error = error
