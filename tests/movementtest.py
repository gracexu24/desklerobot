import time
from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig

#chat generate test code, modified for tests I wanted 

ROBOT_PORT = "/dev/tty.usbmodem5B415325441"
ROBOT_ID = "rory"

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


def main():
    robot = SO101Follower(
        SO101FollowerConfig(
            port=ROBOT_PORT,
            id=ROBOT_ID,
            max_relative_target=15.0,
        )
    )

    robot.connect()

    try:
        current = get_joint_positions(robot)

        # Example target: rotate base, lower shoulder a little, open gripper
        target = current.copy()
        target["shoulder_pan.pos"] += 15
        target["shoulder_lift.pos"] = 10
        target["elbow_flex.pos"] = 45
        target["wrist_flex.pos"] = 45 
        target["wrist_roll.pos"] = 45 
        target["gripper.pos"] = 45

        smooth_move(robot, target, duration_s=2.0)

        time.sleep(1)

        # Return to original pose
        smooth_move(robot, current, duration_s=2.0)

    finally:
        robot.disconnect()


if __name__ == "__main__":
    main()