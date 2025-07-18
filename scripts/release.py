#!/usr/bin/env python3
# this_file: scripts/release.py
"""Release script for boabro package."""

import subprocess
import sys
import re
from pathlib import Path
from typing import Optional

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

def get_current_version() -> str:
    """Get the current version from git tags."""
    result = run_command("git describe --tags --abbrev=0", check=False)
    if result.returncode == 0:
        return result.stdout.strip()
    return "v0.0.0"

def increment_version(current_version: str, bump_type: str) -> str:
    """Increment version based on bump type."""
    # Remove 'v' prefix if present
    version = current_version.lstrip('v')
    
    # Parse version components
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)(?:-(.+))?$', version)
    if not match:
        print(f"Invalid version format: {version}")
        sys.exit(1)
    
    major, minor, patch = map(int, match.groups()[:3])
    
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        print(f"Invalid bump type: {bump_type}. Use 'major', 'minor', or 'patch'")
        sys.exit(1)
    
    return f"v{major}.{minor}.{patch}"

def update_changelog(version: str) -> None:
    """Update CHANGELOG.md with the new version."""
    changelog_path = Path("CHANGELOG.md")
    if not changelog_path.exists():
        print("CHANGELOG.md not found")
        return
    
    content = changelog_path.read_text()
    
    # Replace [Unreleased] with the new version
    import datetime
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    content = content.replace(
        "## [Unreleased]",
        f"## [Unreleased]\n\n## [{version.lstrip('v')}] - {today}"
    )
    
    changelog_path.write_text(content)
    print(f"Updated CHANGELOG.md with version {version}")

def main():
    """Main release function."""
    if len(sys.argv) != 2:
        print("Usage: python scripts/release.py <major|minor|patch>")
        sys.exit(1)
    
    bump_type = sys.argv[1]
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    subprocess.run(["cd", str(project_root)], shell=True)
    
    # Check if working directory is clean
    result = run_command("git status --porcelain", check=False)
    if result.stdout.strip():
        print("Working directory is not clean. Please commit or stash changes.")
        sys.exit(1)
    
    # Get current version and increment
    current_version = get_current_version()
    new_version = increment_version(current_version, bump_type)
    
    print(f"🚀 Releasing version {new_version} (was {current_version})")
    
    # Update changelog
    update_changelog(new_version)
    
    # Run full test suite
    print("🧪 Running full test suite...")
    run_command("python scripts/test.py")
    
    # Build the package
    print("🏗️  Building package...")
    run_command("python scripts/build.py")
    
    # Commit changelog changes
    print("📝 Committing changelog updates...")
    run_command("git add CHANGELOG.md")
    run_command(f'git commit -m "Update changelog for {new_version}"')
    
    # Create and push tag
    print(f"🏷️  Creating tag {new_version}...")
    run_command(f'git tag -a {new_version} -m "Release {new_version}"')
    
    # Push changes and tag
    print("🚢 Pushing changes and tags...")
    run_command("git push")
    run_command("git push --tags")
    
    print(f"✅ Release {new_version} completed successfully!")
    print(f"🎉 GitHub Actions will now build and publish the release.")

if __name__ == "__main__":
    main()