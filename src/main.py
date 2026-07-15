import cv2 
import time 
import mediapipe as mp
from ultralytics import YOLO 
#detection 
from detection.objdetect import (closest_trash, detect_trash, aruco_position,detect_human_hands,calc_hand_distance)
#voice 
from voice.command import VoiceListener
from planner import next_action 
from skills import (decide_movement, resting_position)
from runpolicy import load_policy, run_policy_for_action
from safetysupervisor import (decide_mode, filter_action)

from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
from lerobot.cameras.opencv import OpenCVCameraConfig

#whys to improve: error handling, edge cases, add print statements, what happens when return nothing? 
#when to error/ try accept, good code writing?, what calls could fail?, try fixing that 
#do i need helper functions? what helper functions do I need? 
#imporvements: handle all trash 

#break into parts and test part by part 
#main loop 
#run perception, trash and human 
#listen for voice 
#input perception and voice into planner 
#planner outputs action word
#policy or skill chosen by planner (gotta handle chunking later, figure out when to finish)
#action ran through saftey (in seperate file?)
#add more saftey features in the future
#action happens 

#things to consider: maintaining command state for timming 

#camera set up and variables 
ROBOT_PORT = "/dev/tty.usbmodem5B415325441"
ROBOT_ID = "rory"
POLICY_DURATION_S = 30.0

def main():

    #startup code 

    model = YOLO("yolov8s.pt")
    #aruco detector 
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    aruco_params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    #hand detector 
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.25,
        min_tracking_confidence=0.25,
    )
    robot_head_position = (0, 0)
    num_trash= 0 
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

    policy, preprocessor, postprocessor, dataset_meta, policy_cfg = load_policy()
    robot.connect() 

    #voice set up 
    listener = VoiceListener()
    listener.start()

    print("set up done")

    # The previous action is the last action actually sent by LeRobot.
    # None means no action has been sent during this run yet.
    previous_action = None
    policy_end_time = None

    try: 
        #things need to be calibrated 
        #does the timing of everything work?
        while True:
            # LeRobot owns camera index 0 and returns its RGB frame in the observation.
            observation = robot.get_observation()
            rgb_frame = observation["front"]
            frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

            # Make a copy to draw on
            display = frame.copy()
            #add more to display?

            #detection 
            #gotta figure out what number the aruco number is 
            robot_head_position = aruco_position(frame, display, detector, 2)
            #need to figure out trash type 
            trash_xy = detect_trash(frame, display, model, "paper")
            trash_exists = False
            on_trash = False 
            closest_trash_distance = None
            if trash_xy: 
                trash_exists = True
                trash_cords,closest_trash_distance = closest_trash(trash_xy, robot_head_position)
                #calibrate this distance 
                if closest_trash_distance <= 10:
                    on_trash = True 
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
        
            #voice 
            #keeps old command until a new one arrives - important for later logic 
            new_command = listener.get_command()
            if new_command is not None:
                command = new_command

            #planner chooses position 
            action_name = next_action(trash_exists, command, on_trash)

            current_time = time.monotonic()
            if command in ("stop", "reset"):
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
                #how to loop through this 
                robot_action = decide_movement(robot, robot_head_position, trash_cords)
            elif action_name == "reset": 
                robot_action = resting_position(robot)
            #stop and no move both send frozen action
            else: 
                robot_action = {
                    joint: float(observation[joint])
                    for joint in robot.action_features
                }

            cv2.imshow("Main running camera", display)
            #quit 
            if cv2.waitKey(1) & 0xFF == ord("q"): 
                break 
        
            #send action to robot..
            #run through saftey 
            mode = decide_mode(closest_hand_distance, hand_exists)
            print(f"Debug: safety mode: {mode}")
            filtered_action = filter_action(robot_action, observation, mode, previous_action)

            sent_action = robot.send_action(filtered_action)
            previous_action = dict(sent_action)
    except KeyboardInterrupt: 
        #what to put here? 
        print("Exited")
    finally: 
        hands.close()
        cv2.destroyAllWindows()
        robot.disconnect() 
        listener.stop()


if __name__ == "__main__":
    main()

