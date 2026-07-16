#needs the most improvement!
#improvements made: 
# - learn how to normalize movements to avoid hardcoding
# - try movement logic in test first 
# - remove extra observation call - imporve latency
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

# decide movement direct based on desired position
def decide_movement(robot, robot_head, desired_pos): 
    if (desired_pos[0] < robot_head[0] and desired_pos[1] > robot_head[1]): 
        return turn_counterclockwise(robot) 
    else: 
        return turn_clockwise(robot)

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

#gotta figure out reset postions - improve this so this is less of a jump 
def resting_position(robot): 
    current = get_joint_positions(robot)
    target = current.copy()
    target["shoulder_pan.pos"] = 45
    target["shoulder_lift.pos"] = 10
    target["elbow_flex.pos"] = 45
    target["wrist_flex.pos"] = 45 
    target["wrist_roll.pos"] = 45 
    target["gripper.pos"] = 45
    return target 
