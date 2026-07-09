from planner import next_action
import cv2 
from ultralytics import YOLO 
from detection.trashdetect import (closest_trash, detect_trash, aruco_position )
from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
#set up steps needed

#whys to improve: error handling, edge cases
#how to interact w robot? 
#when to error/ try accept, good code writing? 
#do i need helper functions? what helper functions do I need? 

#break into parts and test part by part 
#main loop 
#run perception, trash and human 
#listen for voice 
#input perception and voice into planner 
#planner outputs action word
#policy or skill chosen by planner 
#action ran through saftey 
#action happens 

#camera set up and variables 
model = YOLO("yolov8n.pt")

#aruco detector 
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

camera_index = 0 
robot_head_position = (0, 0)
num_trash= 0 
trash_xy = []
cap = cv2.VideoCapture(camera_index)
if not cap.isOpened():
    raise RuntimeError(f"Could not open camera {camera_index}")

next_action = "start"

#change later once adding voice
command = "trash"


robot = SO101Follower(
    SO101FollowerConfig(
        port="/dev/tty.usbmodem5B415325441",
        id="rory",
    )
)

def main():
    robot.connect() 

    #need to run loop for camera detection
    #save previous action 
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
        corners, ids, rejected = detector.detectMarkers(gray)

        if ids: 
            #detect and draw on arco
            cv2.aruco.drawDetectedMarkers(display, corners, ids)
    
        cv2.imshow("yolo + camera + arUco", frame)
        #quit 
        if cv2.waitKey(1) & 0xFF == ord("q"): 
            break 


        #send action to robot..

    cap.release()
    cv2.destroyAllWindows()


    #project_root = find_project_root()
    #print(f"Project root: {project_root}")

    #robot = None

    #chat given try and clean up code, fix to match how to intereact w interface 
    try:
        print("Loading robot...")
        robot = load_robot()

        print("Connecting robot...")
        robot.connect()
        print("Robot connected.")

        print("Loading policy...")
        policy = load_policy()
        print("Policy loaded.")

        run_policy_loop(
            robot=robot,
            policy=policy,
            num_steps=NUM_STEPS,
            control_dt=CONTROL_DT,
        )

    except KeyboardInterrupt:
        print("Stopped by user with Ctrl+C.")

    except Exception as error:
        print(f"Error: {error}")

    finally:
        print("Cleaning up...")

        if robot is not None:
            try:
                # Some LeRobot versions have disconnect().
                robot.disconnect()
                print("Robot disconnected.")
            except AttributeError:
                print("robot.disconnect() not available in this LeRobot version.")
            except Exception as error:
                print(f"Error while disconnecting robot: {error}")

        print("Done.")


if __name__ == "__main__":
    main()

