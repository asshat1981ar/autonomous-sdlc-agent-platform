import asyncio
from typing import List

from refactored_orchestrator import enter_autonomous_sdlc_mode

async def autonomous_sdlc_loop(task: str, agents: List[str], *, iterations: int = 1, delay_seconds: int = 0):
    for _ in range(iterations):
        try:
            await enter_autonomous_sdlc_mode(task, agents)
        except Exception:
            # swallow exceptions to allow loop to continue
            pass
        if delay_seconds:
            await asyncio.sleep(delay_seconds)
