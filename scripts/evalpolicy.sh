#!/bin/bash

set -e 

#run 5 tests
lerobot-record \
    --robot.type=so101_follower \
    --robot.port=/dev/tty.usbmodem5B415325441 \
    --robot.id=rory \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" \
    --display_data=true \
    --dataset.repo_id=Gracexu28/act_desk_trash\
    --dataset.single_task="Pick up the trash and put it in trash can" \
    --dataset.num_episodes=5 \
    --dataset.push_to_hub=false \
    --dataset.episode_time_s=30 \
    --dataset.reset_time_s=15 \
