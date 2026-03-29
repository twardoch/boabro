# GitHub Actions Workflows

These workflow files must be added manually to the repository due to GitHub App permission limitations.

## Required Files

1. **`ci.yml`** - Continuous Integration
   - Runs on push/PR to main and develop branches
   - Tests Python 3.10, 3.11, 3.12
   - Executes linting, type checking, and unit tests
   - Includes HTML example integration testing

2. **`release.yml`** - Release Management
   - Triggers on git tags matching pattern `v*`
   - Runs complete test suite across all Python versions
   - Builds multiplatform binaries (Linux, Windows, macOS)
   - Creates GitHub releases with attached binaries
   - Publishes packages to PyPI

## Setup Instructions

1. Copy workflow files to `.github/workflows/`
2. Commit and push changes
3. Workflows activate automatically

## Required Secrets

Add this secret in GitHub repository settings for release workflow:

- `PYPI_TOKEN` - PyPI API token for package publishing

## Workflow Triggers

- CI runs on every push or pull request
- Release runs when pushing git tags like `v1.0.1`

## Release Commands

```bash
# Manual tagging
git tag -a v1.0.1 -m "Release v1.0.1"
git push --tags

# Automated tagging via script
python scripts/release.py patch  # or minor/major
```