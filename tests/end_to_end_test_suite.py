#!/usr/bin/env python3
"""
Comprehensive End-to-End Test Suite
Tests all components of the Steampunk A2A MCP Integration Framework
"""

import asyncio
import json
import time
import os
import sys
import unittest
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import tempfile
import subprocess

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestResult:
    """TestResult class for steampunk operations."""
    """  Init   with enhanced functionality."""
    def __init__(self, test_name: str, success: bool, details: str = "", duration: float = 0.0):
        self.test_name = test_name
        self.success = success
        self.details = details
        self.duration = duration
        self.timestamp = datetime.now()

class EndToEndTestSuite:
    """Comprehensive test suite for the entire system"""
    """  Init   with enhanced functionality."""

    def __init__(self):
        self.test_results: List[TestResult] = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.start_time = time.time()

    def add_result(self, result: TestResult):
        """Add a test result and update counters"""
        self.test_results.append(result)
        self.total_tests += 1
        if result.success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1

        status = "✅ PASS" if result.success else "❌ FAIL"
        logger.info(f"   {status} {result.test_name} ({result.duration:.3f}s)")
        if not result.success and result.details:
            logger.info(f"        Details: {result.details}")

    async def run_test(self, test_name: str, test_func, *args, **kwargs) -> TestResult:
        """Run a single test with timing and error handling"""
        start_time = time.time()
        try:
            if asyncio.iscoroutinefunction(test_func):
                success, details = await test_func(*args, **kwargs)
            else:
                success, details = test_func(*args, **kwargs)

            duration = time.time() - start_time
            result = TestResult(test_name, success, details, duration)
            self.add_result(result)
            return result

        except Exception as e:
            duration = time.time() - start_time
            result = TestResult(test_name, False, f"Exception: {str(e)}", duration)
            self.add_result(result)
            return result

    # ========== INFRASTRUCTURE TESTS ==========

    def test_file_structure(self) -> tuple[bool, str]:
        """Test that all required files exist"""
        required_files = [
            'styles/steampunk.css',
            'components/SteampunkFileUpload.tsx',
            'components/SteampunkChatInterface.tsx',
            'components/SteampunkGitHubIntegration.tsx',
            'components/SteampunkAgentDevelopment.tsx',
            'components/SteampunkApp.tsx',
            'src/services/bridges/mcp_bridge.py',
            'src/services/bridges/bridge_manager.py',
            'src/services/bridges/github_codex_bridge.py',
            'a2a_mcp_coordinator.py',
            'refactored_orchestrator.py'
        ]

        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)

        if missing_files:
            return False, f"Missing files: {', '.join(missing_files)}"
        return True, f"All {len(required_files)} required files present"

    def test_python_imports(self) -> tuple[bool, str]:
        """Test that all Python modules can be imported"""
        import_tests = [
            ('src.services.bridges.mcp_bridge', 'mcp_bridge'),
            ('src.services.bridges.bridge_manager', 'bridge_manager'),
            ('src.services.bridges.github_codex_bridge', 'github_codex_bridge'),
        ]

        failed_imports = []
        for module_path, object_name in import_tests:
            try:
                module = __import__(module_path, fromlist=[object_name])
                getattr(module, object_name)
            except Exception as e:
                failed_imports.append(f"{module_path}.{object_name}: {str(e)}")

        if failed_imports:
            return False, f"Failed imports: {'; '.join(failed_imports)}"
        return True, f"All {len(import_tests)} imports successful"

    def test_css_syntax(self) -> tuple[bool, str]:
        """Test CSS file syntax"""
        css_file = 'styles/steampunk.css'
        try:
            with open(css_file, 'r') as f:
                content = f.read()

            # Basic CSS syntax checks
            brace_open = content.count('{')
            brace_close = content.count('}')

            if brace_open != brace_close:
                return False, f"Mismatched braces: {brace_open} open, {brace_close} close"

            # Check for required CSS variables
            required_vars = ['--brass-primary', '--copper', '--steel-blue', '--antique-white']
            missing_vars = [var for var in required_vars if var not in content]

            if missing_vars:
                return False, f"Missing CSS variables: {', '.join(missing_vars)}"

            return True, f"CSS syntax valid, {brace_open} rules found"

        except Exception as e:
            return False, f"CSS file error: {str(e)}"

    def test_tsx_syntax(self) -> tuple[bool, str]:
        """Test TypeScript/TSX file syntax"""
        tsx_files = [
            'components/SteampunkFileUpload.tsx',
            'components/SteampunkChatInterface.tsx',
            'components/SteampunkGitHubIntegration.tsx',
            'components/SteampunkAgentDevelopment.tsx',
            'components/SteampunkApp.tsx'
        ]

        syntax_errors = []
        for tsx_file in tsx_files:
            try:
                with open(tsx_file, 'r') as f:
                    content = f.read()

                # Basic syntax checks
                if not content.strip().startswith('import'):
                    syntax_errors.append(f"{tsx_file}: Missing imports")

                if 'export' not in content:
                    syntax_errors.append(f"{tsx_file}: Missing export")

                if content.count('{') != content.count('}'):
                    syntax_errors.append(f"{tsx_file}: Mismatched braces")

            except Exception as e:
                syntax_errors.append(f"{tsx_file}: {str(e)}")

        if syntax_errors:
            return False, f"TSX syntax errors: {'; '.join(syntax_errors)}"
        return True, f"All {len(tsx_files)} TSX files have valid syntax"

    # ========== MCP BRIDGE TESTS ==========

    async def test_mcp_bridge_initialization(self) -> tuple[bool, str]:
        """Test MCP bridge initialization"""
        try:
            from src.services.bridges.mcp_bridge import mcp_bridge

            # Test database initialization
            if not os.path.exists(mcp_bridge.db_path):
                return False, "MCP bridge database not created"

            # Test server discovery
            if not mcp_bridge.servers:
                return False, "No MCP servers discovered"

            expected_servers = ['perplexity', 'notion', 'eslint', 'deepseek', 'jenkins']
            found_servers = list(mcp_bridge.servers.keys())
            missing_servers = [s for s in expected_servers if s not in found_servers]

            if missing_servers:
                return False, f"Missing servers: {', '.join(missing_servers)}"

            return True, f"MCP bridge initialized with {len(found_servers)} servers"

        except Exception as e:
            return False, f"MCP bridge initialization failed: {str(e)}"

    async def test_mcp_bridge_health_check(self) -> tuple[bool, str]:
        """Test MCP bridge health check functionality"""
        try:
            from src.services.bridges.mcp_bridge import mcp_bridge

            health_result = await mcp_bridge.health_check()

            if not isinstance(health_result, dict):
                return False, "Health check did not return dict"

            required_fields = ['status', 'servers', 'healthy_servers', 'total_servers']
            missing_fields = [f for f in required_fields if f not in health_result]

            if missing_fields:
                return False, f"Health check missing fields: {', '.join(missing_fields)}"

            if health_result['total_servers'] == 0:
                return False, "No servers reported in health check"

            return True, f"Health check successful: {health_result['healthy_servers']}/{health_result['total_servers']} servers"

        except Exception as e:
            return False, f"Health check failed: {str(e)}"

    async def test_mcp_server_communication(self) -> tuple[bool, str]:
        """Test MCP server communication (simulated)"""
        try:
            from src.services.bridges.mcp_bridge import mcp_bridge

            # Test research functionality
            research_result = await mcp_bridge.research_documentation(
                "Python testing best practices",
                "normal"
            )

            if not research_result.get('success'):
                return False, f"Research failed: {research_result.get('error', 'Unknown error')}"

            # Test API discovery
            api_result = await mcp_bridge.discover_apis(
                "FastAPI",
                "REST API development"
            )

            if not api_result.get('success'):
                return False, f"API discovery failed: {api_result.get('error', 'Unknown error')}"

            return True, "MCP server communication successful"

        except Exception as e:
            return False, f"MCP communication failed: {str(e)}"

    # ========== BRIDGE MANAGER TESTS ==========

    async def test_bridge_manager_initialization(self) -> tuple[bool, str]:
        """Test bridge manager initialization"""
        try:
            from src.services.bridges.bridge_manager import bridge_manager, BridgeType

            # Check all bridges are registered
            expected_bridges = [
                BridgeType.CLAUDE_CODE,
                BridgeType.GEMINI_CLI,
                BridgeType.GITHUB_CODEX,
                BridgeType.BLACKBOX_AI,
                BridgeType.MCP_SERVER
            ]

            missing_bridges = [b for b in expected_bridges if b not in bridge_manager.bridges]

            if missing_bridges:
                return False, f"Missing bridges: {[b.value for b in missing_bridges]}"

            # Check capabilities are defined
            if not bridge_manager.bridge_capabilities:
                return False, "No bridge capabilities defined"

            return True, f"Bridge manager initialized with {len(bridge_manager.bridges)} bridges"

        except Exception as e:
            return False, f"Bridge manager initialization failed: {str(e)}"

    async def test_bridge_manager_health_check(self) -> tuple[bool, str]:
        """Test bridge manager health check"""
        try:
            from src.services.bridges.bridge_manager import bridge_manager

            status = await bridge_manager.get_bridge_status()

            required_fields = ['bridges', 'healthy_count', 'total_count', 'last_check']
            missing_fields = [f for f in required_fields if f not in status]

            if missing_fields:
                return False, f"Status missing fields: {', '.join(missing_fields)}"

            if status['total_count'] == 0:
                return False, "No bridges reported"

            return True, f"Bridge status: {status['healthy_count']}/{status['total_count']} healthy"

        except Exception as e:
            return False, f"Bridge status check failed: {str(e)}"

    async def test_bridge_manager_task_routing(self) -> tuple[bool, str]:
        """Test bridge manager task routing"""
        try:
            from src.services.bridges.bridge_manager import bridge_manager, TaskType

            # Test research task routing
            best_bridge = await bridge_manager.get_best_bridge(TaskType.RESEARCH)

            if not best_bridge:
                return False, "No bridge found for RESEARCH task"

            # Test code generation task routing
            best_bridge_code = await bridge_manager.get_best_bridge(TaskType.CODE_GENERATION)

            if not best_bridge_code:
                return False, "No bridge found for CODE_GENERATION task"

            return True, f"Task routing successful: {best_bridge.value} for research, {best_bridge_code.value} for code gen"

        except Exception as e:
            return False, f"Task routing failed: {str(e)}"

    # ========== A2A COORDINATOR TESTS ==========

    async def test_a2a_coordinator_initialization(self) -> tuple[bool, str]:
        """Test A2A coordinator initialization"""
        try:
            from a2a_mcp_coordinator import a2a_mcp_coordinator, AgentRole

            # Check agents are initialized
            if not a2a_mcp_coordinator.agents:
                return False, "No agents initialized"

            expected_roles = [
                AgentRole.RESEARCH_AGENT,
                AgentRole.CODE_ANALYZER,
                AgentRole.API_SCOUT,
                AgentRole.KNOWLEDGE_KEEPER,
                AgentRole.BUILD_MASTER,
                AgentRole.QUALITY_INSPECTOR
            ]

            missing_roles = [r for r in expected_roles if r not in a2a_mcp_coordinator.agents]

            if missing_roles:
                return False, f"Missing agent roles: {[r.value for r in missing_roles]}"

            return True, f"A2A coordinator initialized with {len(a2a_mcp_coordinator.agents)} agents"

        except Exception as e:
            return False, f"A2A coordinator initialization failed: {str(e)}"

    async def test_a2a_message_creation(self) -> tuple[bool, str]:
        """Test A2A message creation and structure"""
        try:
            from a2a_mcp_coordinator import a2a_mcp_coordinator

            message = await a2a_mcp_coordinator.create_message(
                sender="test_client",
                recipient="research_agent",
                intent="research_documentation",
                data={'query': 'test query'},
                context={'test': True}
            )

            required_fields = ['id', 'sender', 'recipient', 'intent', 'data', 'context', 'timestamp']
            missing_fields = [f for f in required_fields if not hasattr(message, f)]

            if missing_fields:
                return False, f"Message missing fields: {', '.join(missing_fields)}"

            if message.sender != "test_client":
                return False, f"Incorrect sender: {message.sender}"

            if message.recipient != "research_agent":
                return False, f"Incorrect recipient: {message.recipient}"

            return True, f"Message created successfully with ID: {message.id}"

        except Exception as e:
            return False, f"Message creation failed: {str(e)}"

    async def test_a2a_message_routing(self) -> tuple[bool, str]:
        """Test A2A message routing functionality"""
        try:
            from a2a_mcp_coordinator import a2a_mcp_coordinator

            # Test research agent routing
            message = await a2a_mcp_coordinator.create_message(
                sender="test_client",
                recipient="research_agent",
                intent="research_documentation",
                data={'query': 'FastAPI testing', 'detail_level': 'normal'}
            )

            result = await a2a_mcp_coordinator.route_message(message)

            if not result.get('success'):
                return False, f"Research routing failed: {result.get('error')}"

            # Test MCP server direct routing
            mcp_message = await a2a_mcp_coordinator.create_message(
                sender="test_client",
                recipient="mcp_server",
                intent="research_docs",
                data={'query': 'API testing patterns'}
            )

            mcp_result = await a2a_mcp_coordinator.route_message(mcp_message)

            if not mcp_result.get('success'):
                return False, f"MCP routing failed: {mcp_result.get('error')}"

            return True, "Message routing successful for both agent and MCP targets"

        except Exception as e:
            return False, f"Message routing failed: {str(e)}"

    # ========== ORCHESTRATOR TESTS ==========

    async def test_orchestrator_initialization(self) -> tuple[bool, str]:
        """Test orchestrator initialization"""
        try:
            from refactored_orchestrator import enhanced_orchestrator

            # Check providers are initialized
            if not enhanced_orchestrator.providers:
                return False, "No AI providers initialized"

            expected_providers = ['gemini', 'claude', 'openai', 'blackbox']
            missing_providers = [p for p in expected_providers if p not in enhanced_orchestrator.providers]

            if missing_providers:
                return False, f"Missing providers: {', '.join(missing_providers)}"

            return True, f"Orchestrator initialized with {len(enhanced_orchestrator.providers)} providers"

        except Exception as e:
            return False, f"Orchestrator initialization failed: {str(e)}"

    async def test_orchestrator_collaboration(self) -> tuple[bool, str]:
        """Test orchestrator collaboration functionality"""
        try:
            from refactored_orchestrator import enhanced_orchestrator

            result = await enhanced_orchestrator.collaborate(
                session_id="test_session",
                paradigm="mesh",
                task="Test collaboration functionality",
                agents=['claude', 'gemini'],
                context={'test': True}
            )

            if not result.get('success', True):  # Default to True if success not specified
                return False, f"Collaboration failed: {result.get('error')}"

            required_fields = ['paradigm', 'task', 'agents', 'status']
            missing_fields = [f for f in required_fields if f not in result]

            if missing_fields:
                return False, f"Collaboration result missing fields: {', '.join(missing_fields)}"

            return True, f"Collaboration successful: {result['paradigm']} with {len(result['agents'])} agents"

        except Exception as e:
            return False, f"Orchestrator collaboration failed: {str(e)}"

    # ========== INTEGRATION TESTS ==========

    async def test_full_workflow_integration(self) -> tuple[bool, str]:
        """Test complete workflow integration"""
        try:
            from a2a_mcp_coordinator import a2a_mcp_coordinator

            workflow_result = await a2a_mcp_coordinator.orchestrate_development_workflow({
                'name': 'Test Integration Project',
                'technology': 'Python',
                'project_type': 'API',
                'use_case': 'testing framework',
                'language': 'python',
                'generate_code': True,
                'requirements': ['testing', 'validation', 'documentation']
            })

            if not workflow_result.get('success'):
                return False, f"Workflow failed: {workflow_result.get('error')}"

            phases_completed = workflow_result.get('phases_completed', 0)
            if phases_completed < 3:  # At least 3 phases should complete
                return False, f"Only {phases_completed} phases completed, expected at least 3"

            return True, f"Full workflow integration successful: {phases_completed} phases completed"

        except Exception as e:
            return False, f"Full workflow integration failed: {str(e)}"

    # ========== PERFORMANCE TESTS ==========

    async def test_response_times(self) -> tuple[bool, str]:
        """Test system response times"""
        try:
            from a2a_mcp_coordinator import a2a_mcp_coordinator

            # Test message creation time
            start_time = time.time()
            message = await a2a_mcp_coordinator.create_message(
                sender="perf_test",
                recipient="research_agent",
                intent="research_documentation",
                data={'query': 'performance test'}
            )
            creation_time = time.time() - start_time

            # Test message routing time
            start_time = time.time()
            result = await a2a_mcp_coordinator.route_message(message)
            routing_time = time.time() - start_time

            # Performance thresholds
            max_creation_time = 0.1  # 100ms
            max_routing_time = 1.0   # 1 second

            if creation_time > max_creation_time:
                return False, f"Message creation too slow: {creation_time:.3f}s > {max_creation_time}s"

            if routing_time > max_routing_time:
                return False, f"Message routing too slow: {routing_time:.3f}s > {max_routing_time}s"

            return True, f"Performance acceptable: creation {creation_time:.3f}s, routing {routing_time:.3f}s"

        except Exception as e:
            return False, f"Performance test failed: {str(e)}"

    async def test_concurrent_operations(self) -> tuple[bool, str]:
        """Test concurrent operation handling"""
        try:
            from a2a_mcp_coordinator import a2a_mcp_coordinator

            # Create multiple concurrent messages
            tasks = []
            for i in range(5):
                message = await a2a_mcp_coordinator.create_message(
                    sender=f"concurrent_test_{i}",
                    recipient="research_agent",
                    intent="research_documentation",
                    data={'query': f'concurrent test {i}'}
                )
                tasks.append(a2a_mcp_coordinator.route_message(message))

            # Execute concurrently
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            total_time = time.time() - start_time

            # Check results
            successful_results = [r for r in results if isinstance(r, dict) and r.get('success')]
            exceptions = [r for r in results if isinstance(r, Exception)]

            if exceptions:
                return False, f"Concurrent operations had exceptions: {len(exceptions)}"

            if len(successful_results) < 4:  # At least 4 should succeed
                return False, f"Only {len(successful_results)}/5 concurrent operations succeeded"

            return True, f"Concurrent operations successful: {len(successful_results)}/5 in {total_time:.3f}s"

        except Exception as e:
            return False, f"Concurrent operations test failed: {str(e)}"

    # ========== MAIN TEST RUNNER ==========

    async def run_all_tests(self):
        """Run the complete test suite"""
        logger.info("🧪 STARTING COMPREHENSIVE END-TO-END TEST SUITE")
        logger.info("=" * 70)

        # Infrastructure Tests
        logger.info("\n📁 INFRASTRUCTURE TESTS")
        await self.run_test("File Structure Check", self.test_file_structure)
        await self.run_test("Python Imports", self.test_python_imports)
        await self.run_test("CSS Syntax Validation", self.test_css_syntax)
        await self.run_test("TSX Syntax Validation", self.test_tsx_syntax)

        # MCP Bridge Tests
        logger.info("\n🔧 MCP BRIDGE TESTS")
        await self.run_test("MCP Bridge Initialization", self.test_mcp_bridge_initialization)
        await self.run_test("MCP Bridge Health Check", self.test_mcp_bridge_health_check)
        await self.run_test("MCP Server Communication", self.test_mcp_server_communication)

        # Bridge Manager Tests
        logger.info("\n🌉 BRIDGE MANAGER TESTS")
        await self.run_test("Bridge Manager Initialization", self.test_bridge_manager_initialization)
        await self.run_test("Bridge Manager Health Check", self.test_bridge_manager_health_check)
        await self.run_test("Bridge Manager Task Routing", self.test_bridge_manager_task_routing)

        # A2A Coordinator Tests
        logger.info("\n🤖 A2A COORDINATOR TESTS")
        await self.run_test("A2A Coordinator Initialization", self.test_a2a_coordinator_initialization)
        await self.run_test("A2A Message Creation", self.test_a2a_message_creation)
        await self.run_test("A2A Message Routing", self.test_a2a_message_routing)

        # Orchestrator Tests
        logger.info("\n🎼 ORCHESTRATOR TESTS")
        await self.run_test("Orchestrator Initialization", self.test_orchestrator_initialization)
        await self.run_test("Orchestrator Collaboration", self.test_orchestrator_collaboration)

        # Integration Tests
        logger.info("\n🔗 INTEGRATION TESTS")
        await self.run_test("Full Workflow Integration", self.test_full_workflow_integration)

        # Performance Tests
        logger.info("\n⚡ PERFORMANCE TESTS")
        await self.run_test("Response Times", self.test_response_times)
        await self.run_test("Concurrent Operations", self.test_concurrent_operations)

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_duration = time.time() - self.start_time

        report = {
            'summary': {
                'total_tests': self.total_tests,
                'passed_tests': self.passed_tests,
                'failed_tests': self.failed_tests,
                'success_rate': (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0,
                'total_duration': total_duration,
                'average_test_duration': sum(r.duration for r in self.test_results) / len(self.test_results) if self.test_results else 0
            },
            'results': [
                {
                    'test_name': r.test_name,
                    'success': r.success,
                    'details': r.details,
                    'duration': r.duration,
                    'timestamp': r.timestamp.isoformat()
                }
                for r in self.test_results
            ],
            'failed_tests': [
                {
                    'test_name': r.test_name,
                    'details': r.details,
                    'duration': r.duration
                }
                for r in self.test_results if not r.success
            ]
        }

        return report

    def print_summary(self):
        """Print test summary"""
        total_duration = time.time() - self.start_time
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0

        logger.info(f"\n🎯 TEST SUMMARY")
        logger.info("=" * 50)
        logger.info(f"   Total Tests: {self.total_tests}")
        logger.info(f"   Passed: {self.passed_tests} ✅")
        logger.info(f"   Failed: {self.failed_tests} ❌")
        logger.info(f"   Success Rate: {success_rate:.1f}%")
        logger.info(f"   Total Duration: {total_duration:.2f}s")

        if self.failed_tests > 0:
            logger.info(f"\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result.success:
                    logger.info(f"   • {result.test_name}: {result.details}")

        overall_status = "✅ ALL TESTS PASSED" if self.failed_tests == 0 else "❌ SOME TESTS FAILED"
        logger.info(f"\n{overall_status}")

async def main():
    """Main test runner"""
    test_suite = EndToEndTestSuite()

    try:
        await test_suite.run_all_tests()
        test_suite.print_summary()

        # Generate detailed report
        report = test_suite.generate_report()

        # Save report to file
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"\n📄 Detailed report saved to: {report_file}")

        # Return exit code based on test results
        return 0 if test_suite.failed_tests == 0 else 1

    except Exception as e:
        logger.info(f"\n💥 TEST SUITE CRASHED: {str(e)}")
        return 2

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)