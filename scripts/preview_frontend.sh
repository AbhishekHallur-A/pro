#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-8000}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../frontend" && pwd)"

echo "Serving frontend from ${DIR} on http://localhost:${PORT}"
python -m http.server "${PORT}" --directory "${DIR}"
