# https://github.com/mihai-dinculescu/tapo/blob/main/tapo/examples/tapo_camera.rs
# snapshot with high resolution 
from datetime import datetime
import os
import cv2

CAMERA_IP = os.getenv("IP_ADDRESS", "192.168.1.100")
CAMERA_USER = os.getenv("TAPO_CAMERA_USERNAME", "your_camera_user")
CAMERA_PASS = os.getenv("TAPO_CAMERA_PASSWORD", "your_camera_password")

RTSP_URL = f"rtsp://{CAMERA_USER}:{CAMERA_PASS}@{CAMERA_IP}:554/stream1"

# Must be set BEFORE importing cv2 in some builds, or right before VideoCapture
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"


def capture_screenshot(output_path: str) -> None:
  cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
  if not cap.isOpened():
    raise RuntimeError(
        f"Failed to connect to {CAMERA_IP}:554. Check IP, port, and Camera"
        " Account credentials."
    )

  try:
    frame = None
    for _ in range(5):
      ret, frame = cap.read()
      if not ret:
        raise RuntimeError(
            "Connected, but failed to read frame from RTSP stream."
        )

    cv2.imwrite(output_path, frame)
    print(f"Screenshot saved to {output_path}")
  finally:
    cap.release()


if __name__ == "__main__":
  capture_screenshot(f"c210_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")