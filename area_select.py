import numpy as np
import cv2
text_color = (255, 0 , 0) #blue
font = cv2.FONT_HERSHEY_SIMPLEX 
fontScale = 1   

img = cv2.imread('cafe.jpg') #import example image
cols = img.shape[1] #num cols
white_img = 255 * np.ones_like(img)
thresh = int(1.5*cols)
concat = np.concatenate((img, white_img), axis=1) 
concat = concat[:, :thresh, :]
cv2.putText(concat, 'Welcome', (cols+25, 50), font, fontScale, text_color, 2,cv2.LINE_AA)
cv2.putText(concat, 'to', (cols+25, 100), font, fontScale, text_color, 2,cv2.LINE_AA)
cv2.putText(concat, 'SmartCrowd', (cols+25, 150), font, fontScale, text_color, 2,cv2.LINE_AA)
cv2.rectangle(concat, (cols+25, 200), (cols+250, 250), text_color, 5)
cv2.putText(concat, 'Click here for gym', (cols+50, 225), font, .6, text_color, 2,cv2.LINE_AA)

mask = np.zeros_like(img) #black 
colors = [(0, 0, 255), (28, 172, 255), (15, 196, 241), (0, 255, 0), (255, 0, 0)]
color_i = 0
shapes = dict() #[] #list to store all drawn areas
curr_shape_index = [] #list to store the indices of the polygon currently drawing
def draw_polygon(event, x, y, flags, params):
    global shapes, curr_shape_index, colors, color_i
    color = (0, 0, 255) #red
    thickness = 5
    if x in range(cols+25, cols+250) and y in range(200, 250) and event == cv2.EVENT_LBUTTONDOWN:
        concat[:, cols:, :] = 255 #reset to white
        cv2.putText(concat, 'instructions', (cols+25, 50), font, fontScale, text_color, 2,cv2.LINE_AA)

    elif x <= cols and event == cv2.EVENT_LBUTTONDOWN: #for all points except last, left click
        curr_shape_index.append((x, y))
        if len(curr_shape_index) > 1:
            cv2.line(img, curr_shape_index[-2], curr_shape_index[-1], color, thickness)
            cv2.line(concat, curr_shape_index[-2], curr_shape_index[-1], color, thickness)
    elif x <= cols and event == cv2.EVENT_RBUTTONDOWN: #middle click to denote last vertex of polygon
        curr_shape_index.append((x, y))
        cv2.line(img, curr_shape_index[-2], curr_shape_index[-1], color, thickness)
        cv2.line(img, curr_shape_index[0], curr_shape_index[-1], color, thickness)
        cv2.line(concat, curr_shape_index[-2], curr_shape_index[-1], color, thickness)
        cv2.line(concat, curr_shape_index[0], curr_shape_index[-1], color, thickness)
        pts = np.array(curr_shape_index, np.int32)

        cv2.fillPoly(mask, [pts], colors[color_i]) #fill in where areas are
        color_i = (1 + color_i) % len(colors)
        n = input('enter area name: ')
        shapes[n] = (curr_shape_index.copy(), colors[color_i])
        #shapes.append(curr_shape_index.copy()) #save polygon
        curr_shape_index = [] #reset current indices list
    
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_polygon)

while True:
    cv2.imshow('Image', concat)
    if cv2.waitKey(20) & 0xFF == 27: #press escape to stop selecting areas
        cv2.imwrite('output.png', img)
        cv2.imwrite('mask.png', mask)
        print(f'number of areas = {len(shapes)}')
        print(shapes) #print coordinates of areas
        break    
cv2.destroyAllWindows()
