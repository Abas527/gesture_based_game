# # hand based
# import urllib.request
# import os

# model_url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
# model_path = "model/hand_landmarker.task"

# print("Downloading MediaPipe hand landmark model...")

# try:
#     urllib.request.urlretrieve(model_url, model_path)
#     print(f"Model downloaded successfully: {model_path}")
#     print(f"File size: {os.path.getsize(model_path) / 1024 / 1024:.2f} MB")
# except Exception as e:
#     print(f"Download failed: {e}")
#     print("\nAlternative: Download manually from:")
#     print("https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")
#     print("Save it as 'hand_landmarker.task' in the same folder as your script")

# face_model
import urllib.request
import os

# Face landmark model URL
model_url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
model_path = "model/face_landmarker.task"

os.makedirs("model", exist_ok=True)

print("Downloading MediaPipe face landmark model...")

try:
    urllib.request.urlretrieve(model_url, model_path)
    print(f"Model downloaded: {model_path}")
except Exception as e:
    print(f"Download failed: {e}")