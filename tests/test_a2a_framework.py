
import unittest
import asyncio
from unittest.mock import MagicMock, AsyncMock

# It's better to import the specific classes you need
# to avoid polluting the namespace and for clarity.
from a2a_framework import (
    A2AAgent,
    A2AOrchestrator,
    AgentCapability,
    MessageType,
    A2AMessage
)


class TestA2AFramework(unittest.TestCase):
    """TestA2AFramework class for steampunk operations."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.loop = asyncio.get_event_loop()

        # Agent Capabilities
        self.coding_capabilities = [
            AgentCapability("code_generation", "Generate code", ["requirements"], ["code"], 0.9, ["python"]),
            AgentCapability("code_review", "Review code", ["code"], ["feedback"], 0.8, ["best_practices"])
        ]
        self.testing_capabilities = [
            AgentCapability("test_generation", "Generate test cases", ["code"], ["tests"], 0.85, ["unit_testing"])
        ]

        # Agents
        self.coder_agent = A2AAgent("coder_001", "CodeMaster", self.coding_capabilities)
        self.tester_agent = A2AAgent("tester_001", "TestGuardian", self.testing_capabilities)

        # Orchestrator
        self.orchestrator = A2AOrchestrator()
        self.orchestrator.register_agent(self.coder_agent)
        self.orchestrator.register_agent(self.tester_agent)

    def test_agent_registration(self):
        """Test that agents are registered correctly in the orchestrator."""
        self.assertIn("coder_001", self.orchestrator.agents)
        self.assertIn("tester_001", self.orchestrator.agents)
        self.assertEqual(len(self.orchestrator.agents), 2)

        # Test peer connections
        self.assertIn("tester_001", self.coder_agent.peers)
        self.assertIn("coder_001", self.tester_agent.peers)

    def test_send_and_receive_message(self):
        """Test that an agent can send and receive a message."""

        """Run Test with enhanced functionality."""
        async def run_test():
            # Start agents
            await self.coder_agent.start()
            await self.tester_agent.start()

            # Mock the receive_message method of the tester agent to check if it's called
            self.tester_agent.receive_message = AsyncMock()

            # Coder sends a message to the tester
            await self.coder_agent.send_message(
                receiver_id="tester_001",
                message_type=MessageType.REQUEST,
                content={"task": "generate tests"}
            )

            # Let the event loop run for a bit to process the message
            await asyncio.sleep(0.1)

            # Assert that the tester agent's receive_message was called
            self.tester_agent.receive_message.assert_called_once()

            # Stop agents
            await self.coder_agent.stop()
            await self.tester_agent.stop()

        self.loop.run_until_complete(run_test())


if __name__ == '__main__':
    unittest.main()
