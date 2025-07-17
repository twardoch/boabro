#!/usr/bin/env python3
# this_file: scripts/test.py
"""Test script for boabro package."""

import subprocess
import sys
from pathlib import Path

def run_command(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result

def main():
    """Main test function."""
    # Change to project root
    project_root = Path(__file__).parent.parent
    subprocess.run(["cd", str(project_root)], shell=True)
    
    print("🧪 Running boabro test suite...")
    
    # Run linting
    print("🔍 Running linting...")
    run_command("python -m ruff check src/boabro tests")
    
    # Run formatting check
    print("🎨 Checking formatting...")
    run_command("python -m ruff format --check src/boabro tests")
    
    # Run type checking
    print("🔬 Running type checking...")
    run_command("python -m mypy src/boabro tests")
    
    # Run unit tests
    print("🧪 Running unit tests...")
    run_command("python -m pytest tests/ src/boabro/test_boabro.py -v --cov=src/boabro --cov-report=term-missing")
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    main()