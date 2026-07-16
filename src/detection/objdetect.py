
import cv2 
import math
from ultralytics import YOLO 
import mediapipe as mp
import numpy as np

#red detction values 
RED_MIN_SATURATION = 90
RED_MIN_VALUE = 70
#white detection values  
WHITE_MAX_SATURATION = 160
WHITE_MIN_VALUE = 90
MIN_WHITE_SIZE_PX = 50
MAX_WHITE_SIZE_PX = 100

# (0, 0) is the top-left corner  

#helper functions 

#return center of box, top left and bottom right corner inputted
def center_of_box(x1,y1, x2,  y2):
    return (((x1+x2)/2), ((y1+y2)/2))

def distance_between_points(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calc_hand_distance(hand_positions, head_position): 
    #could also use hand_positions.empty() 
    if hand_positions is None or [] == hand_positions: 
        #no hands detected
        closest_hand_distance = None
    else: 
        #choose closest hand
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
#depreciated function, use red color detection instead
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

#detects red head and draws it on display and returns the center of the head
def detect_red_head(frame, display): 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Red wraps around both ends of OpenCV's hue range.
    lower_red_1 = np.array([0, RED_MIN_SATURATION, RED_MIN_VALUE], dtype=np.uint8)
    upper_red_1 = np.array([12, 255, 255], dtype=np.uint8)
    lower_red_2 = np.array([168, RED_MIN_SATURATION, RED_MIN_VALUE], dtype=np.uint8)
    upper_red_2 = np.array([179, 255, 255], dtype=np.uint8)
    mask = cv2.bitwise_or(cv2.inRange(hsv, lower_red_1, upper_red_1), cv2.inRange(hsv, lower_red_2, upper_red_2),)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    red_center = None
    #can't just run max incase contours is empty 
    if contours:
        #find largest red area, so ignores smaller random red patches
        largest_red_area = max(contours, key=cv2.contourArea)
        x, y, width, height = cv2.boundingRect(largest_red_area)
        red_center = center_of_box(x, y, x + width, y + height)
        cv2.rectangle(display, (x, y), (x + width, y + height), (255, 0, 255), 2)
        cv2.putText(
                display,
                f"red marker {red_center}",
                (int(red_center[0] + 10), int(max(red_center[1] - 10, 20))),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 255),
                2,
            )
    return red_center

#return a list of trash coords and draw it on display (if list returned is empty then no trash)
#used to use yolo model to detect trash, now detects white color objects within a size range (old code commented out)
def detect_trash(frame, display): 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, WHITE_MIN_VALUE], dtype=np.uint8)
    upper_white = np.array([179, WHITE_MAX_SATURATION, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # A small closing kernel joins nearby white pixels without erasing small
    # or distant objects.
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    trash_positions = []
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        if not (MIN_WHITE_SIZE_PX <= width <= MAX_WHITE_SIZE_PX and MIN_WHITE_SIZE_PX <= height <= MAX_WHITE_SIZE_PX):
            continue
        trash_positions.append(center_of_box(x, y, x + width, y + height))
        cv2.rectangle(display, (x, y), (x + width, y + height), (0, 255, 0), 2)
        cv2.putText(display,"trash item",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,)

    return trash_positions

    #trash_positions = [] 
    #results = model(frame, conf=0.5, verbose=False)
    #for result in results: 
    #   boxes = result.boxes
    #    for box in boxes: 
           #chat given code - create boxes around items 
    #        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
    #       class_id = int(box.cls[0])
    #        confidence = float(box.conf[0])
    #        class_name = model.names[class_id]
    #       if class_name == trash_type: 
    #            obj_pos = center_of_box(x1, y1, x2, y2)
    #            trash_positions.append(obj_pos)
    #           cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #            label = f"{class_name} {confidence:.2f}"
    #            cv2.putText(display,label,(x1, y1 - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    #return trash_positions

#chat assisted function to detect hands and draw them on display and return the center of the hands
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