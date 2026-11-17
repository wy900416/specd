#!/usr/bin/env bash
# Run the workspace-local specd package from any directory.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="$ROOT/specd${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m specd --root "$ROOT" "$@"
