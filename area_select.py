import numpy as np
import cv2

drawing = False #True if mouse is pressed
ix, iy = -1, -1 #start coordinates of rectangle
areas = [] #list of all drawn rectangles
def draw_rectangle(event, x, y, flags, params):
    global ix, iy, drawing, areas
    color = (0, 0, 255) #red
    thickness = 5
    if event == cv2.EVENT_LBUTTONDOWN: #press left mouse button down
        drawing = True
        ix, iy = x, y #save coordinates of rectangle corner
    elif event == cv2.EVENT_LBUTTONUP: #release left mouse button
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), color, thickness) #draw rectangle from 
        areas.append((ix, iy, x, y)) #add drawn area t olist

img = cv2.imread('cafe.jpg') #example img from internet
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_rectangle)

while True:
    cv2.imshow("Image", img)
    if cv2.waitKey(20) & 0xFF == 27: #press escape to stop selecting areas
        cv2.imwrite('output.png', img)
        print(f'number of areas = {len(areas)}')
        print(areas) #print coordinates of areas
        break

cv2.destroyAllWindows()