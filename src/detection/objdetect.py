
import dis
from termios import TABDLY
from turtle import distance
import cv2 
import math
from ultralytics import YOLO 
import mediapipe as mp


#add human detect? 
#add hand detect? 

# (0, 0) is the top-left corner 
#make helper functions for detection values I need
#load in yolo model 

# (0, 0) is the top-left corner 

#create bounding boxes, grid/coordinate system 
#detect and return location of robot head
#detect and return number of trash items 
#return the postion of the closest piece of trash 

#camera_index = 0 

#robot_head_position = (0, 0)
#num_trash= 0 
#trash_xy = []

#cap = cv2.VideoCapture(camera_index)


#helper functions 
#return center of box, top left and bottom right corner inputted
def center_of_box(x1,y1, x2,  y2):
    return (((x1+x2)/2), ((y1+y2)/2))

def distance_between_points(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calc_hand_distance(hand_positions, head_position): 
    if hand_positions is None: 
        closest_hand_distance = None
    else: 
        closest_hand_distance = distance_between_points(head_position, hand_positions[0])
        for hand in hand_positions: 
            new_hand = distance_between_points(head_position, hand)
            if new_hand < closest_hand_distance: 
                closest_hand_distance = new_hand
    return closest_hand_distance

#location of closest trash 
def closest_trash(trash_list, head_position): 
    closest = distance_between_points(trash_list[0], head_position) 
    trash_cords = trash_list[0]
    for trash in trash_list: 
        dist = distance_between_points(trash,head_position)
        if dist < closest: 
            closest = dist 
            trash_cords = trash
    return trash_cords, closest 


#main detection funcstions 

#return position of aruco(robot head) and draw it on display
#only one aruconum to start
def aruco_position(frame, display, detector, aruco_num): 
    #make the frame grayscale 
    head_pos = (0,0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   
    corners, ids, rejected = detector.detectMarkers(gray)
    if ids is not None: 
        #detect and draw on arco
        if ids[0] == aruco_num: 
            head_pos = center_of_box(corners[0][0][0], corners[0][0][1], corners[0][2][0], corners[0][2][1])
            cv2.aruco.drawDetectedMarkers(display, corners, ids)
    return head_pos


#return a list of trash coords and draw it on display (if list returned is empty then no trash)
#trash type hardcoded for now
#model is yolo 
def detect_trash(frame, display, model, trash_type): 
    trash_positions = [] 
    results = model(frame, conf=0.5, verbose=False)
    for result in results: 
        boxes = result.boxes
        for box in boxes: 
            #chat given code - create boxes around items 
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = model.names[class_id]
            if class_name == trash_type: 
                obj_pos = center_of_box(x1, y1, x2, y2)
                trash_positions.append(obj_pos)
                cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{class_name} {confidence:.2f}"
                cv2.putText(display,label,(x1, y1 - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return trash_positions

def detect_human_hands(frame, display, hands, mp_drawing, mp_hands): 
    hand_positions = []
    frame_height, frame_width = frame.shape[:2]

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_results = hands.process(rgb_frame)

    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            x_coordinates = [
                int(landmark.x * frame_width)
                for landmark in hand_landmarks.landmark
            ]
            y_coordinates = [
                int(landmark.y * frame_height)
                for landmark in hand_landmarks.landmark
            ]

            x1, x2 = min(x_coordinates), max(x_coordinates)
            y1, y2 = min(y_coordinates), max(y_coordinates)
            hand_center = center_of_box(x1, y1, x2, y2)
            hand_positions.append(hand_center)

            cv2.rectangle(display, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.circle(
                display,
                (int(hand_center[0]), int(hand_center[1])),
                5,
                (0, 0, 255),
                -1,
            )
            mp_drawing.draw_landmarks(
                display,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
            )

    return hand_positions