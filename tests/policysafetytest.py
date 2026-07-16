"""Run the ACT policy through hand-distance safety supervision.

Controls:
    S: start/restart the policy
    Space: pause policy motion
    Q: quit

Distance is measured in camera pixels from the largest red circular marker to
the closest detected hand. Motion is stopped whenever the red marker is lost.
"""

import sys
import time
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from runpolicy import load_policy, run_policy_for_action
from safetysupervisor import decide_mode, filter_action

ROBOT_PORT = "/dev/tty.usbmodem5B415325441"
ROBOT_ID = "rory"
POLICY_DURATION_S = 30.0
FPS = 30.0
RED_MIN_SATURATION = 90
RED_MIN_VALUE = 70
SPEED_MULTIPLIERS = {"stop": 0.0, "slow": 0.5, "normal": 1.0}


def create_robot():
    from lerobot.cameras.opencv import OpenCVCameraConfig
    from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig

    return SO101Follower(
        SO101FollowerConfig(
            port=ROBOT_PORT,
            id=ROBOT_ID,
            max_relative_target=15.0,
            cameras={
                "front": OpenCVCameraConfig(
                    index_or_path=0,
                    width=640,
                    height=480,
                    fps=30,
                )
            },
        )
    )


def detect_red_marker(frame, display):
    """Return the center of the largest approximately circular red region."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.bitwise_or(
        cv2.inRange(
            hsv,
            np.array([0, RED_MIN_SATURATION, RED_MIN_VALUE], dtype=np.uint8),
            np.array([12, 255, 255], dtype=np.uint8),
        ),
        cv2.inRange(
            hsv,
            np.array([168, RED_MIN_SATURATION, RED_MIN_VALUE], dtype=np.uint8),
            np.array([179, 255, 255], dtype=np.uint8),
        ),
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    frame_area = frame.shape[0] * frame.shape[1]
    candidates = []
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if area < max(30.0, frame_area * 0.0001) or perimeter == 0:
            continue

        circularity = 4.0 * np.pi * area / (perimeter * perimeter)
        x, y, width, height = cv2.boundingRect(contour)
        if circularity < 0.55 or not 0.65 <= width / float(height) <= 1.35:
            continue

        (center_x, center_y), radius = cv2.minEnclosingCircle(contour)
        candidates.append(((int(center_x), int(center_y)), int(radius)))

    if not candidates:
        return None, mask

    center, radius = max(candidates, key=lambda candidate: candidate[1])
    cv2.circle(display, center, radius, (255, 0, 255), 3)
    cv2.circle(display, center, 4, (255, 255, 255), -1)
    return center, mask


def detect_hands(rgb_frame, display, hands, mp_drawing, mp_hands):
    """Return hand bounding-box centers and draw MediaPipe landmarks."""
    frame_height, frame_width = rgb_frame.shape[:2]
    hand_centers = []
    results = hands.process(rgb_frame)
    if not results.multi_hand_landmarks:
        return hand_centers

    for landmarks in results.multi_hand_landmarks:
        xs = [int(point.x * frame_width) for point in landmarks.landmark]
        ys = [int(point.y * frame_height) for point in landmarks.landmark]
        x1, x2 = min(xs), max(xs)
        y1, y2 = min(ys), max(ys)
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        hand_centers.append(center)
        cv2.rectangle(display, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.circle(display, center, 4, (0, 0, 255), -1)
        mp_drawing.draw_landmarks(
            display,
            landmarks,
            mp_hands.HAND_CONNECTIONS,
        )
    return hand_centers


def closest_hand_distance(marker_center, hand_centers, display):
    if marker_center is None or not hand_centers:
        return None

    closest_center = min(
        hand_centers,
        key=lambda center: np.hypot(
            center[0] - marker_center[0],
            center[1] - marker_center[1],
        ),
    )
    distance = float(
        np.hypot(
            closest_center[0] - marker_center[0],
            closest_center[1] - marker_center[1],
        )
    )
    midpoint = (
        (marker_center[0] + closest_center[0]) // 2,
        (marker_center[1] + closest_center[1]) // 2,
    )
    cv2.line(display, marker_center, closest_center, (0, 255, 255), 2)
    cv2.putText(
        display,
        f"{distance:.1f} px",
        midpoint,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2,
    )
    return distance


def draw_status(display, active, marker_center, distance, mode, speed):
    distance_text = "n/a" if distance is None else f"{distance:.1f} px"
    lines = [
        f"Policy: {'RUNNING' if active else 'PAUSED'}",
        f"Red marker: {'found' if marker_center is not None else 'MISSING'}",
        f"Hand distance: {distance_text}",
        f"Safety: {mode} | speed: {speed:.1f}x",
        "S: start | Space: pause | Q: quit",
    ]
    for index, text in enumerate(lines):
        cv2.putText(
            display,
            text,
            (20, 30 + index * 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )


def hold_current_position(robot, observation):
    hold_action = {
        joint: float(observation[joint])
        for joint in robot.action_features
    }
    return dict(robot.send_action(hold_action))


def main():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.25,
        min_tracking_confidence=0.25,
    )

    robot = create_robot()
    policy, preprocessor, postprocessor, dataset_meta, policy_cfg = load_policy()
    robot.connect(calibrate=False)

    active = False
    policy_end_time = None
    previous_action = None
    last_print_time = 0.0
    dt = 1.0 / FPS
    print("Robot connected. Policy is PAUSED.")
    print("Camera window: S=start, Space=pause, Q=quit")

    try:
        while True:
            loop_start = time.monotonic()
            observation = robot.get_observation()
            rgb_frame = observation["front"]
            frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
            display = frame.copy()

            marker_center, red_mask = detect_red_marker(frame, display)
            hand_centers = detect_hands(
                rgb_frame,
                display,
                hands,
                mp_drawing,
                mp_hands,
            )
            distance = closest_hand_distance(marker_center, hand_centers, display)

            # Missing marker means distance cannot be trusted, so fail closed.
            if marker_center is None:
                mode = "stop"
            else:
                mode = decide_mode(distance, bool(hand_centers))
            speed = SPEED_MULTIPLIERS[mode]

            if policy_end_time is not None and time.monotonic() >= policy_end_time:
                active = False
                policy_end_time = None
                previous_action = hold_current_position(robot, observation)
                print("Policy duration complete; motion paused.")

            draw_status(display, active, marker_center, distance, mode, speed)
            cv2.imshow("Policy safety test", display)
            cv2.imshow("Red marker mask", red_mask)
            key = cv2.waitKey(1) & 0xFF

            command = None
            if key in (ord("s"), ord("S")):
                command = "s"
            elif key == ord(" "):
                command = "p"
            elif key in (ord("q"), ord("Q")):
                command = "q"

            if command == "q":
                previous_action = hold_current_position(robot, observation)
                break
            if command in ("p", "pause"):
                active = False
                policy_end_time = None
                previous_action = hold_current_position(robot, observation)
                print("Policy paused.")
            elif command in ("s", "start"):
                policy.reset()
                preprocessor.reset()
                postprocessor.reset()
                previous_action = None
                active = True
                policy_end_time = time.monotonic() + POLICY_DURATION_S
                print(f"Policy started for at most {POLICY_DURATION_S:.0f} seconds.")

            if active:
                raw_action = run_policy_for_action(
                    robot=robot,
                    observation=observation,
                    policy=policy,
                    preprocessor=preprocessor,
                    postprocessor=postprocessor,
                    dataset_meta=dataset_meta,
                    cfg=policy_cfg,
                )
                safe_action = filter_action(
                    raw_action,
                    observation,
                    mode,
                    previous_action,
                )
                sent_action = robot.send_action(safe_action)
                previous_action = dict(sent_action)

            now = time.monotonic()
            if now - last_print_time >= 0.5:
                print(
                    f"safety={mode}, speed={speed:.1f}x, "
                    f"hand_distance={distance if distance is not None else 'n/a'}"
                )
                last_print_time = now

            elapsed = time.monotonic() - loop_start
            time.sleep(max(0.0, dt - elapsed))
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
