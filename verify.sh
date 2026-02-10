#!/bin/bash

# LLMCompiler Verification Script

echo "=========================================="
echo "LLMCompiler Build Verification"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check counter
checks_passed=0
checks_failed=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((checks_passed++))
    else
        echo -e "${RED}✗${NC} $1 (missing)"
        ((checks_failed++))
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        ((checks_passed++))
    else
        echo -e "${RED}✗${NC} $1/ (missing)"
        ((checks_failed++))
    fi
}

echo "Checking project structure..."
echo ""

# Core files
echo "Core Files:"
check_file "README.md"
check_file "requirements.txt"
check_file ".env.example"
check_file ".gitignore"
check_file "setup.sh"
echo ""

# Source code
echo "Source Code:"
check_dir "src"
check_dir "src/core"
check_file "src/core/planner.py"
check_file "src/core/scheduler.py"
check_file "src/core/joiner.py"
check_file "src/core/graph.py"
echo ""

check_dir "src/models"
check_file "src/models/task.py"
check_file "src/models/state.py"
echo ""

check_dir "src/tools"
check_file "src/tools/search.py"
check_file "src/tools/math.py"
check_file "src/tools/registry.py"
echo ""

check_dir "src/prompts"
check_file "src/prompts/planner.py"
check_file "src/prompts/joiner.py"
echo ""

check_dir "src/parsers"
check_file "src/parsers/task_parser.py"
echo ""

check_dir "src/utils"
check_file "src/utils/config.py"
echo ""

# Examples
echo "Examples:"
check_dir "examples"
check_file "examples/simple_question.py"
check_file "examples/multi_hop.py"
check_file "examples/math_problem.py"
echo ""

# Tests
echo "Tests:"
check_dir "tests"
check_file "tests/test_parser.py"
check_file "tests/test_task.py"
check_file "tests/test_tools.py"
echo ""

# Documentation
echo "Documentation:"
check_dir "docs"
check_file "docs/architecture.md"
check_file "docs/components.md"
check_file "docs/api.md"
echo ""

# Notebooks
echo "Notebooks:"
check_dir "notebooks"
check_file "notebooks/demo.ipynb"
echo ""

# Summary
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "Checks passed: ${GREEN}$checks_passed${NC}"
echo -e "Checks failed: ${RED}$checks_failed${NC}"
echo ""

if [ $checks_failed -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Project is complete.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run: ./setup.sh (if not already done)"
    echo "2. Edit .env with your API keys"
    echo "3. Run: source venv/bin/activate"
    echo "4. Try: python examples/simple_question.py"
    exit 0
else
    echo -e "${RED}✗ Some files are missing. Please review the build.${NC}"
    exit 1
fi
