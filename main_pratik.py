import cv2
import json
import time
from datetime import datetime, timedelta
from ultralytics import YOLO

# Path to your JSON file
json_file_path = 'areas.json'

# Open and read the JSON file
with open(json_file_path, 'r') as file:
    areas = json.load(file)
    areas = {tuple(value): key for key, value in areas.items()}

# Load YOLO model
model = YOLO('yolov8s.pt')

sample_vids = ['CCTV_720p.mov', 'CCTV_1080p.mov', 'peopleCount.mp4', 'scaife.mov']

vid = 'SampleVideos/' + sample_vids[3]

cap = cv2.VideoCapture(vid)

# def RGB(event, x, y, flags, param):
#     if event == cv2.EVENT_MOUSEMOVE:
#         colorsBGR = [x, y]
#         print(colorsBGR)

# cv2.namedWindow('RGB')
# cv2.setMouseCallback('RGB', RGB)

with open("coco.txt", "r") as my_file:
    data = my_file.read()

class_list = data.split("\n")

trackers = []
count = 0

# Dictionary to store entry and exit times of each person in each area
entry_exit_times = {area: [] for area in areas.values()}

while True:
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 2 != 0:
        continue
    frame = cv2.resize(frame, (1020, 500))
    mask = cv2.imread('mask.png')
    mask = cv2.resize(mask, (1020, 500))

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
        if xc < 1020 and yc < 500:
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

                # Record entry time if not already recorded
                if xc < 1020 and yc < 500 and (xc, yc, 'entry') not in entry_exit_times[area_name]:
                    entry_exit_times[area_name].append((xc, yc, 'entry', time.time()))

    # Check if any person left an area
    for area_name, times in entry_exit_times.items():
        for entry_exit in times:
            xc, yc, status, timestamp = entry_exit
            if status == 'entry' and (xc, yc, 'exit') not in entry_exit_times[area_name]:
                if xc < 1020 and yc < 500:
                    cv2.circle(frame, (xc, yc), 5, (0, 0, 255), -1)
                entry_exit_times[area_name].append((xc, yc, 'exit', time.time()))

    # Print the number of people in each area
    for area, count in people_count.items():
        if count == 1:
            print(f"{area}: {count} person")
        else:
            print(f"{area}: {count} people")

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Calculate and print average waiting time for each area
for area_name, times in entry_exit_times.items():
    entry_times = [time_entry for time_entry in times if time_entry[2] == 'entry']
    exit_times = [time_exit for time_exit in times if time_exit[2] == 'exit']

    # Match entry and exit times
    matched_times = []
    for entry_time in entry_times:
        xc, yc, _, entry_timestamp = entry_time
        closest_exit_time = min(exit_times, key=lambda x: abs(x[0] - xc) + abs(x[1] - yc))
        exit_timestamp = closest_exit_time[3]
        matched_times.append((entry_timestamp, exit_timestamp))

    # Working Version
    # # Calculate waiting times
    # waiting_times = [timedelta(seconds=(exit_time - entry_time)) for entry_time, exit_time in matched_times]
    # waiting_times_seconds = [time.total_seconds() for time in waiting_times]

    # # Convert average waiting time from timedelta to seconds
    # average_waiting_time_seconds = sum(waiting_times_seconds) / len(waiting_times_seconds)

    # # Convert average waiting time back to timedelta
    # average_waiting_time = timedelta(seconds=average_waiting_time_seconds)

    # average_minutes, average_seconds = divmod(average_waiting_time.seconds, 60)
    # print(f"Average time spent in {area_name}: {average_waiting_time.days} days, {average_waiting_time.seconds} seconds ({average_minutes} mins and {average_seconds} seconds)")


    # Calculate waiting times
    # waiting_times = [(exit_time - entry_time) for entry_time, exit_time in matched_times]
    waiting_times = [timedelta(seconds=(exit_time - entry_time)) for entry_time, exit_time in matched_times]
    # Check if waiting_times is not empty
    if waiting_times:
        waiting_times_seconds = [time.total_seconds() for time in waiting_times]

        # Check if waiting_times_seconds is not empty
        if waiting_times_seconds:
            # Calculate and print average waiting time for each area
            average_waiting_time_seconds = sum(waiting_times_seconds) / len(waiting_times_seconds)

            # Convert average waiting time from timedelta to seconds
            average_waiting_time = timedelta(seconds=average_waiting_time_seconds)

            # Get average waiting time in minutes and seconds
            average_minutes, average_seconds = divmod(average_waiting_time_seconds, 60)

            # Print average waiting time in the desired format
            print(f"Average time spent in {area_name}: {average_waiting_time.days} days, {average_waiting_time_seconds} seconds "
                f"({average_minutes} mins and {average_seconds} seconds)")
        else:
            print(f"No waiting times recorded for {area_name}")
    else:
        print(f"No waiting times recorded for {area_name}")



cv2.waitKey(0)
