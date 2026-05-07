import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from opencv.conn import shared
import threading
import time
import numpy as np

latest_result = None

def is_fist(hand_landmarks):
    fingers = [(8,5),(12,9),(16,13),(20,17)]
    closed = 0

    for tip, mcp in fingers:
        if hand_landmarks[tip].y > hand_landmarks[mcp].y:
            closed += 1

    thumb_tip = hand_landmarks[4]
    thumb_ip = hand_landmarks[3]
    thumb_closed = thumb_tip.x < thumb_ip.x

    return closed >= 3 and thumb_closed

def get_hand_bbox(hand_landmarks, frame_shape):
    h, w, _ = frame_shape
    xs = [int(lm.x * w) for lm in hand_landmarks]
    ys = [int(lm.y * h) for lm in hand_landmarks]
    
    min_x, max_x = max(0, min(xs) - 30), min(w, max(xs) + 30)
    min_y, max_y = max(0, min(ys) - 30), min(h, max(ys) + 30)
    
    return min_x, min_y, max_x, max_y

def apply_blur_outside_hand(frame, hand_landmarks, blur_strength=1000):
    if hand_landmarks is None:
        return cv2.GaussianBlur(frame, (blur_strength, blur_strength), 0)
    
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    
    min_x, min_y, max_x, max_y = get_hand_bbox(hand_landmarks, frame.shape)
    
    h, w = frame.shape[:2]
    points = []
    for lm in hand_landmarks:
        cx, cy = int(lm.x * w), int(lm.y * h)
        points.append([cx, cy])
    
    hull = cv2.convexHull(np.array(points))
    
    cv2.fillPoly(mask, [hull], 255)
    
    kernel = np.ones((15, 15), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    blurred = cv2.GaussianBlur(frame, (blur_strength, blur_strength), 0)
    
    mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
    result = (frame * mask_3channel + blurred * (1 - mask_3channel)).astype(np.uint8)
    
    return result

def result_callback(result, output_image, timestamp_ms):
    global latest_result
    latest_result = result

def create_conn():
    threading.Thread(target=open_webcam, daemon=True).start()

def open_webcam():
    global latest_result

    prev_x, prev_y = None, None
    last_command_time = 0

    base_options = python.BaseOptions(
        model_asset_path='model/hand_landmarker.task'
    )

    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        running_mode=vision.RunningMode.LIVE_STREAM,
        result_callback=result_callback,
        min_hand_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    )

    detector = vision.HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('assets/output.avi', fourcc, 20.0, (640, 480))

    timestamp = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        detector.detect_async(mp_image, timestamp)
        timestamp += 1

        hand_landmarks = None
        if latest_result and latest_result.hand_landmarks:
            hand = latest_result.hand_landmarks[0]
            hand_landmarks = hand

            if is_fist(hand):
                wrist = hand[0]
                x, y = wrist.x, wrist.y

                if prev_x is not None:
                    dx = x - prev_x
                    dy = y - prev_y

                    if time.time() - last_command_time > 0.15:
                        if abs(dx) > 0.01:
                            shared.set_command("LEFT" if dx < 0 else "RIGHT")
                            last_command_time = time.time()

                        if abs(dy) > 0.03:
                            shared.set_command("JUMP" if dy > 0 else "DOWN")
                            last_command_time = time.time()

                prev_x, prev_y = x, y

            frame = apply_blur_outside_hand(frame, hand_landmarks, blur_strength=55)
            
            h, w, _ = frame.shape
            for lm in hand:
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 2, (0,255,0), -1)
        else:
            frame = cv2.GaussianBlur(frame, (55, 55), 0)

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        out.write(frame)

    cap.release()
    cv2.destroyAllWindows()