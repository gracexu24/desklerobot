#!/bin/bash

#error checking recommended by chat 
#run setup first 
if [ -z "$ROBOT_PORT" ]; then
  echo "Error: ROBOT_PORT is not set"
  exit 1
fi

if [ -z "$TELEOP_PORT" ]; then
  echo "Error: TELEOP_PORT is not set"
  exit 1
fi


lerobot-teleoperate \
 --robot.type=so101_follower \
 --robot.port=$ROBOT_PORT \
 --robot.id=rory \
 --teleop.type=so101_leader \
 --teleop.port=$TELEOP_PORT \
 --teleop.id=lorelai
