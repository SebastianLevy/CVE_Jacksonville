import numpy as np
import cv2

img = cv2.imread('cafe.jpg') #import example image
mask = np.zeros_like(img) #black
# red, orange, yellow, green, blue - can add more/adjust
colors = [(0, 0, 255), (28, 172, 255), (15, 196, 241), (0, 255, 0), (255, 0, 0)]
color_i = 0 #keep track of which color to use
shapes = [] #list to store all drawn areas
curr_shape_index = [] #list to store the indices of the polygon currently drawing
def draw_polygon(event, x, y, flags, params):
    global shapes, curr_shape_index, colors, color_i
    color = (0, 0, 255) #red
    thickness = 5
    if event == cv2.EVENT_LBUTTONDOWN: #for all points except last, left click
        curr_shape_index.append((x, y))
    elif event == cv2.EVENT_MBUTTONDOWN: #middle click to denote last vertex of polygon
        curr_shape_index.append((x, y))
        isClosed = True
        pts = np.array(curr_shape_index, np.int32)

        cv2.polylines(img, [pts], isClosed, color, thickness) #draw polygon on img
        cv2.fillPoly(mask, [pts], colors[color_i]) #fill in where areas are w/diff colors
        color_i = (1 + color_i) % len(colors) #to prevent index from going out of bounds
        shapes.append(curr_shape_index.copy()) #save polygon
        curr_shape_index = [] #reset current indices list
    
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_polygon)

while True:
    cv2.imshow('Image', img)
    
    if cv2.waitKey(20) & 0xFF == 27: #press escape to stop selecting areas
        cv2.imwrite('output.png', img)
        cv2.imwrite('mask.png', mask)
        print(f'number of areas = {len(shapes)}')
        print(shapes) #print coordinates of areas
        break    
cv2.destroyAllWindows()
