# CVE_Jacksonville


1) **Area Segmentation:** The area segmentation portion of the code asks for user input in selecting the desired areas in an image and outputs a mask. For each area, the user clicks where they want each corner of the area to be, right clicking for the final point, and the code adds the area onto the image in red lines as the user clicks. When the user is done, the code asks for the name of the area, and saves the area onto a mask, which is all black, except for the pixels within the area, which are assigned a color from a list. The code saves the mask and a json file with a dictionary that contains key value pairs of the area name and its assigned color. This information is used in the real time analysis of video. This code is integrated with the ui in ui.py



2) Status Detection - Sebastian



3) YOLO - Sebastian


4) **Live Occupancy:** The Live Occupancy portion of the provided code focuses on real-time object detection using the YOLO (You Only Look Once) model. Utilizing the 'yolov8s.pt' file, the YOLO model processes frames captured from a video source, identifying individuals classified as "person" within the scene. The code visualizes these detections by drawing bounding boxes around detected people, labeling them as "person," and marking the key bottom-midpoint with circle. Additionally, the code defines and displays different areas that are drawn by the user using polygons and labels. The user is provided with a real-time view of detected individuals and their spatial distribution within the specified regions. The program allows for easy observation of live occupancy dynamics and is terminated upon user input (pressing the 'Esc' key), ensuring an interactive and informative experience.


5) **UI:** The purpose of creating code for a user interface (UI) to demonstrate a proof of concept is to visually articulate the intended design and functionality of a software application. By implementing UI code, we can show a clear proof of concept. This proof of concept helps validate the feasibility and potential success of the proposed product. Running this part of the code requires instructions.png, analytics.png, first_sidebar.png, and first_frame.png to be in the same folder. The workflow of the code is as follows: the user will click anywhere on instructions.png to continue, select their areas on the left side (where their area is), double click in the area that prompts the user to advance, and then watch the live analytics on the last slide.
