import json
from pathlib import Path

import torch

from lerobot.datasets.utils import build_dataset_frame
from lerobot.policies.utils import make_robot_action
from lerobot.utils.constants import OBS_STR
from lerobot.utils.control_utils import predict_action

POLICY_PATH = "models/act_desk_trash"
TASK = "Pick up the trash and put it in trash can"
DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

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


def run_policy_for_action(
    robot,
    observation,
    policy,
    preprocessor,
    postprocessor,
    dataset_meta,
    cfg,
):
    """Run one policy inference step and return a robot joint dictionary."""
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
    return make_robot_action(action_tensor, dataset_meta.features)