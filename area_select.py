import numpy as np
import cv2
import json

img = cv2.imread('bar.jpg')  # Import example image
mask = np.zeros_like(img)  # Black mask
# Red, orange, yellow, green, blue - can add more/adjust
colors = [(0, 0, 255), (28, 172, 255), (15, 196, 241), (0, 255, 0), (255, 0, 0)]
color_i = 0  # Keep track of which color to use
shapes = []  # List to store all drawn areas
curr_shape_index = []  # List to store the indices of the polygon currently drawing
area_names = []  # List to store names of the areas


def draw_polygon(event, x, y, flags, params):
    global shapes, curr_shape_index, colors, color_i
    color = (0, 0, 255)  # Red
    thickness = 5
    if event == cv2.EVENT_LBUTTONDOWN:  # For all points except last, left click
        curr_shape_index.append((x, y))
    elif event == cv2.EVENT_RBUTTONDOWN:  # Right click to denote last vertex of polygon
        curr_shape_index.append((x, y))
        is_closed = True
        pts = np.array(curr_shape_index, np.int32)

        cv2.polylines(img, [pts], is_closed, color, thickness)  # Draw polygon on img
        cv2.fillPoly(mask, [pts], colors[color_i])  # Fill in where areas are w/diff colors
        color_i = (1 + color_i) % len(colors)  # To prevent index from going out of bounds
        shapes.append((curr_shape_index.copy(), colors[color_i - 1]))  # Save polygon with color
        curr_shape_index = []  # Reset current indices list


cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_polygon)

while True:
    cv2.imshow('Image', img)

    if cv2.waitKey(20) & 0xFF == 27:  # Press escape to stop selecting areas
        for shape, color in shapes:
            name = input(f"Enter name for area with color {color}: ")
            area_names.append(name)
        break
cv2.destroyAllWindows()

# Constructing JSON object
areas_dict = {name: color for name, color in zip(area_names, [color for _, color in shapes])}

# Writing to a JSON file
with open('areas.json', 'w') as file:
    json.dump(areas_dict, file, indent=4)

cv2.imwrite('output.png', img)
cv2.imwrite('mask.png', mask)

print(f'Number of areas = {len(shapes)}')
print(shapes)  # Print coordinates of areas
