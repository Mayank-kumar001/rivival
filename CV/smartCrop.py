import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# setup detector
base_options = python.BaseOptions(model_asset_path="blaze_face_short_range.tflite")
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)

# video settings
FRAME_W = 1920
FRAME_H = 1080
CROP_W = 607  # 9:16 width for 1080 height

cap = cv2.VideoCapture(r"C:\Users\Aadya\Pictures\Camera Roll\WIN_20260219_20_11_48_Pro.mp4")

# setup output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("output.mp4", fourcc, 30, (CROP_W, FRAME_H))

smooth_x = FRAME_W // 2  # start from center

while True:
    ret, frame = cap.read()

    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    result = detector.detect(mp_image)

    if result.detections:
        box = result.detections[0].bounding_box
        face_center_x = box.origin_x + box.width // 2

        # smoothing - ease toward face position
        smooth_x = int(0.9 * smooth_x + 0.1 * face_center_x)

    # calculate crop boundaries
    x1 = smooth_x - CROP_W // 2
    x1 = max(0, min(x1, FRAME_W - CROP_W))  # clamp so it doesn't go out of bounds
    x2 = x1 + CROP_W

    # crop and write
    cropped = frame[0:FRAME_H, x1:x2]
    out.write(cropped)

cap.release()
out.release()
print("done! check output.mp4")