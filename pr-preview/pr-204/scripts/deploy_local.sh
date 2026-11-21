#!/usr/bin/env bash

# Local deploy helper to mirror the GitHub Actions workflow steps:
# 1) Fetch GitHub stars (scripts/fetch_stars.py)
# 2) Build the site with Jekyll into ./_site
# 3) Serve the built site locally for testing
#
# Usage:
#   bash scripts/deploy_local.sh [--port 4000] [--skip-fetch]
#
# Notes:
# - Assumes "uv" is available and Python >= 3.10 is installed.
# - For the Jekyll build, Docker (jekyll/jekyll:4) is preferred to avoid
#   requiring a local Ruby/Jekyll install. If Docker is not available, we
#   fall back to a local "jekyll build" if present in PATH.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

PORT=4000
SKIP_FETCH=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)
      PORT=${2:-4000}
      shift 2
      ;;
    --skip-fetch)
      SKIP_FETCH=1
      shift
      ;;
    -h|--help)
      echo "Usage: bash scripts/deploy_local.sh [--port 4000] [--skip-fetch]"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

log() { printf "\033[1;34m[deploy-local]\033[0m %s\n" "$*"; }
warn() { printf "\033[1;33m[deploy-local]\033[0m %s\n" "$*"; }
err() { printf "\033[1;31m[deploy-local]\033[0m %s\n" "$*"; }

# 1) Fetch GitHub stars
if [[ "$SKIP_FETCH" -eq 0 ]]; then
  log "Fetching GitHub stars (scripts/fetch_stars.py)"
  # Run via uv, honoring the script's header for deps and Python version
  if ! uv run --script "${ROOT_DIR}/scripts/fetch_stars.py"; then
    err "Fetching stars failed."
    exit 1
  fi
else
  log "Skipping GitHub stars fetch (per --skip-fetch)."
fi

# 2) Build with Jekyll to ./_site
log "Building site with Jekyll into ${ROOT_DIR}/_site"
mkdir -p "${ROOT_DIR}/_site"

if command -v docker >/dev/null 2>&1; then
  log "Using Docker image jekyll/jekyll:4 for the build"
  docker run --rm \
    -e JEKYLL_ENV=production \
    -v "${ROOT_DIR}:/srv/jekyll" \
    -w /srv/jekyll \
    jekyll/jekyll:4 \
    jekyll build -s /srv/jekyll -d /srv/jekyll/_site
elif command -v jekyll >/dev/null 2>&1; then
  log "Docker not found. Falling back to local 'jekyll build'"
  jekyll build -s "${ROOT_DIR}" -d "${ROOT_DIR}/_site"
else
  err "Neither Docker nor a local 'jekyll' command is available."
  err "Install Docker (recommended) or Ruby Jekyll to build locally."
  exit 1
fi

# 3) Serve the built site locally
log "Serving ./_site at http://localhost:${PORT} (press Ctrl+C to stop)"
(cd "${ROOT_DIR}/_site" && python3 -m http.server "${PORT}")
