"""Tests for Task model."""

import pytest
from src.models.task import Task, TaskStatus


def test_task_creation():
    """Test creating a task."""
    task = Task(
        idx=1,
        name="search_tool",
        args={"query": "test"},
        dependencies=[]
    )
    
    assert task.idx == 1
    assert task.name == "search_tool"
    assert task.status == TaskStatus.PENDING


def test_task_is_ready_no_dependencies():
    """Test task with no dependencies is ready."""
    task = Task(idx=1, name="test", args={}, dependencies=[])
    
    assert task.is_ready(set())


def test_task_is_ready_with_dependencies():
    """Test task readiness with dependencies."""
    task = Task(idx=3, name="test", args={}, dependencies=[1, 2])
    
    assert not task.is_ready({1})
    assert task.is_ready({1, 2})
    assert task.is_ready({1, 2, 3})


def test_task_mark_completed():
    """Test marking task as completed."""
    task = Task(idx=1, name="test", args={}, dependencies=[])
    
    task.mark_completed("result")
    
    assert task.status == TaskStatus.COMPLETED
    assert task.result == "result"


def test_task_mark_failed():
    """Test marking task as failed."""
    task = Task(idx=1, name="test", args={}, dependencies=[])
    
    task.mark_failed("error message")
    
    assert task.status == TaskStatus.FAILED
    assert task.error == "error message"
