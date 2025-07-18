# GitHub Actions Workflows

These workflow files need to be manually added to the repository due to GitHub App permissions.

## Files to Add

1. **`ci.yml`** - Continuous Integration workflow
   - Runs on push/PR to main/develop branches
   - Tests across Python 3.10, 3.11, 3.12
   - Runs linting, type checking, and tests
   - Includes integration testing for HTML examples

2. **`release.yml`** - Release workflow  
   - Triggers on git tags (v*)
   - Runs full test suite across Python versions
   - Builds multiplatform binaries (Linux, Windows, macOS)
   - Creates GitHub releases with binaries
   - Publishes to PyPI

## How to Add

1. Copy these files to `.github/workflows/` in your repository
2. Commit and push the changes
3. The workflows will automatically activate

## Required Secrets

For the release workflow to work, you'll need to add these secrets in your GitHub repository settings:

- `PYPI_TOKEN` - PyPI API token for publishing packages

## Testing

- CI workflow will run automatically on every push/PR
- Release workflow will run when you push a git tag like `v1.0.1`

## Usage

```bash
# Create a new release
git tag -a v1.0.1 -m "Release v1.0.1"
git push --tags

# Or use the release script
python scripts/release.py patch  # or minor/major
```