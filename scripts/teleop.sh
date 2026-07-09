#!/bin/bash

lerobot-teleoperate \
 --robot.type=so101_follower \
 --robot.port=$ROBOT_PORT \
 --robot.id=rory \
 --teleop.type=so101_leader \
 --teleop.port=$TELEOP_PORT \
 --teleop.id=lorelai
