#!/bin/bash

set -e 

#activate enviroment 
conda activate lerobot 

export ROBOT_PORT= "/dev/tty.usbmodem5B415325441"
export TELEOP_PORT= "/dev/tty.usbmodem5B415332981"

#export ids? 

pip install -r requirements.txt 

#check where all the lerobot robots are 
python -c "import lerobot.robots, pkgutil; print([m.name for m in pkgutil.iter_modules(lerobot.robots.__path__)])"
python -c "import lerobot.robots.so_follower as m; print(dir(m))"