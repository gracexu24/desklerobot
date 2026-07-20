#!/bin/bash
# Install dependencies and export shared robot / teleop env vars.
# Usage:
#   ./scripts/setup.sh          # install + print env
#   source scripts/setup.sh     # export env into current shell

set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export HF_USER="${HF_USER:-Gracexu28}"
export ROBOT_PORT="${ROBOT_PORT:-/dev/tty.usbmodem5B415325441}"
export TELEOP_PORT="${TELEOP_PORT:-/dev/tty.usbmodem5B415332981}"
export ROBOT_ID="${ROBOT_ID:-rory}"
export TELEOP_ID="${TELEOP_ID:-lorelai}"
export POLICY_PATH="${POLICY_PATH:-models/act_desk_trash}"
export DATASET_REPO_ID="${DATASET_REPO_ID:-${HF_USER}/so101_desk_trash}"
export TASK="${TASK:-Pick up the trash and put it in trash can}"
export CAMERA_WIDTH="${CAMERA_WIDTH:-640}"
export CAMERA_HEIGHT="${CAMERA_HEIGHT:-480}"
export CAMERA_FPS="${CAMERA_FPS:-30}"

# Only install when executed directly (not when sourced).
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "Installing requirements..."
  pip install -r requirements.txt

  echo "Checking LeRobot robot modules..."
  python -c "import lerobot.robots, pkgutil; print([m.name for m in pkgutil.iter_modules(lerobot.robots.__path__)])"
  python -c "import lerobot.robots.so_follower as m; print(dir(m))"

  echo
  echo "Setup complete. Shared defaults:"
  echo "  HF_USER=${HF_USER}"
  echo "  ROBOT_PORT=${ROBOT_PORT}"
  echo "  TELEOP_PORT=${TELEOP_PORT}"
  echo "  ROBOT_ID=${ROBOT_ID}"
  echo "  TELEOP_ID=${TELEOP_ID}"
  echo "  POLICY_PATH=${POLICY_PATH}"
  echo "  DATASET_REPO_ID=${DATASET_REPO_ID}"
  echo
  echo "To export these into your shell: source scripts/setup.sh"
fi
