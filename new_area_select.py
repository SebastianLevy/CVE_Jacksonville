import cv2
import json
import numpy as np

# Define the video file path
video_path = r'C:\Users\prati\Desktop\College\Fall 2023\CV (24678)\Project\CVE_Jacksonville\CCTV_720p.mov'

# Create a video capture object
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Read the first frame from the video
ret, img = cap.read()
if not ret:
    print("Error: Could not read the first frame.")
    exit()

# Create a mask for drawing areas
mask = np.zeros_like(img)

# Create an empty list to store drawn areas
shapes = []

# Callback function for drawing polygons
def draw_polygon(event, x, y, flags, param):
    global shapes, colors, color_i, mask, curr_shape_index
    color = (0, 0, 255)  # red
    thickness = 5

    if event == cv2.EVENT_LBUTTONDOWN:  # For all points except the last, left click
        curr_shape_index.append((x, y))
    elif event == cv2.EVENT_MBUTTONDOWN:  # Middle click to denote the last vertex of the polygon
        curr_shape_index.append((x, y))
        is_closed = True
        pts = np.array(curr_shape_index, np.int32)

        cv2.polylines(overlay_img, [pts], is_closed, color, thickness)  # Draw polygon on overlay_img
        cv2.fillPoly(mask, [pts], colors[color_i])  # Fill in where areas are with different colors
        color_i = (1 + color_i) % len(colors)  # Prevent the index from going out of bounds
        shapes.append(curr_shape_index.copy())  # Save polygon
        curr_shape_index = []  # Reset the current indices list

# Define colors for drawing areas
colors = [(0, 0, 255), (28, 172, 255), (15, 196, 241), (0, 255, 0), (255, 0, 0)]
color_i = 0  # Keep track of which color to use
curr_shape_index = []  # List to store the indices of the polygon currently drawing

# Set up the window and callback function
cv2.namedWindow("Video")
cv2.setMouseCallback("Video", draw_polygon)

# Create a copy of the first frame for display
display_img = img.copy()

# Create a copy of the first frame for accumulating drawn rectangles
overlay_img = img.copy()

# Main loop for video processing
while True:
    # Read the next frame from the video
    ret, img = cap.read()
    if not ret:
        print("End of video.")
        break

    # Overlay the drawn rectangles onto the current frame
    display_img = cv2.addWeighted(img, 1, overlay_img, 1, 0)

    # Show the current frame with the drawn rectangles
    cv2.imshow("Video", display_img)

    # Break the loop if the 'Esc' key is pressed
    if cv2.waitKey(20) & 0xFF == 27:
        break

# Save the drawn areas to a file (e.g., areas.json)
with open('areas.json', 'w') as f:
    json.dump(shapes, f)

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
