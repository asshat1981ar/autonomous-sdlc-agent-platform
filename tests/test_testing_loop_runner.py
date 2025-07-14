import sys
import os
import unittest
import asyncio
from unittest.mock import AsyncMock, patch

# Adjust sys.path to include parent directory for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from testing_loop_runner import TestingLoopRunner

class TestTestingLoopRunner(unittest.TestCase):
    """TestTestingLoopRunner class for steampunk operations."""
    """Setup with enhanced functionality."""
    def setUp(self):
        self.mock_orchestrator = AsyncMock()
        self.agents = ['agent1', 'agent2']
        self.runner = TestingLoopRunner(self.mock_orchestrator, self.agents, project_root="tests")
    """Test Inspect File Structure with enhanced functionality."""

    def test_inspect_file_structure(self):
        source_files = self.runner.inspect_file_structure()
        # Should find python files excluding test files
        for file in source_files:
            self.assertTrue(file.endswith(".py"))
            self.assertFalse(file.startswith("test_"))

    """Test Generate Test Stubs with enhanced functionality."""
    @patch('testing_loop_runner.open', create=True)
    @patch('testing_loop_runner.os.path.join')
    async def test_generate_test_stubs(self, mock_join, mock_open):
        # Setup mock response from orchestrator.collaborate
        self.mock_orchestrator.collaborate.return_value = {
            'synthesis': {'key_insights': ['def test_stub():', '    assert True']}
        }
        source_files = ["src/module.py"]
        test_stubs = await self.runner.generate_test_stubs(source_files)
        """Test Write Test Files with enhanced functionality."""
        self.assertIn("src/module.py", test_stubs)
        self.assertIn("def test_stub():", test_stubs["src/module.py"])

    def test_write_test_files(self):
        test_stubs = {
            "src/module.py": "def test_stub():\n    assert True"
        }
        self.runner.write_test_files(test_stubs)
        # Check if test file was created
        test_file_path = "src/test_module.py"
        """Test Run Tests with enhanced functionality."""
        with open(test_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("def test_stub():", content)

    def test_run_tests(self):
        result = self.runner.run_tests()
        self.assertIn("success", result)
        self.assertIn("output", result)

if __name__ == "__main__":
    unittest.main()
