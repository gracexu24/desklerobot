#!/bin/bash
# Train an ACT policy on the desk trash dataset.
# Run: source scripts/setup.sh && ./scripts/trainpolicy.sh

set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

HF_USER="${HF_USER:-Gracexu28}"
DATASET="${DATASET:-${HF_USER}/so101_desk_trash_merged}"
POLICY_REPO_ID="${POLICY_REPO_ID:-${HF_USER}/act_desk_trash}"
OUTPUT_DIR="${OUTPUT_DIR:-outputs/train/act_so101_desk_trash}"
JOB_NAME="${JOB_NAME:-act_desk_trash}"

POLICY_DEVICE="${POLICY_DEVICE:-mps}"

echo "Training ACT on ${DATASET}"
echo "Output: ${OUTPUT_DIR}"
echo "Hub repo: ${POLICY_REPO_ID}"
echo "Device: ${POLICY_DEVICE}"

lerobot-train \
  --dataset.repo_id="${DATASET}" \
  --policy.type=act \
  --output_dir="${OUTPUT_DIR}" \
  --job_name="${JOB_NAME}" \
  --policy.device="${POLICY_DEVICE}" \
  --wandb.enable=false \
  --policy.repo_id="${POLICY_REPO_ID}"
