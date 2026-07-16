import cv2 
import time 
import mediapipe as mp
from ultralytics import YOLO 
#detection 
from detection.objdetect import (closest_trash, detect_trash, detect_red_head,detect_human_hands,calc_hand_distance)
#voice 
from voice.command import VoiceListener
from planner import next_action 
from skills import (PIDController, pid_movement, smooth_move, increment_resting_position, PIDController)
from runpolicy import load_policy, run_policy_for_action
from safetysupervisor import (decide_mode, filter_action)

from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
from lerobot.cameras.opencv import OpenCVCameraConfig

#to improve: planner state machine, edge cases, error handling, missing cases 


#camera set up and variables 
ROBOT_PORT = "/dev/tty.usbmodem5B415325441"
ROBOT_ID = "rory"

#values that can be calibrated: 

POLICY_DURATION_S = 15.0 #seconds
TRASH_DISTANCE_THRESHOLD = 100 #pixels
HAND_DISTANCE_THRESHOLD = 50 #pixels
SHOULDER_PIVOT_PX = (90, 440)
SLOW_FACTOR = 0.5 #fraction of the way to the target

# Start with proportional-only control; increase KP gradually if movement is too slow.
PID_KP = 0.4
PID_KI = 0.0
PID_KD = 0.0
PID_MAX_STEP = 10
PID_DEADBAND_DEG = 3.5
PID_DIRECTION = 1.0

REST_TARGET = {
    "shoulder_pan.pos": 10,
    "shoulder_lift.pos": -60,
    "elbow_flex.pos": 100,
    "wrist_flex.pos": 10,
    "wrist_roll.pos": 50,
    "gripper.pos": 0,
}

def main():

    #hand detector 
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.25, min_tracking_confidence=0.25,)
    robot_head_position = None
    trash_xy = []

    action_name = ""
    command = ""

    #robot set up 
    robot = SO101Follower(
        SO101FollowerConfig(
            port=ROBOT_PORT,
            id=ROBOT_ID,
            cameras={
            "front": OpenCVCameraConfig(
                index_or_path=0,
                width=640,
                height=480,
                fps=30,)
            },
        )
    )

    #pid controller set up 
    controller = PIDController(kp=PID_KP, ki=PID_KI, kd=PID_KD, max_output=PID_MAX_STEP, deadband=PID_DEADBAND_DEG, direction=PID_DIRECTION,)

    policy, preprocessor, postprocessor, dataset_meta, policy_cfg = load_policy()
    robot.connect() 

    #voice set up 
    listener = VoiceListener()
    listener.start()

    # The previous action is the last action actually sent by LeRobot.
    # None means no action has been sent during this run yet.
    previous_action = None
    policy_end_time = None

    #start robot position
    smooth_move(robot, REST_TARGET, duration_s=2.0)

    print("set up done")

    try: 

        while True:
            # LeRobot owns camera index 0 and returns its RGB frame in the observation.
            observation = robot.get_observation()
            rgb_frame = observation["front"]
            frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

            # Make a copy to draw on
            display = frame.copy()

            #detection 
            robot_head_position = detect_red_head(frame, display)
            trash_xy = detect_trash(frame, display)
            trash_exists = False
            on_trash = False 
            closest_trash_distance = None
            locked_target = None

            #trash detection used for planner input 
            if trash_xy: 
                trash_exists = True
                trash_cords,closest_trash_distance = closest_trash(trash_xy, robot_head_position)
                #calibrate this distancee 
                if closest_trash_distance <= TRASH_DISTANCE_THRESHOLD:
                    on_trash = True 
            
            #hand detection used for safety supervisor input 
            human_hands = detect_human_hands(frame, display, hands, mp_drawing, mp_hands)
            hand_exists = False
            closest_hand_distance = None
            if human_hands: 
                hand_exists = True
                closest_hand_distance = calc_hand_distance(human_hands, robot_head_position)

            print(f"Debug: head: {robot_head_position}")
            print(f"Debug: trash: {trash_xy}, closest trash distance: {closest_trash_distance}")
            print(f"Debug: hands: {human_hands}, closest hand distance: {closest_hand_distance}")
            print(f"Debug: closest hand distance: {closest_hand_distance}")

            #mode choice 
            mode = decide_mode(closest_hand_distance, hand_exists, HAND_DISTANCE_THRESHOLD)

            #voice 
            #keeps old command until a new one arrives - important for later logic 
            new_command = listener.get_command()
            if new_command is not None:
                command = new_command

            #planner chooses position 
            action_name = next_action(trash_exists, command, on_trash, mode)

            current_time = time.monotonic()
            if action_name in ("stop", "reset"):
                policy_end_time = None
            elif policy_end_time is not None:
                if current_time < policy_end_time:
                    action_name = "trash policy"
                else:
                    print("Policy duration complete")
                    policy_end_time = None
                    command = ""
                    action_name = "no move"

            print(f"Debug: next action: {action_name}")

            robot_action = {} 

            if action_name == "trash policy": 
                #unlock target
                locked_target = None
                #reset policy
                if policy_end_time is None:
                    policy.reset()
                    preprocessor.reset()
                    postprocessor.reset()
                    policy_end_time = current_time + POLICY_DURATION_S
                    print(f"Running policy for {POLICY_DURATION_S} seconds")

                robot_action = run_policy_for_action(
                    robot=robot,
                    observation=observation,
                    policy=policy,
                    preprocessor=preprocessor,
                    postprocessor=postprocessor,
                    dataset_meta=dataset_meta,
                    cfg=policy_cfg,
                )
            elif action_name == "go to trash": 
                if locked_target is None:
                    locked_target = trash_cords
                robot_action= pid_movement(observation, robot_head_position, trash_cords, controller, SHOULDER_PIVOT_PX)
            elif action_name == "reset": 
                robot_action = increment_resting_position(observation, REST_TARGET)
            #stop and no move both send frozen action
            else: 
                robot_action = {
                    joint: float(observation[joint])
                    for joint in robot.action_features
                }

            #added aditional markers to display for debugging
            if robot_head_position:
                cv2.circle(display, robot_head_position, 5, (0, 0, 255), -1)
            if trash_cords:
                cv2.circle(display, trash_cords, 5, (0, 255, 0), -1)
            if closest_hand_distance:
                cv2.circle(display, closest_hand_distance, 5, (0, 255, 0), -1)
            if closest_trash_distance:
                cv2.circle(display, closest_trash_distance, 5, (0, 255, 0), -1)

            cv2.imshow("Main running camera", display)

            #quit 
            if cv2.waitKey(1) & 0xFF == ord("q"): 
                break 
        
            #send action to robot
            #run through saftey 
            print(f"Debug: safety mode: {mode}")
            filtered_action = filter_action(robot_action, observation, mode, SLOW_FACTOR, previous_action)

            sent_action = robot.send_action(filtered_action)
            previous_action = dict(sent_action)
    except KeyboardInterrupt: 
        print("Exited")
    finally: 
        hands.close()
        cv2.destroyAllWindows()
        robot.disconnect() 
        listener.stop()


if __name__ == "__main__":
    main()

