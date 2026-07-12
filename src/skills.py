#gotta figure out the right motors for this 
#turn clockwise
#turn counterclockwise
#move to starting 
#move to given location (where should this go, do more advanced math calculation)
import time 

JOINTS = [
    "shoulder_pan.pos",
    "shoulder_lift.pos",
    "elbow_flex.pos",
    "wrist_flex.pos",
    "wrist_roll.pos",
    "gripper.pos",
]

def get_joint_positions(robot):
    obs = robot.get_observation()
    return {joint: obs[joint] for joint in JOINTS}

# have it do movement here or in main? i think return action instead - so do movement loop till location met in main 
def decide_movement(robot_head, desired_pos): 
    #logic for turn?!?!
    return action or movemnt? 

#return action 
#is this direction correct? 
def turn_clockwise(robot, angle=10): 
    start = get_joint_positions(robot)
    action = {} 
    for joint in JOINTS: 
        if joint == "shoulder_pan.pos": 
            action[joint] = start[joint]+ angle
        else: 
            action[joint] = start[joint]
    return action 

#return action 
def turn_counterclockwise(robot, angle=10):
    start = get_joint_positions(robot)
    action = {} 
    for joint in JOINTS: 
        if joint == "shoulder_pan.pos": 
            action[joint] = start[joint] - angle
        else: 
            action[joint] = start[joint]
    return action 

#just do it directly - figure out what is the resting postion numbers 
def resting_position(robot): 
    current = get_joint_positions(robot)
    target = current.copy()
    target["shoulder_pan.pos"] = 45
    target["shoulder_lift.pos"] = 10
    target["elbow_flex.pos"] = 45
    target["wrist_flex.pos"] = 45 
    target["wrist_roll.pos"] = 45 
    target["gripper.pos"] = 45
    smooth_move(robot, target)

#from test, need to modify for this 
def smooth_move(robot, target, duration_s=2.0, hz=30):
    start = get_joint_positions(robot)
    steps = int(duration_s * hz)
    for i in range(1, steps + 1):
        alpha = i / steps
        action = {}
        for joint in JOINTS:
            action[joint] = start[joint] + alpha * (target[joint] - start[joint])
        robot.send_action(action)
        time.sleep(1 / hz)
