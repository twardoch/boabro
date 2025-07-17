#!/usr/bin/env python3
# this_file: scripts/build.py
"""Build script for boabro package."""

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
    """Main build function."""
    # Change to project root
    project_root = Path(__file__).parent.parent
    subprocess.run(["cd", str(project_root)], shell=True)
    
    print("🏗️  Building boabro package...")
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    run_command("rm -rf dist/ build/ src/boabro.egg-info/")
    
    # Run linting
    print("🔍 Running linting...")
    run_command("python -m ruff check src/boabro tests")
    run_command("python -m ruff format --check src/boabro tests")
    
    # Run type checking
    print("🔬 Running type checking...")
    run_command("python -m mypy src/boabro tests")
    
    # Run tests
    print("🧪 Running tests...")
    run_command("python -m pytest tests/ src/boabro/test_boabro.py -v")
    
    # Build package
    print("📦 Building package...")
    run_command("python -m build")
    
    # List built files
    print("✅ Build complete! Built files:")
    dist_path = Path("dist")
    if dist_path.exists():
        for file in dist_path.iterdir():
            print(f"  - {file}")
    
    print("🎉 Build successful!")

if __name__ == "__main__":
    main()