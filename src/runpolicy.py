import json
import time
from pathlib import Path

import torch

POLICY_PATH = "models/act_desk_trash"
TASK = "Pick up the trash and put it in trash can"
ROBOT_PORT = "/dev/tty.usbmodem5B415325441"
ROBOT_ID = "rory"

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
