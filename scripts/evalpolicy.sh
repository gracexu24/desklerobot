#!/bin/bash
# Run evaluation episodes with the trained ACT policy.
# Run: source scripts/setup.sh && ./scripts/evalpolicy.sh

set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

HF_USER="${HF_USER:-Gracexu28}"
ROBOT_PORT="${ROBOT_PORT:-/dev/tty.usbmodem5B415325441}"
ROBOT_ID="${ROBOT_ID:-rory}"
POLICY_PATH="${POLICY_PATH:-models/act_desk_trash}"
TASK="${TASK:-Pick up the trash and put it in trash can}"
NUM_EPISODES="${NUM_EPISODES:-5}"
EPISODE_TIME_S="${EPISODE_TIME_S:-30}"
RESET_TIME_S="${RESET_TIME_S:-0}"
CAMERA_WIDTH="${CAMERA_WIDTH:-640}"
CAMERA_HEIGHT="${CAMERA_HEIGHT:-480}"
CAMERA_FPS="${CAMERA_FPS:-30}"
EVAL_REPO_ID="${EVAL_REPO_ID:-${HF_USER}/eval_act_desk_trash_$(date +%Y%m%d_%H%M%S)}"

if [[ ! -d "${POLICY_PATH}" ]]; then
  echo "Error: policy not found at ${POLICY_PATH}"
  echo "Download it first, e.g.:"
  echo "  huggingface-cli download Gracexu28/act_desk_trash --local-dir ${POLICY_PATH}"
  exit 1
fi

echo "Evaluating policy from ${POLICY_PATH}"
echo "Logging eval episodes to ${EVAL_REPO_ID}"

lerobot-record \
  --robot.type=so101_follower \
  --robot.port="${ROBOT_PORT}" \
  --robot.id="${ROBOT_ID}" \
  --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: ${CAMERA_WIDTH}, height: ${CAMERA_HEIGHT}, fps: ${CAMERA_FPS}}}" \
  --display_data=true \
  --policy.path="${POLICY_PATH}" \
  --dataset.repo_id="${EVAL_REPO_ID}" \
  --dataset.single_task="${TASK}" \
  --dataset.num_episodes="${NUM_EPISODES}" \
  --dataset.push_to_hub=false \
  --dataset.episode_time_s="${EPISODE_TIME_S}" \
  --dataset.reset_time_s="${RESET_TIME_S}"
