import numpy as np
import cv2

img = cv2.imread('cafe.jpg') #import example image

shapes = [] #list to store all drawn areas
curr_shape_index = [] #list to store the indices of the polygon currently drawing
def draw_polygon(event, x, y, flags, params):
    global shapes, curr_shape_index
    color = (0, 0, 255) #red
    thickness = 5
    if event == cv2.EVENT_LBUTTONDOWN: #for all points except last, left click
        curr_shape_index.append((x, y))
    elif event == cv2.EVENT_MBUTTONDOWN: #middle click to denote last vertex of polygon
        curr_shape_index.append((x, y))
        isClosed = True
        pts = np.array(curr_shape_index, np.int32)

        cv2.polylines(img, [pts], isClosed, color, thickness) #draw polygon on img
        shapes.append(curr_shape_index.copy()) #save polygon
        curr_shape_index = [] #reset current indices list
    

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_polygon)

while True:
    cv2.imshow('Image', img)
    
    if cv2.waitKey(20) & 0xFF == 27: #press escape to stop selecting areas
        cv2.imwrite('output.png', img)
        print(f'number of areas = {len(shapes)}')
        print(shapes) #print coordinates of areas
        #print(type(shapes))
        break    

cv2.destroyAllWindows()
