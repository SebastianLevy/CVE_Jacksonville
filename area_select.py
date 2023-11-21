import numpy as np
import cv2
img = cv2.imread('cafe.jpg')
drawing = True
shapes = []
curr_shape_index = []
def draw_polygon(event, x, y, flags, params):
    global drawing, shapes, curr_shape_index
    color = (0, 0, 255) #red
    thickness = 5
    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing is False: drawing = True
        curr_shape_index.append((x, y)) #assumes list is empty initially
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        drawing = False
        isClosed = True
        pts = np.array(curr_shape_index, np.int32)

        cv2.polylines(img, [pts], 
                      isClosed, color, thickness)
        shapes.append(curr_shape_index.copy())
        curr_shape_index = []

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_polygon)

while True:
    cv2.imshow('Image', img)
    
    if cv2.waitKey(20) & 0xFF == 27: #press escape to stop selecting areas
        cv2.imwrite('output.png', img)
        print(f'number of areas = {len(shapes)}')
        print(shapes) #print coordinates of areas
        break    

cv2.destroyAllWindows()
