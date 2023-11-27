import numpy as np
import cv2
text_color = (255, 0 , 0) #blue
font = cv2.FONT_HERSHEY_SIMPLEX 
org = (50, 50) 
fontScale = 1    
width = 300
height = 600
# def instruction_window():
#     cv2.namedWindow('Output',cv2.WINDOW_NORMAL)
#     cv2.resizeWindow('Output', width, height)
#     white_img = 255 * np.ones((height, width, 3))
#     white_img = cv2.putText(white_img, 'Welcome', org, font, fontScale, text_color, 2, cv2.LINE_AA)
#     white_img = cv2.putText(white_img, 'to', (50, 100), font, fontScale, text_color, 2, cv2.LINE_AA)
#     white_img = cv2.putText(white_img, 'SmartCrowd', (50, 150), font, fontScale, text_color, 2, cv2.LINE_AA)
#     cv2.rectangle(white_img, (50, 200), (250,300), text_color, 5)
#     def show_instructions(event, x, y, flags, params):
#         global text_color, font, org, fontScale, width, height, white_img
        
#         if event == cv2.EVENT_LBUTTONDOWN:
#             #white_img = 255 * np.ones((height, width, 3))
#             print('show instructions called, button clicked')
#             white_img = cv2.putText(white_img, 'Instructions', org, font, fontScale, text_color, 2, cv2.LINE_AA)
            
#             cv2.imshow('Output', white_img)
#     cv2.setMouseCallback("Output", show_instructions)
#     cv2.imshow('Output', white_img)
#     while True:
#         cv2.imshow('Output', white_img)
#         if cv2.waitKey(20) & 0xFF == 27:
#             break    


img = cv2.imread('cafe.jpg') #import example image
print(img.shape)
r,c,_ = img.shape
white_img = 255 * np.ones((r, c, 3))
print(white_img.shape)
#concat = np.concatenate((img, white_img), axis=1) 
concat = np.vstack((img, white_img))
print(concat.shape)
concat = img
mask = np.zeros_like(img) #black 
colors = [(0, 0, 255), (28, 172, 255), (15, 196, 241), (0, 255, 0), (255, 0, 0)]
color_i = 0
shapes = [] #list to store all drawn areas
curr_shape_index = [] #list to store the indices of the polygon currently drawing
def draw_polygon(event, x, y, flags, params):
    global shapes, curr_shape_index, colors, color_i
    color = (0, 0, 255) #red
    thickness = 5
    if event == cv2.EVENT_LBUTTONDOWN: #for all points except last, left click
        curr_shape_index.append((x, y))
        if len(curr_shape_index) > 1:
            cv2.line(img, curr_shape_index[-2], curr_shape_index[-1], color, thickness)
            cv2.line(concat, curr_shape_index[-2], curr_shape_index[-1], color, thickness)
    elif event == cv2.EVENT_RBUTTONDOWN: #middle click to denote last vertex of polygon
        curr_shape_index.append((x, y))
        cv2.line(img, curr_shape_index[-2], curr_shape_index[-1], color, thickness)
        cv2.line(img, curr_shape_index[0], curr_shape_index[-1], color, thickness)
        cv2.line(concat, curr_shape_index[-2], curr_shape_index[-1], color, thickness)
        cv2.line(concat, curr_shape_index[0], curr_shape_index[-1], color, thickness)
        #isClosed = True
        pts = np.array(curr_shape_index, np.int32)

        #cv2.polylines(img, [pts], isClosed, color, thickness) #draw polygon on img
        cv2.fillPoly(mask, [pts], colors[color_i]) #fill in where areas are
        color_i = (1 + color_i) % len(colors)
        shapes.append(curr_shape_index.copy()) #save polygon
        curr_shape_index = [] #reset current indices list
    
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_polygon)

#instruction_window()

while True:
    #cv2.imshow('Image', img)
    cv2.imshow('Image', concat)
    if cv2.waitKey(20) & 0xFF == 27: #press escape to stop selecting areas
        cv2.imwrite('output.png', img)
        cv2.imwrite('mask.png', mask)
        print(f'number of areas = {len(shapes)}')
        print(shapes) #print coordinates of areas
        break    
cv2.destroyAllWindows()
