import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import json

# Path to your JSON file
json_file_path = 'areas.json'

# Open and read the JSON file
with open(json_file_path, 'r') as file:
    areas = json.load(file)
    areas = {tuple(value): key for key, value in areas.items()}

model = YOLO('yolov8s.pt')

cv2.namedWindow('RGB')

with open("coco.txt", "r") as my_file:
    data = my_file.read()
class_list = data.split("\n") 



#YOLO VIDEO FOR LOOP STARTS
frame = cv2.resize(cv2.imread('bar.jpg'), (1020, 500))
mask = cv2.imread('mask.png')

results = model.predict(frame)

# Accessing the boxes, confidences, and class IDs
boxes = results[0].boxes.xyxy
confidences = results[0].boxes.conf
class_ids = results[0].boxes.cls
converted_boxes = []
for box in boxes:
    x1, y1, x2, y2 = map(int, box[:4])
    width, height = x2 - x1, y2 - y1
    x, y = x1, y1  # Top-left corner
    converted_boxes.append([x, y, width, height])

confidence_list = [float(conf) for conf in confidences]

indices = cv2.dnn.NMSBoxes(converted_boxes, confidence_list, 0.5, 0.4)

# Initialize the counter dictionary
people_count = {area: 0 for area in areas.values()}

# Iterating through detections
for i in indices:
    box = boxes[i]
    confidence = confidences[i]
    class_id = class_ids[i]

    class_id = int(class_id)

    x1, y1, x2, y2 = map(int, box[:4])
    xc = int((x1 + x2) / 2)
    yc = y2

    c = class_list[class_id]
    colour = tuple(int(val) for val in mask[yc, xc])

    if 'person' in c:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, str(c), (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.circle(frame, (xc, yc), 5, colour, -1)

        area_col = mask[yc, xc]
        area_col_tuple = tuple(area_col)

        # Find the area name by color and update the count
        area_name = areas.get(area_col_tuple, "no color")
        if area_name != "no color":
            people_count[area_name] += 1

# Print the number of people in each area
for area, count in people_count.items():
    if count == 1: 
        print(f"{area}: {count} person")
    else:
        print(f"{area}: {count} people")

cv2.imshow("RGB", frame)

#YOLO VIDEO FOR LOOP ENDS


cv2.waitKey(0)
