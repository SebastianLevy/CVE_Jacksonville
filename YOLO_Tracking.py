import cv2
import torch
import numpy as np
from ultralytics import YOLO


model=YOLO('yolov8s.pt')


sample_vids = ['CCTV_720p.mov', 'CCTV_1080p.mov', 'peopleCount.mp4']




for vid in sample_vids:
    # Capture video
    cap = cv2.VideoCapture('SampleVideos/'+vid)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocess and model inference
        results = model(frame)

        # Filter for person class and extract midpoints
        midpoints = []
        for x1, y1, x2, y2, conf, cls in results.xyxy[0].numpy():
            if int(cls) == 0:  # Person class
                midpoint_x = (x1 + x2) / 2
                midpoint_y = y2
                midpoints.append((midpoint_x, midpoint_y))

        # Further processing with midpoints

    cap.release()
    cv2.destroyAllWindows()