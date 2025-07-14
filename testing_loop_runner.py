import os
import subprocess
import asyncio
import time
from typing import List, Dict, Any

class TestingLoopRunner:
    """TestingLoopRunner class for steampunk operations."""
    """  Init   with enhanced functionality."""
    def __init__(self, orchestrator, agents: List[str], project_root: str = "."):
        self.orchestrator = orchestrator
        self.agents = agents
        self.project_root = project_root
        self.test_results = []

    def inspect_file_structure(self) -> List[str]:
        """
        Inspect the project directory to find source files for test generation.
        """
        source_files = []
        for root, _, files in os.walk(self.project_root):
            for file in files:
                if file.endswith(".py") and not file.startswith("test_"):
                    source_files.append(os.path.join(root, file))
        return source_files

    async def generate_test_stubs(self, source_files: List[str]) -> Dict[str, str]:
        """
        Generate pytest/unittest stubs for the given source files using AI.
        Returns a dict mapping source file to generated test code.
        """
        test_stubs = {}
        for source_file in source_files:
            prompt = f"Generate pytest test stubs for the Python source file: {source_file}."
            # Call orchestrator to generate test code
            response = await self.orchestrator.collaborate(
                session_id=f"testgen_{int(time.time())}",
                paradigm='orchestra',
                task=prompt,
                agents=self.agents,
                context={'mode': 'test_generation'}
            )
            test_code = response.get('synthesis', {}).get('key_insights', [])
            if test_code:
                test_stubs[source_file] = "\n".join(test_code)
            else:
                test_stubs[source_file] = "# Test generation failed or returned empty."
        return test_stubs

    def write_test_files(self, test_stubs: Dict[str, str]):
        """
        Write generated test stubs to test files in the project.
        """
        for source_file, test_code in test_stubs.items():
            test_file = os.path.join(
                os.path.dirname(source_file),
                f"test_{os.path.basename(source_file)}"
            )
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(test_code)

    def run_tests(self) -> Dict[str, Any]:
        """
        Run tests using pytest and gather results.
        """
        try:
            result = subprocess.run(
                ["pytest", "--json-report", "--json-report-file=report.json"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            with open(os.path.join(self.project_root, "report.json"), "r", encoding="utf-8") as f:
                report = f.read()
            self.test_results.append({
                "success": True,
                "output": result.stdout,
                "report": report
            })
            return self.test_results[-1]
        except subprocess.CalledProcessError as e:
            self.test_results.append({
                "success": False,
                "output": e.output,
                "error": str(e)
            })
            return self.test_results[-1]

    async def run_testing_loop(self):
        """
        Full testing loop: inspect files, generate tests, write files, run tests, and return results.
        """
        source_files = self.inspect_file_structure()
        test_stubs = await self.generate_test_stubs(source_files)
        self.write_test_files(test_stubs)
        test_results = self.run_tests()
        return test_results
