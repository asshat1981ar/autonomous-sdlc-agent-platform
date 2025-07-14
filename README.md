# Autonomous SDLC Agent Platform

This project provides an experimental platform for running an automated software development life cycle driven by AI agents. Tests are provided to validate the basic orchestration logic.

## Installation

1. **Create a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install the required packages**:

```bash
pip install -r requirements.txt
```

## Running the Test Suite

With the requirements installed, execute the tests using **pytest**. The project
uses `pytest-asyncio` for asynchronous tests, so a compatible version of Python
(3.11 or later) is recommended:

```bash
pytest -q
```

