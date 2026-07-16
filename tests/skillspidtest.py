"""Test basic skills and PID visual alignment without policy or voice code.

The main loop owns perception and robot observations. Skill helpers only build
action dictionaries from the current observation.

Controls (camera window must be focused):
    A: one small counterclockwise shoulder-pan step
    D: one small clockwise shoulder-pan step
    P: PID-align the red marker horizontally with the nearest white object
    R: move toward the resting position
    Space: hold current position
    Q: hold and quit
"""

import sys
import time
from pathlib import Path

import cv2
import mediapipe as mp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from detection.objdetect import (
    calc_hand_distance,
    closest_trash,
    detect_human_hands,
    detect_red_head,
    detect_trash,
)
from safetysupervisor import decide_mode, filter_action

from lerobot.cameras.opencv import OpenCVCameraConfig
from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig

ROBOT_PORT = "/dev/tty.usbmodem5B415325441"
ROBOT_ID = "rory"
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

MANUAL_TURN_STEP = 1.0
PID_KP = 0.01
PID_KI = 0.0
PID_KD = 0.0
PID_MAX_STEP = 0.5
PID_DEADBAND_PX = 15.0
PID_DIRECTION = 1.0  # Change to -1.0 if the marker moves away from the target.

JOINTS = [
    "shoulder_pan.pos",
    "shoulder_lift.pos",
    "elbow_flex.pos",
    "wrist_flex.pos",
    "wrist_roll.pos",
    "gripper.pos",
]

REST_TARGET = {
    "shoulder_pan.pos": 45.0,
    "shoulder_lift.pos": 10.0,
    "elbow_flex.pos": 45.0,
    "wrist_flex.pos": 45.0,
    "wrist_roll.pos": 45.0,
    "gripper.pos": 45.0,
}


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
            self.reset()
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


def joint_positions(observation):
    return {joint: float(observation[joint]) for joint in JOINTS}


def hold_position(observation):
    return joint_positions(observation)


def turn_clockwise(observation):
    action = joint_positions(observation)
    action["shoulder_pan.pos"] += MANUAL_TURN_STEP
    return action


def turn_counterclockwise(observation):
    action = joint_positions(observation)
    action["shoulder_pan.pos"] -= MANUAL_TURN_STEP
    return action


def resting_position(observation):
    action = joint_positions(observation)
    action.update(REST_TARGET)
    return action


def pid_movement(observation, robot_head, desired_position, controller):
    action = joint_positions(observation)
    if robot_head is None or desired_position is None:
        controller.reset()
        return action, None, 0.0

    horizontal_error = float(desired_position[0] - robot_head[0])
    pan_delta = controller.update(horizontal_error)
    action["shoulder_pan.pos"] += pan_delta
    return action, horizontal_error, pan_delta


def create_robot():
    return SO101Follower(
        SO101FollowerConfig(
            port=ROBOT_PORT,
            id=ROBOT_ID,
            max_relative_target=2.0,
            cameras={
                "front": OpenCVCameraConfig(
                    index_or_path=0,
                    width=CAMERA_WIDTH,
                    height=CAMERA_HEIGHT,
                    fps=CAMERA_FPS,
                )
            },
        )
    )


def draw_status(display, control_mode, safety_mode, error, pan_delta):
    error_text = "n/a" if error is None else f"{error:.1f} px"
    lines = [
        f"Control: {control_mode}",
        f"Safety: {safety_mode}",
        f"Horizontal error: {error_text}",
        f"PID pan delta: {pan_delta:.3f}",
        "A/D: turn | P: PID | R: rest | Space: hold | Q: quit",
    ]
    for index, text in enumerate(lines):
        cv2.putText(
            display,
            text,
            (15, 25 + index * 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 255),
            2,
        )


def main():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.25,
        min_tracking_confidence=0.25,
    )
    controller = PIDController(
        kp=PID_KP,
        ki=PID_KI,
        kd=PID_KD,
        max_output=PID_MAX_STEP,
        deadband=PID_DEADBAND_PX,
        direction=PID_DIRECTION,
    )
    robot = create_robot()
    robot.connect(calibrate=False)

    control_mode = "hold"
    previous_action = None
    print("Robot connected. Test starts in hold mode.")
    print("Focus the camera window before using A, D, P, R, Space, or Q.")

    try:
        while True:
            observation = robot.get_observation()
            rgb_frame = observation["front"]
            frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
            display = frame.copy()

            robot_head = detect_red_head(frame, display)
            trash_positions = detect_trash(frame, display, None, None)
            desired_position = None
            trash_distance = None
            if robot_head is not None and trash_positions:
                desired_position, trash_distance = closest_trash(
                    trash_positions,
                    robot_head,
                )
                cv2.line(
                    display,
                    (int(robot_head[0]), int(robot_head[1])),
                    (int(desired_position[0]), int(desired_position[1])),
                    (0, 255, 255),
                    2,
                )
                cv2.putText(
                    display,
                    f"{trash_distance:.1f} px",
                    (
                        int((robot_head[0] + desired_position[0]) / 2),
                        int((robot_head[1] + desired_position[1]) / 2),
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2,
                )

            hand_positions = detect_human_hands(
                frame,
                display,
                hands,
                mp_drawing,
                mp_hands,
            )
            hand_distance = None
            if robot_head is not None and hand_positions:
                hand_distance = calc_hand_distance(hand_positions, robot_head)

            if robot_head is None:
                safety_mode = "stop"
            else:
                safety_mode = decide_mode(hand_distance, bool(hand_positions))

            horizontal_error = None
            pan_delta = 0.0
            if control_mode == "clockwise":
                robot_action = turn_clockwise(observation)
                control_mode = "hold"
            elif control_mode == "counterclockwise":
                robot_action = turn_counterclockwise(observation)
                control_mode = "hold"
            elif control_mode == "rest":
                robot_action = resting_position(observation)
            elif control_mode == "pid":
                robot_action, horizontal_error, pan_delta = pid_movement(
                    observation,
                    robot_head,
                    desired_position,
                    controller,
                )
            else:
                robot_action = hold_position(observation)

            draw_status(
                display,
                control_mode,
                safety_mode,
                horizontal_error,
                pan_delta,
            )
            cv2.imshow("Skills PID test", display)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), ord("Q")):
                robot.send_action(hold_position(observation))
                break
            if key in (ord("a"), ord("A")):
                control_mode = "counterclockwise"
                controller.reset()
            elif key in (ord("d"), ord("D")):
                control_mode = "clockwise"
                controller.reset()
            elif key in (ord("p"), ord("P")):
                control_mode = "pid"
                controller.reset()
            elif key in (ord("r"), ord("R")):
                control_mode = "rest"
                controller.reset()
            elif key == ord(" "):
                control_mode = "hold"
                controller.reset()

            filtered_action = filter_action(
                robot_action,
                observation,
                safety_mode,
                previous_action,
            )
            sent_action = robot.send_action(filtered_action)
            previous_action = dict(sent_action)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        hands.close()
        cv2.destroyAllWindows()
        try:
            robot.disconnect()
            print("Robot disconnected.")
        except Exception as error:
            print(f"Disconnect failed: {error}")
            print("Disconnect robot power manually.")


if __name__ == "__main__":
    main()
