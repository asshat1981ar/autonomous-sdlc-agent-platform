import asyncio
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Callable

class MessageType(Enum):
    REQUEST = auto()
    RESPONSE = auto()

@dataclass
class AgentCapability:
    name: str
    description: str
    inputs: List[str]
    outputs: List[str]
    reliability: float
    tools: List[str] = field(default_factory=list)

@dataclass
class A2AMessage:
    sender: str
    receiver: str
    message_type: MessageType
    content: Dict[str, Any]

class A2AAgent:
    def __init__(self, agent_id: str, name: str,
                 capabilities: List[AgentCapability], orchestrator: 'A2AOrchestrator | None' = None) -> None:
        self.agent_id = agent_id
        self.name = name
        self.capabilities = capabilities
        self.orchestrator = orchestrator
        self.peers: List[str] = []

    async def start(self) -> None:
        await asyncio.sleep(0)

    async def stop(self) -> None:
        await asyncio.sleep(0)

    async def send_message(self, receiver_id: str, message_type: MessageType, content: Dict[str, Any]) -> None:
        if not self.orchestrator:
            raise RuntimeError('Agent not registered with orchestrator')
        message = A2AMessage(self.agent_id, receiver_id, message_type, content)
        await self.orchestrator.deliver_message(message)

    async def receive_message(self, message: A2AMessage) -> None:
        # Default implementation just logs; tests patch this method
        await asyncio.sleep(0)

class A2AOrchestrator:
    def __init__(self) -> None:
        self.agents: Dict[str, A2AAgent] = {}

    def register_agent(self, agent: A2AAgent) -> None:
        agent.orchestrator = self
        self.agents[agent.agent_id] = agent
        # connect peers
        for other in self.agents.values():
            if other.agent_id != agent.agent_id:
                if agent.agent_id not in other.peers:
                    other.peers.append(agent.agent_id)
                if other.agent_id not in agent.peers:
                    agent.peers.append(other.agent_id)

    async def deliver_message(self, message: A2AMessage) -> None:
        receiver = self.agents.get(message.receiver)
        if receiver:
            await receiver.receive_message(message)

