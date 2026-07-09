#!/bin/bash

set -e 

# Run 5 evaluation episodes with a trained policy.
# Local copy is sanitized for the installed LeRobot version.
POLICY_PATH="models/act_desk_trash"
EVAL_REPO_ID="Gracexu28/eval_act_desk_trash_$(date +%Y%m%d_%H%M%S)"

lerobot-record \
    --robot.type=so101_follower \
    --robot.port=/dev/tty.usbmodem5B415325441 \
    --robot.id=rory \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" \
    --display_data=true \
    --policy.path="${POLICY_PATH}" \
    --dataset.repo_id="${EVAL_REPO_ID}" \
    --dataset.single_task="Pick up the trash and put it in trash can" \
    --dataset.num_episodes=5 \
    --dataset.push_to_hub=false \
    --dataset.episode_time_s=30 \
    --dataset.reset_time_s=0
