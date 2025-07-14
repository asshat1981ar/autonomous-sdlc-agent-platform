#!/usr/bin/env python3
"""
Test script to demonstrate SDLC Orchestrator functionality
"""
import asyncio
import json
import sys
import os
import logging

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.ai_providers_simple import orchestrator

logger = logging.getLogger(__name__)

async def _async_test_orchestrator():
    """Test the SDLC orchestrator with different collaboration paradigms"""

    logger.info("SDLC Orchestrator Test Suite")
    logger.info("=" * 50)

    # Test Task: Create a simple web API
    test_task = "Create a REST API for a todo list application with CRUD operations"
    test_agents = ['gemini', 'claude', 'openai']

    paradigms = [
        'orchestra',
        'mesh',
        'swarm',
        'weaver',
        'ecosystem'
    ]

    for paradigm in paradigms:
        logger.info(f"\nTesting {paradigm.upper()} Paradigm")
        logger.info("-" * 40)

        try:
            session_id = f"test_{paradigm}"
            result = await orchestrator.collaborate(
                session_id=session_id,
                paradigm=paradigm,
                task=test_task,
                agents=test_agents
            )

            logger.info(f"Success: {result['paradigm']}")
            logger.info(f"Task: {result['task']}")
            logger.info(f"Agents: {', '.join(result['agents'])}")

            if 'conductor_guidance' in result:
                logger.info(f"Conductor: {result['conductor_guidance'][:100]}...")
            if 'conversations' in result:
                logger.info(f"Conversations: {len(result['conversations'])} exchanges")
            if 'emergent_patterns' in result:
                logger.info(f"Emergent Patterns: Available")
            if 'context_analysis' in result:
                logger.info(f"Context Analysis: Available")
            if 'emergent_synthesis' in result:
                logger.info(f"Ecosystem Evolution: Available")

        except Exception as e:
            logger.info(f"Error in {paradigm}: {e}")

    logger.info(f"\nTesting Bridge Services")
    logger.info("-" * 40)

    # Test bridge initialization
    bridge_result = await orchestrator.initialize_bridges()
    if bridge_result['success']:
        logger.info("Bridge services initialized successfully")

        # Test enhanced code generation
        code_result = await orchestrator.generate_code_with_bridges(
            "Create a Python function to validate email addresses",
            language="python",
            paradigm="orchestra"
        )
        logger.info(f"Enhanced Code Generation: {code_result.get('success', False)}")

    else:
        logger.info(f"Bridge services: {bridge_result.get('error', 'Not available')}")

    logger.info(f"\nOrchestrator Status")
    logger.info("-" * 40)
    logger.info(f"Active Sessions: {len(orchestrator.active_sessions)}")
    logger.info(f"Available Providers: {list(orchestrator.providers.keys())}")
    logger.info(f"Bridge Enhanced: {orchestrator.bridge_initialized}")

def test_orchestrator():
    asyncio.run(_async_test_orchestrator())


if __name__ == "__main__":
    logger.info("Starting SDLC Orchestrator Test...")
    asyncio.run(_async_test_orchestrator())
    logger.info("\nTest Complete!")
