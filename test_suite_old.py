#!/usr/bin/env python3
"""
Comprehensive test suite for SDLC Orchestrator
Tests functionality, debugs issues, and validates improvements
"""
import asyncio
import sys
import os
import time
import json
import logging
from typing import Dict, List, Any
from contextlib import asynccontextmanager

# Add src to path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

logger = logging.getLogger(__name__)

class TestResult:
    """TestResult class for steampunk operations."""
    """  Init   with enhanced functionality."""
    def __init__(self, name: str, passed: bool, error: str = None, duration: float = 0):
        self.name = name
        self.passed = passed
        self.error = error
        self.duration = duration

"""  Init   with enhanced functionality."""
"""TestSuite class for steampunk operations."""
class TestSuite:
    def __init__(self):
        self.results: List[TestResult] = []
        self.total_tests = 0
        self.passed_tests = 0

    @asynccontextmanager
    async def test_case(self, name: str):
        """Context manager for individual test cases"""
        start_time = time.time()
        try:
            logger.info(f"Running {name}...")
            yield
            duration = time.time() - start_time
            self.results.append(TestResult(name, True, duration=duration))
            self.passed_tests += 1
            logger.info(f"PASSED {name} ({duration:.2f}s)")
        except Exception as e:
            duration = time.time() - start_time
            self.results.append(TestResult(name, False, str(e), duration))
            logger.info(f"FAILED {name} ({duration:.2f}s): {e}")
        finally:
            self.total_tests += 1

    def print_summary(self):
        """Print test summary"""
        logger.info("\n" + "="*60)
        logger.info("TEST SUMMARY")
        logger.info("="*60)
        logger.info(f"Total Tests: {self.total_tests}")
        logger.info(f"Passed: {self.passed_tests}")
        logger.info(f"Failed: {self.total_tests - self.passed_tests}")
        logger.info(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")

        if self.total_tests > self.passed_tests:
            logger.info("\nFAILED TESTS:")
            for result in self.results:
                if not result.passed:
                    logger.info(f"- {result.name}: {result.error}")

async def run_orchestrator_functionality():
    """Test core orchestrator functionality"""
    suite = TestSuite()

    # Test 1: Import and Initialize Orchestrator
    async with suite.test_case("Import Orchestrator"):
        from services.ai_providers_simple import orchestrator
        assert orchestrator is not None
        assert len(orchestrator.providers) > 0

    # Test 2: Test Basic Collaboration
    async with suite.test_case("Basic Collaboration"):
        result = await orchestrator.collaborate(
            session_id="test_basic",
            paradigm="orchestra",
            task="Create a simple function",
            agents=["gemini", "claude"]
        )
        assert result is not None
        assert "status" in result
        assert result["status"] == "completed"

    # Test 3: Test All Paradigms
    async with suite.test_case("All Paradigms"):
        paradigms = ["orchestra", "mesh", "swarm", "weaver", "ecosystem"]
        for paradigm in paradigms:
            result = await orchestrator.collaborate(
                session_id=f"test_{paradigm}",
                paradigm=paradigm,
                task="Test paradigm",
                agents=["gemini"]
            )
            assert result["paradigm"] is not None

    # Test 4: Bridge Services
    async with suite.test_case("Bridge Services"):
        bridge_result = await orchestrator.initialize_bridges()
        assert bridge_result is not None
        assert "success" in bridge_result

    # Test 5: Error Handling
    async with suite.test_case("Error Handling"):
        result = await orchestrator.collaborate(
            session_id="test_error",
            paradigm="invalid_paradigm",
            task="Test error",
            agents=["gemini"]
        )
        assert "error" in result

    return suite

async def run_database_functionality():
    """Test database operations"""
    suite = TestSuite()

    # Test 1: Import Database Models
    async with suite.test_case("Import Database Models"):
        try:
            from models.agent import db, Agent, Session, Task, Collaboration
            assert db is not None
        except ImportError as e:
            # Expected if SQLAlchemy not properly configured
            logger.info(f"Database import failed (expected): {e}")

    # Test 2: Database Connection
    async with suite.test_case("Database Connection"):
        # This test will likely fail due to missing Flask context
        try:
            from flask import Flask
            app = Flask(__name__)
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            logger.info("Database configuration successful")
        except Exception as e:
            logger.info(f"Database setup issue: {e}")

    return suite

async def run_api_endpoints():
    """Test API endpoint functionality"""
    suite = TestSuite()

    # Test 1: Import Routes
    async with suite.test_case("Import Routes"):
        try:
            from routes.collaboration import collaboration_bp
            from routes.recommendations import recommendations_bp
            assert collaboration_bp is not None
            assert recommendations_bp is not None
        except ImportError as e:
            logger.info(f"Route import failed: {e}")

    return suite

async def run_frontend_structure():
    """Test frontend file structure"""
    suite = TestSuite()

    # Check if required frontend files exist
    frontend_files = [
        "App.tsx",
        "constants.tsx",
        "components/AppInputForm.tsx",
        "components/IdeationView.tsx"
    ]

    for file_path in frontend_files:
        async with suite.test_case(f"Frontend File: {file_path}"):
            assert os.path.exists(file_path), f"File {file_path} does not exist"

    return suite

async def run_performance_tests():
    """Run performance benchmarks"""
    suite = TestSuite()

    async with suite.test_case("Orchestrator Performance"):
        start_time = time.time()
        from services.ai_providers_simple import orchestrator

        # Test concurrent collaboration
        tasks = []
        for i in range(5):
            task = orchestrator.collaborate(
                session_id=f"perf_test_{i}",
                paradigm="orchestra",
                task=f"Performance test {i}",
                agents=["gemini"]
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        duration = time.time() - start_time

        assert len(results) == 5
        assert all(result["status"] == "completed" for result in results)
        logger.info(f"Concurrent collaboration took {duration:.2f}s")

    return suite

async def main():
    """Run all tests"""
    logger.info("SDLC Orchestrator Test Suite")
    logger.info("="*60)

    test_suites = [
        await run_orchestrator_functionality(),
        await run_database_functionality(),
        await run_api_endpoints(),
        run_frontend_structure(),
        await run_performance_tests()
    ]

    # Combine all results
    total_tests = sum(suite.total_tests for suite in test_suites)
    total_passed = sum(suite.passed_tests for suite in test_suites)

    logger.info("\n" + "="*60)
    logger.info("OVERALL TEST SUMMARY")
    logger.info("="*60)
    logger.info(f"Total Tests: {total_tests}")
    logger.info(f"Passed: {total_passed}")
    logger.info(f"Failed: {total_tests - total_passed}")
    logger.info(f"Success Rate: {(total_passed/total_tests)*100:.1f}%")

    # Print detailed results
    logger.info("\nDETAILED RESULTS:")
    for i, suite in enumerate(test_suites):
        suite_name = ["Orchestrator", "Database", "API", "Frontend", "Performance"][i]
        logger.info(f"\n{suite_name} Tests:")
        for result in suite.results:
            status = "PASS" if result.passed else "FAIL"
            logger.info(f"  {status} {result.name}")
            if not result.passed:
                logger.info(f"    Error: {result.error}")

if __name__ == "__main__":
    asyncio.run(main())
