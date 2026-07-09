import cv2 
from ultralytics import YOLO 

# (0, 0) is the top-left corner 
#make helper functions for detection values I need
#load in yolo model 
model = YOLO("yolov8n.pt")

#aruco detector 
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)



# (0, 0) is the top-left corner 


#create bounding boxes, grid/coordinate system 
#detect and return location of robot head
#detect and return number of trash items 
#return the postion of the closest piece of trash 

camera_index = 0 

robot_head_position = (0, 0)
num_trash= 0 
trash_xy = []

cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    raise RuntimeError(f"Could not open camera {camera_index}")

while True:

    #code to get camera image showing and running the whole time 
    ret, frame = cap.read()
    if not ret: 
        print("failed to read camera")
        break 
    # Make a copy to draw on
    display = frame.copy()

    #yolo 
    #first tested to see what yolo detected, then used that for the trash
    results = model(frame, conf=0.5, verbose=False)
    for result in results: 
        boxes = result.boxes
        for box in boxes: 
            #chat given code - create boxes around items 
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = model.names[class_id]
            cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{class_name} {confidence:.2f}"
            cv2.putText(
                display,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
    #make the frame grayscale 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   
    corners, ids, rejected = aruco_detector.detectMarkers(gray)

    if ids: 
        #detect and draw on arco
        cv2.aruco.drawDetectedMarkers(display, corners, ids)
   
    cv2.imshow("yolo + camera + arUco", frame)
    #quit 
    if cv2.waitKey(1) & 0xFF == ord("q"): 
        break 

cap.release()
cv2.destroyAllWindows()

