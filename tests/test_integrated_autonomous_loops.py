import unittest
import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from integrated_autonomous_loops import IntegratedAutonomousLoops
from refactored_orchestrator import EnhancedOrchestrator

class TestIntegratedAutonomousLoops(unittest.IsolatedAsyncioTestCase):
    """TestIntegratedAutonomousLoops class for steampunk operations."""
    """Test Run All Loops Basic with enhanced functionality."""
    async def test_run_all_loops_basic(self):
        orchestrator = EnhancedOrchestrator()
        agents = ['gemini', 'claude', 'openai']
        task_description = "Test task for integrated autonomous loops"

        loops_runner = IntegratedAutonomousLoops(orchestrator, agents)
        await loops_runner.run_all_loops(task_description, iterations=2, delay_seconds=1)

        # Check that performance history has entries
        self.assertEqual(len(loops_runner.performance_history), 2)

        # Check that each entry contains expected keys
        for entry in loops_runner.performance_history:
            self.assertIn('sd_result', entry)
            self.assertIn('feedback_result', entry)
            self.assertIn('optimization_result', entry)

        # Check that feedback and optimization results are non-empty strings
        for entry in loops_runner.performance_history:
            self.assertIsInstance(entry['feedback_result'], str)
            self.assertIsInstance(entry['optimization_result'], str)
            self.assertTrue(len(entry['feedback_result']) > 0)
            self.assertTrue(len(entry['optimization_result']) > 0)

if __name__ == "__main__":
    unittest.main()
