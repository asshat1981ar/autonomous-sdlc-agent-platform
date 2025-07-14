import asyncio
from typing import List, Dict, Any

from refactored_orchestrator import EnhancedOrchestrator

class IntegratedAutonomousLoops:
    """Runs a series of autonomous SDLC loops."""
    def __init__(self, orchestrator: EnhancedOrchestrator, agents: List[str]) -> None:
        self.orchestrator = orchestrator
        self.agents = agents
        self.performance_history: List[Dict[str, Any]] = []

    async def run_all_loops(self, task: str, iterations: int = 1, delay_seconds: int = 0) -> None:
        for _ in range(iterations):
            sd_result = await self.orchestrator.collaborate(
                session_id='sd', paradigm='self-directed', task=task, agents=self.agents
            )
            feedback_result = f"feedback for {task}"
            optimization_result = f"optimization for {task}"
            self.performance_history.append({
                'sd_result': sd_result,
                'feedback_result': feedback_result,
                'optimization_result': optimization_result,
            })
            if delay_seconds:
                await asyncio.sleep(delay_seconds)
