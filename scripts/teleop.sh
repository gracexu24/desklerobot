#!/bin/bash
# Teleoperate the SO101 follower with the leader arm.
# Run: source scripts/setup.sh && ./scripts/teleop.sh

set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ROBOT_PORT="${ROBOT_PORT:-/dev/tty.usbmodem5B415325441}"
TELEOP_PORT="${TELEOP_PORT:-/dev/tty.usbmodem5B415332981}"
ROBOT_ID="${ROBOT_ID:-rory}"
TELEOP_ID="${TELEOP_ID:-lorelai}"
CAMERA_WIDTH="${CAMERA_WIDTH:-640}"
CAMERA_HEIGHT="${CAMERA_HEIGHT:-480}"
CAMERA_FPS="${CAMERA_FPS:-30}"

if [[ -z "${ROBOT_PORT}" ]]; then
  echo "Error: ROBOT_PORT is not set"
  exit 1
fi

if [[ -z "${TELEOP_PORT}" ]]; then
  echo "Error: TELEOP_PORT is not set"
  exit 1
fi

lerobot-teleoperate \
  --robot.type=so101_follower \
  --robot.port="${ROBOT_PORT}" \
  --robot.id="${ROBOT_ID}" \
  --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: ${CAMERA_WIDTH}, height: ${CAMERA_HEIGHT}, fps: ${CAMERA_FPS}}}" \
  --teleop.type=so101_leader \
  --teleop.port="${TELEOP_PORT}" \
  --teleop.id="${TELEOP_ID}" \
  --display_data=true
