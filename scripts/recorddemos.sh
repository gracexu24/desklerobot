#!/bin/bash
# Record teleop demos for the desk trash task.
# Run: source scripts/setup.sh && ./scripts/recorddemos.sh

set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

HF_USER="${HF_USER:-Gracexu28}"
ROBOT_PORT="${ROBOT_PORT:-/dev/tty.usbmodem5B415325441}"
TELEOP_PORT="${TELEOP_PORT:-/dev/tty.usbmodem5B415332981}"
ROBOT_ID="${ROBOT_ID:-rory}"
TELEOP_ID="${TELEOP_ID:-lorelai}"
DATASET_REPO_ID="${DATASET_REPO_ID:-${HF_USER}/so101_desk_trash}"
TASK="${TASK:-Pick up the trash and put it in trash can}"
NUM_EPISODES="${NUM_EPISODES:-50}"
EPISODE_TIME_S="${EPISODE_TIME_S:-30}"
RESET_TIME_S="${RESET_TIME_S:-10}"
CAMERA_WIDTH="${CAMERA_WIDTH:-640}"
CAMERA_HEIGHT="${CAMERA_HEIGHT:-480}"
CAMERA_FPS="${CAMERA_FPS:-30}"

if [[ -z "${ROBOT_PORT}" || -z "${TELEOP_PORT}" ]]; then
  echo "Error: ROBOT_PORT and TELEOP_PORT must be set"
  exit 1
fi

echo "Recording ${NUM_EPISODES} episodes to ${DATASET_REPO_ID}"
echo "Task: ${TASK}"

lerobot-record \
  --robot.type=so101_follower \
  --robot.port="${ROBOT_PORT}" \
  --robot.id="${ROBOT_ID}" \
  --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: ${CAMERA_WIDTH}, height: ${CAMERA_HEIGHT}, fps: ${CAMERA_FPS}}}" \
  --teleop.type=so101_leader \
  --teleop.port="${TELEOP_PORT}" \
  --teleop.id="${TELEOP_ID}" \
  --display_data=true \
  --dataset.repo_id="${DATASET_REPO_ID}" \
  --dataset.num_episodes="${NUM_EPISODES}" \
  --dataset.single_task="${TASK}" \
  --dataset.episode_time_s="${EPISODE_TIME_S}" \
  --dataset.reset_time_s="${RESET_TIME_S}"
