#code by chat 

import json
import time
from pathlib import Path

import torch

# =========================
# EDIT THESE VALUES
# =========================

POLICY_PATH = "models/act_desk_trash"
TASK = "Pick up the trash and put it in trash can"
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
DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

# =========================
# ROBOT SETUP
# =========================

def create_robot():
    """
    Creates the SO-101 follower robot.

    If this import fails, your LeRobot version may use a slightly different
    module/class name.
    """

    from lerobot.cameras.opencv import OpenCVCameraConfig
    from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig

    config = SO101FollowerConfig(
        port=ROBOT_PORT,
        id=ROBOT_ID,
        cameras={
            "front": OpenCVCameraConfig(
                index_or_path=0,
                width=640,
                height=480,
                fps=30,
            )
        },
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

    from lerobot.configs.policies import PreTrainedConfig
    from lerobot.datasets.lerobot_dataset import LeRobotDatasetMetadata
    from lerobot.policies.factory import make_policy, make_pre_post_processors

    policy_path = Path(POLICY_PATH)
    train_config = json.loads((policy_path / "train_config.json").read_text())
    dataset_repo_id = train_config["dataset"]["repo_id"]

    cfg = PreTrainedConfig.from_pretrained(POLICY_PATH)
    cfg.pretrained_path = policy_path
    cfg.device = DEVICE

    dataset_meta = LeRobotDatasetMetadata(dataset_repo_id)
    policy = make_policy(cfg, ds_meta=dataset_meta)
    preprocessor, postprocessor = make_pre_post_processors(
        policy_cfg=cfg,
        pretrained_path=POLICY_PATH,
        dataset_stats=dataset_meta.stats,
        preprocessor_overrides={
            "device_processor": {"device": cfg.device},
        },
    )

    policy.eval()
    return policy, preprocessor, postprocessor, dataset_meta, cfg


# =========================
# MAIN LOOP
# =========================

def main():
    robot = create_robot()
    policy, preprocessor, postprocessor, dataset_meta, cfg = load_policy()

    from lerobot.datasets.utils import build_dataset_frame
    from lerobot.policies.utils import make_robot_action
    from lerobot.utils.constants import OBS_STR
    from lerobot.utils.control_utils import predict_action

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
            observation_frame = build_dataset_frame(dataset_meta.features, observation, prefix=OBS_STR)
            action_tensor = predict_action(
                observation=observation_frame,
                policy=policy,
                device=torch.device(cfg.device),
                preprocessor=preprocessor,
                postprocessor=postprocessor,
                use_amp=cfg.use_amp,
                task=TASK,
                robot_type=robot.name,
            )
            action = make_robot_action(action_tensor, dataset_meta.features)

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