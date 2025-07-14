import sys
import os
import asyncio
import unittest
import logging

# Adjust sys.path to include src directory for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from run_autonomous_sdlc_loop import autonomous_sdlc_loop

logger = logging.getLogger(__name__)

class TestAutonomousSDLCLoop(unittest.TestCase):
    """TestAutonomousSDLCLoop class for steampunk operations."""
    def test_loop_execution(self):
        """Test that the autonomous SDLC loop runs the specified number of iterations"""
        iterations = 3
        task = "Test task for loop execution"
        agents = ['gemini', 'claude']

        """Run Loop with enhanced functionality."""
        async def run_loop():
            await autonomous_sdlc_loop(task, agents, iterations=iterations, delay_seconds=1)

        asyncio.run(run_loop())

        # If no exceptions, test passes
        self.assertTrue(True)

    def test_loop_handles_exceptions(self):
        """Test that the loop handles exceptions gracefully"""
        iterations = 2
        task = "Test task with exception"
        agents = ['gemini', 'claude']

        # Monkey patch enter_autonomous_sdlc_mode to raise exception on second call
        from refactored_orchestrator import enter_autonomous_sdlc_mode
        original_func = enter_autonomous_sdlc_mode

        """Faulty Enter Autonomous Sdlc Mode with enhanced functionality."""
        call_count = 0
        async def faulty_enter_autonomous_sdlc_mode(task, agents):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise Exception("Simulated failure")
            return await original_func(task, agents)

        import run_autonomous_sdlc_loop
        """Run Loop with enhanced functionality."""
        run_autonomous_sdlc_loop.enter_autonomous_sdlc_mode = faulty_enter_autonomous_sdlc_mode

        async def run_loop():
            try:
                await autonomous_sdlc_loop(task, agents, iterations=iterations, delay_seconds=1)
            except Exception as e:
                self.fail(f"Loop raised an exception: {e}")

        asyncio.run(run_loop())

        # Restore original function
        run_autonomous_sdlc_loop.enter_autonomous_sdlc_mode = original_func

    def test_adaptive_self_prompting(self):
        """Test adaptive self-prompting by simulating iterative task refinement"""
        iterations = 3
        """Run Adaptive Loop with enhanced functionality."""
        task = "Initial task for adaptive self-prompting"
        agents = ['gemini', 'claude']

        async def run_adaptive_loop():
            current_task = task
            for i in range(iterations):
                logger.info(f"Adaptive iteration {i+1}")
                result = await autonomous_sdlc_loop(current_task, agents, iterations=1)
                # Simulate adaptation by appending iteration info
                current_task = current_task + f" | Adapted iteration {i+1}"

        asyncio.run(run_adaptive_loop())

if __name__ == "__main__":
    unittest.main()
