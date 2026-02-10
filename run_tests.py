#!/usr/bin/env python3
"""Quick test script for LLMCompiler."""

import sys
sys.path.insert(0, '.')

def test_imports():
    """Test that all modules can be imported."""
    print("="*60)
    print("Test 1: Module Imports")
    print("="*60)
    
    try:
        from src.models.task import Task, TaskStatus
        from src.models.state import GraphState
        from src.parsers.task_parser import parse_tasks
        from src.tools.registry import get_all_tools, get_tool_by_name
        print("✓ All modules imported successfully\n")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}\n")
        return False


def test_task_model():
    """Test Task model functionality."""
    print("="*60)
    print("Test 2: Task Model")
    print("="*60)
    
    try:
        from src.models.task import Task, TaskStatus
        
        # Create a task
        task = Task(
            idx=1,
            name="search_tool",
            args={"query": "test"},
            dependencies=[]
        )
        
        # Test initial state
        assert task.idx == 1, "Task idx incorrect"
        assert task.name == "search_tool", "Task name incorrect"
        assert task.status == TaskStatus.PENDING, "Initial status should be PENDING"
        print("  ✓ Task creation works")
        
        # Test readiness
        assert task.is_ready(set()), "Task with no dependencies should be ready"
        print("  ✓ Dependency checking works")
        
        # Test status changes
        task.mark_running()
        assert task.status == TaskStatus.RUNNING, "Status should be RUNNING"
        print("  ✓ Status changes work")
        
        task.mark_completed("test result")
        assert task.status == TaskStatus.COMPLETED, "Status should be COMPLETED"
        assert task.result == "test result", "Result should be stored"
        print("  ✓ Task completion works")
        
        # Test with dependencies
        task2 = Task(idx=2, name="test", args={}, dependencies=[1, 3])
        assert not task2.is_ready({1}), "Should not be ready with incomplete dependencies"
        assert task2.is_ready({1, 3}), "Should be ready with all dependencies"
        print("  ✓ Complex dependency checking works\n")
        
        return True
    except Exception as e:
        print(f"✗ Task model test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_task_parser():
    """Test task parser functionality."""
    print("="*60)
    print("Test 3: Task Parser")
    print("="*60)
    
    try:
        from src.parsers.task_parser import parse_tasks
        
        # Test valid JSON
        valid_output = '''Here is the plan:
        [
            {"idx": 1, "tool": "search_tool", "args": {"query": "test"}, "dependencies": []},
            {"idx": 2, "tool": "math_tool", "args": {"expression": "2+2"}, "dependencies": [1]}
        ]
        '''
        
        tasks = parse_tasks(valid_output)
        assert len(tasks) == 2, "Should parse 2 tasks"
        assert tasks[0]["idx"] == 1, "First task idx should be 1"
        assert tasks[1]["dependencies"] == [1], "Second task should depend on first"
        print("  ✓ Valid JSON parsing works")
        
        # Test invalid JSON
        try:
            parse_tasks("No JSON here")
            print("  ✗ Should have raised error for invalid JSON")
            return False
        except ValueError:
            print("  ✓ Invalid JSON rejection works\n")
        
        return True
    except Exception as e:
        print(f"✗ Parser test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_tools():
    """Test tools system."""
    print("="*60)
    print("Test 4: Tools System")
    print("="*60)
    
    try:
        from src.tools.registry import get_all_tools, get_tool_by_name
        from src.tools.math import math_tool
        
        # Test tool registry
        tools = get_all_tools()
        assert len(tools) >= 2, "Should have at least 2 tools"
        print(f"  ✓ Found {len(tools)} tools in registry")
        
        # Test getting tool by name
        math = get_tool_by_name("math_tool")
        assert math is not None, "Should find math_tool"
        print("  ✓ Tool lookup works")
        
        # Test math tool
        result = math_tool.invoke({"expression": "2 + 2"})
        assert "4" in result, f"Math result should contain 4, got: {result}"
        print("  ✓ Math tool works")
        
        result = math_tool.invoke({"expression": "sqrt(16) * 3"})
        assert "12" in result, f"Complex math should work, got: {result}"
        print("  ✓ Complex math expressions work\n")
        
        return True
    except Exception as e:
        print(f"✗ Tools test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("LLMCompiler Test Suite")
    print("="*60 + "\n")
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Task Model", test_task_model()))
    results.append(("Task Parser", test_task_parser()))
    results.append(("Tools System", test_tools()))
    
    # Summary
    print("="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    if passed == total:
        print("🎉 All tests passed! LLMCompiler is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
