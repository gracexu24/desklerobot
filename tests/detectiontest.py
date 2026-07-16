# Tests white-object, ArUco, hand, and camera detection.
import time
from datetime import datetime
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
# from ultralytics import YOLO  # Optional custom YOLO detector.

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_FPS = 30
MAX_READ_FAILURES = 30
PHOTO_OUTPUT_DIR = Path("datasets/trash/raw")
# ARUCO_SCALE = 2.0
RED_MIN_SATURATION = 90
RED_MIN_VALUE = 70
# Deliberately permissive defaults for dim lighting and off-white objects.
WHITE_MAX_SATURATION = 160
WHITE_MIN_VALUE = 90
MIN_WHITE_SIZE_PX = 50
MAX_WHITE_SIZE_PX = 100

# Optional YOLOv8 models, kept commented out for later use.
# pretrained_model = YOLO("yolov8s.pt")
# custom_model = YOLO("runs/detect/train/weights/best.pt")
# model = pretrained_model  # Change to custom_model to use your trained weights.

#mediapipe hand detector
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.25,
    min_tracking_confidence=0.25,
)

# ArUco detector kept for later experimentation.
# aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
# aruco_params = cv2.aruco.DetectorParameters()
# aruco_params.adaptiveThreshWinSizeMin = 3
# aruco_params.adaptiveThreshWinSizeMax = 53
# aruco_params.adaptiveThreshWinSizeStep = 4
# aruco_params.minMarkerPerimeterRate = 0.01
# aruco_params.polygonalApproxAccuracyRate = 0.05
# aruco_params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
# aruco_params.errorCorrectionRate = 0.8
# aruco_params.useAruco3Detection = True
# detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)
#
# def detect_small_markers(frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     enhanced = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
#     enlarged = cv2.resize(
#         enhanced,
#         None,
#         fx=ARUCO_SCALE,
#         fy=ARUCO_SCALE,
#         interpolation=cv2.INTER_CUBIC,
#     )
#     corners, ids, _ = detector.detectMarkers(enlarged)
#     if ids is None:
#         return [], None
#     corners = [
#         np.asarray(marker_corners, dtype=np.float32) / ARUCO_SCALE
#         for marker_corners in corners
#     ]
#     return corners, ids

def detect_red_areas(frame, display):
    """Find red regions of any shape above the minimum area."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red wraps around both ends of OpenCV's hue range.
    lower_red_1 = np.array([0, RED_MIN_SATURATION, RED_MIN_VALUE], dtype=np.uint8)
    upper_red_1 = np.array([12, 255, 255], dtype=np.uint8)
    lower_red_2 = np.array([168, RED_MIN_SATURATION, RED_MIN_VALUE], dtype=np.uint8)
    upper_red_2 = np.array([179, 255, 255], dtype=np.uint8)
    mask = cv2.bitwise_or(
        cv2.inRange(hsv, lower_red_1, upper_red_1),
        cv2.inRange(hsv, lower_red_2, upper_red_2),
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    frame_area = frame.shape[0] * frame.shape[1]
    min_area = max(30.0, frame_area * 0.0001)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_areas = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue

        x, y, width, height = cv2.boundingRect(contour)
        center = (x + width // 2, y + height // 2)
        red_areas.append((center, area))
        cv2.drawContours(display, [contour], -1, (255, 0, 255), 3)
        cv2.rectangle(display, (x, y), (x + width, y + height), (255, 0, 255), 2)
        cv2.circle(display, center, 4, (255, 255, 255), -1)
        cv2.putText(
            display,
            f"red marker {center}",
            (center[0] + 10, max(center[1] - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 255),
            2,
        )

    return mask, red_areas

def detect_white_objects(frame, display):
    """Outline bright, low-saturation regions while ignoring tiny noise."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, WHITE_MIN_VALUE], dtype=np.uint8)
    upper_white = np.array([179, WHITE_MAX_SATURATION, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # A small closing kernel joins nearby white pixels without erasing small
    # or distant objects.
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    white_objects = []
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        if not (
            MIN_WHITE_SIZE_PX <= width <= MAX_WHITE_SIZE_PX
            and MIN_WHITE_SIZE_PX <= height <= MAX_WHITE_SIZE_PX
        ):
            continue

        white_objects.append((x, y, width, height))
        cv2.drawContours(display, [contour], -1, (0, 255, 0), 3)
        cv2.rectangle(display, (x, y), (x + width, y + height), (0, 255, 0), 2)
        cv2.putText(
            display,
            "white object",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

    return mask, white_objects

#helpful for testing distances between objects
def draw_marker_distances(display, red_areas, white_objects):
    """Draw pixel distances from the largest red area to each white object."""
    if not red_areas:
        return

    red_center, _ = max(red_areas, key=lambda red_area: red_area[1])
    for x, y, width, height in white_objects:
        white_center = (x + width // 2, y + height // 2)
        distance_px = float(
            np.hypot(
                white_center[0] - red_center[0],
                white_center[1] - red_center[1],
            )
        )
        midpoint = (
            (red_center[0] + white_center[0]) // 2,
            (red_center[1] + white_center[1]) // 2,
        )

        cv2.line(display, red_center, white_center, (255, 255, 0), 2)
        cv2.circle(display, white_center, 4, (255, 255, 0), -1)
        cv2.putText(
            display,
            f"{distance_px:.1f} px",
            midpoint,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2,
        )

camera_index = 0

def open_camera():
    """Open the macOS camera with stable AVFoundation settings."""
    camera = cv2.VideoCapture(camera_index, cv2.CAP_AVFOUNDATION)
    if not camera.isOpened():
        camera.release()
        camera = cv2.VideoCapture(camera_index)

    if camera.isOpened():
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        camera.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
        time.sleep(1.0)
    return camera

cap = open_camera()

if not cap.isOpened():
    raise RuntimeError(f"Could not open camera {camera_index}")

print(
    "Camera resolution:",
    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
    "x",
    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
)
print("Detecting bright, low-saturation white regions with OpenCV.")
PHOTO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
print(f"Press Space to save a raw YOLO photo to {PHOTO_OUTPUT_DIR.resolve()}")

consecutive_read_failures = 0
reconnect_attempts = 0
saved_photo_count = 0

while True:

    #code to get camera image showing and running the whole time 
    ret, frame = cap.read()
    if not ret or frame is None or frame.size == 0:
        consecutive_read_failures += 1
        if consecutive_read_failures < MAX_READ_FAILURES:
            time.sleep(0.05)
            continue

        reconnect_attempts += 1
        print(f"Camera stream lost; reconnecting ({reconnect_attempts}/3)")
        cap.release()
        if reconnect_attempts > 3:
            print("Camera unavailable. Close other camera apps and try again.")
            break
        cap = open_camera()
        consecutive_read_failures = 0
        continue

    consecutive_read_failures = 0
    # Make a copy to draw on
    display = frame.copy()

    # Optional pretrained YOLOv8 inference.
    # results = model(frame, conf=0.25, imgsz=960, verbose=False)
    # for result in results:
    #     for box in result.boxes:
    #         x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
    #         class_id = int(box.cls[0])
    #         confidence = float(box.conf[0])
    #         class_name = model.names[class_id]
    #         cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #         cv2.putText(
    #             display,
    #             f"{class_name} {confidence:.2f}",
    #             (x1, max(y1 - 10, 20)),
    #             cv2.FONT_HERSHEY_SIMPLEX,
    #             0.6,
    #             (0, 255, 0),
    #             2,
    #         )

    white_mask, white_objects = detect_white_objects(frame, display)
    cv2.putText(
        display,
        f"White objects: {len(white_objects)}",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2,
    )

    #mediapipe hands test
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_results = hands.process(rgb_frame)
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                display,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
            )

    red_mask, red_areas = detect_red_areas(frame, display)
    marker_status = f"Red areas: {len(red_areas)}"
    draw_marker_distances(display, red_areas, white_objects)

    cv2.putText(
        display,
        marker_status,
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2,
    )
    cv2.putText(
        display,
        f"Space: save photo | Saved: {saved_photo_count}",
        (20, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2,
    )

    # Optional ArUco inference, kept commented out for later use.
    # corners, ids = detect_small_markers(frame)
    # if ids is not None:
    #     cv2.aruco.drawDetectedMarkers(display, corners, ids)
   
    cv2.imshow("White objects + red marker", display)
    cv2.imshow("White detection mask", white_mask)
    cv2.imshow("Red marker mask", red_mask)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord(" "):
        #use for future custom training data creation
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        image_path = PHOTO_OUTPUT_DIR / f"trash_{timestamp}.jpg"
        # Save the untouched camera frame, without detection overlays.
        if cv2.imwrite(str(image_path), frame):
            saved_photo_count += 1
            print(f"Saved {image_path}")
        else:
            print(f"Failed to save {image_path}")

cap.release()
hands.close()
cv2.destroyAllWindows()

