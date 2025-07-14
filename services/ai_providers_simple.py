import asyncio
from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class Provider:
    name: str

class SimpleOrchestrator:
    """Minimal orchestrator used for unit tests."""
    def __init__(self) -> None:
        self.providers: Dict[str, Provider] = {
            'gemini': Provider('gemini'),
            'claude': Provider('claude'),
            'openai': Provider('openai'),
            'blackbox': Provider('blackbox'),
        }
        self.active_sessions: Dict[str, Any] = {}
        self.bridge_initialized = False

    async def collaborate(self, session_id: str, paradigm: str, task: str,
                          agents: List[str], context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Return a canned response used by the tests."""
        await asyncio.sleep(0)  # allow scheduling
        self.active_sessions[session_id] = task
        return {
            'success': True,
            'paradigm': paradigm,
            'task': task,
            'agents': agents,
            'status': 'ok',
        }

    async def initialize_bridges(self) -> Dict[str, Any]:
        self.bridge_initialized = True
        return {'success': True}

    async def generate_code_with_bridges(self, prompt: str, language: str,
                                         paradigm: str) -> Dict[str, Any]:
        return {'success': True, 'code': f"// code for {prompt}"}

orchestrator = SimpleOrchestrator()
