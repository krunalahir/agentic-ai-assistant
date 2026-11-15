"""Regression guard: the backend must not execute model-generated code.

The python_interpreter tool passed LLM-written code to exec() with full
builtins, which allowed arbitrary code execution. It was removed; this
test fails if anything like it comes back.
"""

import re
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent / "src" / "backend" / "langraph_database.py"


def read_backend_source():
    return BACKEND.read_text(encoding="utf-8")


def test_no_exec_of_model_generated_code():
    source = read_backend_source()
    assert not re.search(r"\bexec\s*\(", source), "exec() found in backend workflow"


def test_no_python_interpreter_tool():
    source = read_backend_source()
    assert "python_interpreter" not in source


def test_no_code_specialist_worker():
    source = read_backend_source()
    assert "CodeSpecialist" not in source
