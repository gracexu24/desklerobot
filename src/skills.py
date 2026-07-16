#needs the most improvement!
#improvements made: 
# - learn how to normalize movements to avoid hardcoding
# - try movement logic in test first 
# - remove extra observation call - imporve latency

import time 
import math 

# Hardcoded shoulder-pan pivot in camera pixels: (x, y).
SHOULDER_PIVOT_PX = (90, 440)

JOINTS = [
    "shoulder_pan.pos",
    "shoulder_lift.pos",
    "elbow_flex.pos",
    "wrist_flex.pos",
    "wrist_roll.pos",
    "gripper.pos",
]

#dont call get_observation in skills 
def get_joint_positions(robot):
    obs = robot.get_observation()
    return {joint: obs[joint] for joint in JOINTS}

def joint_positions(observation):
    return {joint: float(observation[joint]) for joint in JOINTS}


#should lock target for moving! 
#hill climb vs PID?
#calibrate path marker method 
#def decide_movement(robot, robot_head, desired_pos):   
# decide movement direct based on desired position
#def decide_movement_old(robot, robot_head, desired_pos): 
#    if (desired_pos[0] < robot_head[0] and desired_pos[1] > robot_head[1]): 
#        return turn_counterclockwise(robot) 
#    else: 
#        return turn_clockwise(robot)

#return action 
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

def increment_resting_position(observation, desired_position, increment = 15): 
    current = {joint: observation[joint] for joint in JOINTS} 
    action = {}
    for joint in JOINTS:
        movement = desired_position[joint] - current[joint]
        if movement > increment: 
            action[joint] = current[joint] + increment
        elif movement < -increment:
            action[joint] = current[joint] - increment
        elif movement == 0:
            action[joint] = current[joint]
        else:
            action[joint] = desired_position[joint]
    return action

#just for initial resting position, not for movement
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


class PIDController:
    def __init__(
        self,
        kp,
        ki,
        kd,
        max_output,
        deadband,
        direction=1.0,
        integral_limit=500.0,
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_output = max_output
        self.deadband = deadband
        self.direction = direction
        self.integral_limit = integral_limit
        self.reset()

    def reset(self):
        self.integral = 0.0
        self.previous_error = None
        self.previous_time = None

    def update(self, error):
        now = time.monotonic()
        if abs(error) <= self.deadband:
            was_outside_deadband = (
                self.previous_error is not None
                and abs(self.previous_error) > self.deadband
            )
            self.reset()
            if was_outside_deadband:
                print("Aligned (within angular deadband)")
            return 0.0

        if self.previous_time is None:
            dt = 0.0
            derivative = 0.0
        else:
            dt = max(now - self.previous_time, 1e-6)
            derivative = (error - self.previous_error) / dt

        if dt > 0.0:
            self.integral += error * dt
            self.integral = max(
                -self.integral_limit,
                min(self.integral, self.integral_limit),
            )

        output = self.direction * (
            self.kp * error
            + self.ki * self.integral
            + self.kd * derivative
        )
        output = max(-self.max_output, min(output, self.max_output))
        self.previous_error = error
        self.previous_time = now
        return output


def calculate_angular_error(robot_head, desired_position, pivot):
    """Return signed shortest angular error from the red marker to the target.

    All inputs are image coordinates in (x, y) pixel order. Positive and
    negative errors represent opposite shoulder-pan directions.
    """
    robot_angle = math.atan2(
        float(robot_head[1] - pivot[1]),
        float(robot_head[0] - pivot[0]),
    )
    target_angle = math.atan2(
        float(desired_position[1] - pivot[1]),
        float(desired_position[0] - pivot[0]),
    )

    raw_error = target_angle - robot_angle

    # Normalize to [-pi, pi] so the robot chooses the shorter turn.
    wrapped_error = math.atan2(
        math.sin(raw_error),
        math.cos(raw_error),
    )
    return math.degrees(wrapped_error)


def pid_movement(observation, robot_head, desired_position, controller):
    action = joint_positions(observation)
    if robot_head is None or desired_position is None:
        controller.reset()
        return action, None, 0.0

    angular_error = calculate_angular_error(
        robot_head,
        desired_position,
        SHOULDER_PIVOT_PX,
    )
    pan_delta = controller.update(angular_error)
    action["shoulder_pan.pos"] += pan_delta
    return action, angular_error, pan_delta

