import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from opencv.conn import shared
import threading

def create_conn():
    webcam_thread = threading.Thread(target=open_webcam, daemon=True)
    webcam_thread.start()

def open_webcam():
    previous_face_x = None
    previous_face_y = None
    face_position_x = None
    face_position_y = None
    
    base_options = python.BaseOptions(model_asset_path='model/face_landmarker.task')
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=False,
        output_facial_transformation_matrixes=False,
        num_faces=1
    )
    detector = vision.FaceLandmarker.create_from_options(options)
    
    cap = cv2.VideoCapture(0)
    print("Face Control Active - Move your head!")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        detection_result = detector.detect(mp_image)
        
        if detection_result.face_landmarks:
            face = detection_result.face_landmarks[0]
            
            nose = face[1] 
            h, w, _ = frame.shape
            face_position_x = nose.x
            face_position_y = nose.y
    
            nose_pixel = (int(nose.x * w), int(nose.y * h))
            cv2.circle(frame, nose_pixel, 8, (0, 255, 0), -1)
            
            for landmark in face:
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
            

            if previous_face_x is not None:
                delta_x = face_position_x - previous_face_x
                delta_y = face_position_y - previous_face_y
                

                if abs(delta_x) > 0.03:
                    if delta_x > 0:
                        shared.set_command("RIGHT")
                    else:
                        shared.set_command("LEFT")
                
                # Vertical movement (Up/Down)
                if abs(delta_y) > 0.03:
                    if delta_y < 0:  
                        shared.set_command("JUMP")

                    else:  
                        shared.set_command("DOWN")
            
            previous_face_x = face_position_x
            previous_face_y = face_position_y
            
        # Instructions
        cv2.putText(frame, "Move HEAD: LEFT/RIGHT = Change Lanes | UP = Jump ", 
                   (50, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow("Face Control - Move your head", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
