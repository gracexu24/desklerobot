#code by chat 

import time
import torch

# =========================
# EDIT THESE VALUES
# =========================

POLICY_PATH = "Gracexu28/act_desk_trash"
# Example local:
# POLICY_PATH = "/Users/gracexu/lerobot/outputs/train/act_pick_cube/checkpoints/last/pretrained_model"

# Example Hugging Face:
# POLICY_PATH = "your_hf_username/your_policy_name"

ROBOT_PORT = "/dev/tty.usbmodem5B415325441"
# Example:
# ROBOT_PORT = "/dev/tty.usbmodem575E0032081"

ROBOT_ID = "rory"

SECONDS = 30.0
FPS = 30.0
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# =========================
# ROBOT SETUP
# =========================

def create_robot():
    """
    Creates the SO-101 follower robot.

    If this import fails, your LeRobot version may use a slightly different
    module/class name.
    """

    from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig

    config = SO101FollowerConfig(
        port=ROBOT_PORT,
        id=ROBOT_ID,
    )

    robot = SO101Follower(config)
    return robot


# =========================
# POLICY SETUP
# =========================

def load_policy():
    """
    Loads the trained ACT policy.
    """

    from lerobot.policies.factory import make_policy
    from lerobot.configs.policies import PreTrainedConfig

    cfg = PreTrainedConfig.from_pretrained(POLICY_PATH)
    policy = make_policy(cfg)
    policy.from_pretrained(POLICY_PATH)

    policy.to(DEVICE)
    policy.eval()

    return policy


# =========================
# MAIN LOOP
# =========================

def main():
    robot = create_robot()
    policy = load_policy()

    dt = 1.0 / FPS

    robot.connect(calibrate=False)

    print("Robot connected.")
    print("Observation features:")
    print(robot.observation_features)

    print("Action features:")
    print(robot.action_features)

    print(f"Running policy for {SECONDS} seconds...")

    start_time = time.time()

    try:
        while time.time() - start_time < SECONDS:
            loop_start = time.time()

            observation = robot.get_observation()

            with torch.no_grad():
                action = policy.select_action(observation)

            robot.send_action(action)

            elapsed = time.time() - loop_start
            time.sleep(max(0.0, dt - elapsed))

    except KeyboardInterrupt:
        print("Stopped by user.")

    finally:
        robot.disconnect()
        print("Robot disconnected.")


if __name__ == "__main__":
    main()