import unittest
import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extended_autonomous_pipeline import ExtendedAutonomousPipeline
from refactored_orchestrator import EnhancedOrchestrator


class TestExtendedAutonomousPipeline(unittest.IsolatedAsyncioTestCase):
    """Validate the extended SDLC pipeline."""

    async def test_run_pipeline(self):
        orchestrator = EnhancedOrchestrator()
        agents = ['gemini', 'claude']
        pipeline = ExtendedAutonomousPipeline(orchestrator, agents)
        results = await pipeline.run_pipeline('Initial requirements')
        self.assertEqual(len(results), 8)
        expected_names = [
            'requirement_extraction',
            'architecture_synthesis',
            'code_generation',
            'automated_testing',
            'code_review',
            'deployment_orchestration',
            'monitoring',
            'metrics_feedback',
        ]
        self.assertEqual([r.name for r in results], expected_names)


if __name__ == '__main__':
    unittest.main()
