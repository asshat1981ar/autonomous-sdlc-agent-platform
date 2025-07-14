import unittest
import io
import sys
from contextlib import redirect_stdout
import generated_self_directed_prompt

class TestGeneratedSelfDirectedPrompt(unittest.TestCase):
    """TestGeneratedSelfDirectedPrompt class for steampunk operations."""
    """Test Prompt Output with enhanced functionality."""
    def test_prompt_output(self):
        f = io.StringIO()
        with redirect_stdout(f):
            exec(open("generated_self_directed_prompt.py").read())
        output = f.getvalue()
        self.assertIn("You are an autonomous software development orchestrator", output)
        self.assertIn("Generate a self-directed prompt that guides AI agents", output)
        self.assertIn("Create a detailed, structured prompt that can be used to initiate and sustain autonomous development loops.", output)
        self.assertIn("Format the prompt as a multi-line string", output)
        self.assertIn("USER TURN", output)
        self.assertIn("ASSISTANT TURN", output)

if __name__ == "__main__":
    unittest.main()
