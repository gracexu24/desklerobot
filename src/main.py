
import cv2 
import json 
import time 
from pathlib import Path 
import torch 
from ultralytics import YOLO 
#detection 
from detection.objdetect import (closest_trash, detect_trash, aruco_position,detect_human_hands,calc_hand_distance)
#voice 
from voice.command import VoiceListener
from planner import next_action 
from skills import (decide_movement, resting_position)
from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
from lerobot.cameras.opencv import OpenCVCameraConfig

#for running policy
from lerobot.datasets.utils import build_dataset_frame
from lerobot.policies.utils import make_robot_action
from lerobot.utils.constants import OBS_STR
from lerobot.utils.control_utils import predict_action

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

#camera set up and variables 
ROBOT_PORT = "/dev/tty.usbmodem5B415325441"
ROBOT_ID = "rory"
camera_index = 0 

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
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera {camera_index}")

    next_action = ""
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
    robot.connect() 

    #voice set up 
    listener = VoiceListener()
    listener.start()

    print("set up done")

    #save previous action 
    try: 
        #things need to be calibrated 
        #does the timing of everything work?
        while True:
            #code to get camera image showing and running the whole time 
            ret, frame = cap.read()
            if not ret: 
                print("failed to read camera")
                break 
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
            if trash_xy: 
                trash_exists = True
                closest_trash_distance = closest_trash(trash_xy, robot_head_position)
                #calibrate this distance 
                if closest_trash_distance <= 10:
                    on_trash = True 
            human_hands = detect_human_hands(frame, display, hands, mp_drawing, mp_hands)
            hand_exists = False
            if human_hands: 
                trash_exists = True
                closest_hand_distance = calc_hand_distance(human_hands, robot_head_position)
            print(f"Debug: head: {robot_head_position}")
            print(f"Debug: trash: {trash_xy}, closest trash distance: {closest_trash_distance}")
            print(f"Debug: hands: {human_hands}, closest hand distance: {closest_hand_distance}")
            print(f"Debug: closest hand distance: {closest_hand_distance}")
        
            #voice 
            command = listener.get_command() 

            #planner chooses position 
            next_action = next_action(trash_exists, command, on_trash)
            print(f"Debug: next action: {next_action}")

            robot_action = {} 

            if next_action == "trash policy": 
            elif next_action == "go to trash": 
                #how to loop through this 
                robot_action = decide_movement(robot_head_position, closest_trash_distance)
            elif next_action == "reset": 
            #stop and no move both send frozen action
            else: 

            cv2.imshow("Main running camera", display)
            #quit 
            if cv2.waitKey(1) & 0xFF == ord("q"): 
                break 
            #send action to robot..
    except KeyboardInterrupt: 
        #what to put here? 
        print("Exited")
    finally: 
        cap.release()
        cv2.destroyAllWindows()
        robot.disconnect() 
        #close mediapipe?


if __name__ == "__main__":
    main()

