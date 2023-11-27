import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO


model=YOLO('yolov8s.pt')

sample_vids = ['CCTV_720p.mov', 'CCTV_1080p.mov', 'peopleCount.mp4']

vid = 'SampleVideos/' + sample_vids[1]

area1=[(312,388),(289,390),(474,469),(497,462)]

area2=[(279,392),(250,397),(423,477),(454,469)]
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap=cv2.VideoCapture(vid)


my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n") 
#print(class_list)

trackers = []
count=0

while True:    
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 2 != 0:
        continue
    frame = cv2.resize(frame, (1020, 500))

    results = model.predict(frame)

    # Accessing the boxes, confidences, and class IDs
    boxes = results[0].boxes.xyxy
    confidences = results[0].boxes.conf
    class_ids = results[0].boxes.cls

    # Iterating through detections
    for i in range(len(boxes)):
        box = boxes[i]
        confidence = confidences[i]
        class_id = class_ids[i]

        # Convert class_id to a Python integer
        class_id = int(class_id)  # or class_id.item() if class_id is a single-element tensor

        x1, y1, x2, y2 = map(int, box[:4])
        xc = int((x1 + x2) / 2)
        yc = y2

        c = class_list[class_id]

        if 'person' in c:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, str(c), (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv2.circle(frame, (x1, y1), 5, (0, 0, 255), -1)  # Top-left in red
            cv2.circle(frame, (x2, y1), 5, (0, 255, 0), -1)  # Top-right in green
            cv2.circle(frame, (x1, y2), 5, (255, 0, 0), -1)  # Bottom-left in blue
            cv2.circle(frame, (x2, y2), 5, (255, 255, 0), -1)  # Bottom-right in cyan
            cv2.circle(frame, (xc, yc), 5, (255, 0, 255), -1)  # Bottom-Midpoint in pink
            
            
        
    cv2.polylines(frame,[np.array(area1,np.int32)],True,(255,0,0),2)
    cv2.putText(frame,str('1'),(504,471),cv2.FONT_HERSHEY_COMPLEX,(0.5),(0,0,0),1)

    cv2.polylines(frame,[np.array(area2,np.int32)],True,(255,0,0),2)
    cv2.putText(frame,str('2'),(466,485),cv2.FONT_HERSHEY_COMPLEX,(0.5),(0,0,0),1)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1)&0xFF==27:
        break

cap.release()
cv2.destroyAllWindows()

