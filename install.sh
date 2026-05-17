#!/usr/bin/env bash
# install.sh — Install boabro locally
# boabro provides browser-based font analysis tools powered by PyScript
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing boabro..."
uv pip install -e . 2>/dev/null || pip install -e . 2>/dev/null || echo "Install failed"
echo "Done."
