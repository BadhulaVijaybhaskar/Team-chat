#!/usr/bin/env bash
# Build Astra Loop team-edition binaries + webapp and tag Docker image astra-loop:dev.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Prefer repo-pinned toolchains when present (Cloud Agent / local nvm).
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [[ -s "$NVM_DIR/nvm.sh" ]]; then
  # shellcheck disable=SC1090
  . "$NVM_DIR/nvm.sh"
  nvm use --silent "$(cat "$ROOT/.nvmrc" 2>/dev/null || echo 24.11.1)" >/dev/null 2>&1 || nvm use --silent 24.11.1 >/dev/null 2>&1 || true
fi
export PATH="${GO_BIN_DIR:-/usr/local/go-1.26.10/bin}:${PATH}"
export BUILD_ENTERPRISE=false
# Always write server binaries into server/bin (avoid inherited GOBIN pointing elsewhere).
export GOBIN="${GOBIN:-$ROOT/server/bin}"
mkdir -p "$GOBIN"
unset GOPATH

IMAGE_TAG="${IMAGE_TAG:-astra-loop:dev}"
SKIP_PACKAGE="${SKIP_PACKAGE:-0}"
SKIP_DOCKER="${SKIP_DOCKER:-0}"

echo "==> Go $(go version)"
echo "==> Node $(node -v)"

if [[ "$SKIP_PACKAGE" != "1" ]]; then
  echo "==> Installing webapp dependencies"
  make -C webapp node_modules

  echo "==> Building web client"
  make -C server build-client

  echo "==> Building Linux amd64 server (team edition)"
  make -C server setup-go-work
  make -C server build-linux-amd64

  echo "==> Packaging linux-amd64 team tarball"
  make -C server package-linux-amd64

  PACKAGE="$(ls -1t server/dist/mattermost-team-linux-amd64.tar.gz 2>/dev/null | head -1 || true)"
  if [[ -z "$PACKAGE" ]]; then
    # Fallback: some make versions put the archive next to dist/
    PACKAGE="$(ls -1t server/dist/*-team-linux-amd64.tar.gz 2>/dev/null | head -1 || true)"
  fi
  if [[ -z "$PACKAGE" || ! -f "$PACKAGE" ]]; then
    echo "ERROR: could not find mattermost-team-linux-amd64.tar.gz under server/dist" >&2
    ls -la server/dist || true
    exit 1
  fi

  cp -f "$PACKAGE" "$ROOT/astra-loop/mattermost-team-linux-amd64.tar.gz"
  echo "==> Package ready: astra-loop/mattermost-team-linux-amd64.tar.gz"
fi

if [[ "$SKIP_DOCKER" != "1" ]]; then
  echo "==> Building Docker image ${IMAGE_TAG}"
  docker build \
    -f astra-loop/Dockerfile \
    --build-arg MM_PACKAGE=mattermost-team-linux-amd64.tar.gz \
    -t "${IMAGE_TAG}" \
    "$ROOT/astra-loop"
  echo "==> Image built: ${IMAGE_TAG}"
  docker images "${IMAGE_TAG}"
fi

echo "==> Done. Run with:"
echo "    docker compose -f astra-loop/docker-compose.yml up -d"
