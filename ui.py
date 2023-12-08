import cv2
import numpy as np
import json
import socket

#for communication between python scripts, untested
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #sets up server for clients to connect to
# server.bind(('localhost', 9999))

#red orange yellow green blue
colors = [(0, 0, 255), (28, 172, 255), (15, 196, 241), (0, 255, 0), (255, 0, 0)]
color_i = 0 #used to loop throught ^ color list

shapes = dict() #[] #dict to store all drawn areas and their color
curr_shape_index = [] #list to store the indices of the polygon currently drawing

slide = False #
# base image
cafe = cv2.imread('cafe.jpg')
height_base, width_base, channels = cafe.shape

cols = width_base
mask = np.zeros_like(cafe) #black img
# loading the sidebar image
image_path = 'first_sidebar.png'
image = cv2.imread(image_path)

# resizing the sidebar image to fit with the cafe picture
resized_image = cv2.resize(image, (400, 500))
#height_sidebar, width_sidebar, channels = resized_image.shape
blurred_image = cv2.medianBlur(resized_image, 3) 

# putting the two photos together
concat = np.concatenate((cafe, resized_image), axis=1) 
height_total, width_total, channels = concat.shape

# Define the region of interest (ROI) - the right side of concat img (where sidebar img is)
roi_x_min, roi_x_max = width_base+1, width_total
roi_y_min, roi_y_max = 0, height_total
concat_im = 'first_sidebar'
lastScreen = False #

selecting = False #true if currently selecting areas
def on_mouse_click(event, x, y, flags, param):
    global slide, concat, lastScreen, selecting, shapes, curr_shape_index, colors, color_i
    color = (0, 0, 255) #red - color of lines showing areas
    thickness = 5
    if event == cv2.EVENT_LBUTTONDOWN: 
        print(f"Left mouse button clicked at ({x}, {y})")
        #if click in sidebar region
        if roi_x_min <= x <= roi_x_max and roi_y_min <= y <= roi_y_max:
            if param == 'first_sidebar':
                slide = True
                print('first_sidebar')
                #change sidebar to instructions page
                image_path = 'instructions.png'
                image = cv2.imread(image_path)
                resized_image = cv2.resize(image, (400, 500))
                # adjust this code so that the original photo with the polygons is still there
                # or can draw polygons at the end and show that image
                concat = np.concatenate((cafe, resized_image), axis=1)
               
                #create a box to click into when done selecting
                top_left = (roi_x_min, int(3/4 * height_total))
                bottom_right = (roi_x_max, int(5/6 * height_total))
                color = (255, 255, 255) #box outline -white
                thickness = 0
                cv2.rectangle(concat, top_left, bottom_right, color, thickness)
                selecting = True #
                lastScreen = True
            elif param == 'instructions':
                #if clicking in box saying you're done selecting areas
                if roi_x_min <= x <= roi_x_max and int(3/4*height_total) <= y <= int(5/6*height_total):
                    print('analytics')
                    #change sidebar to analytics page
                    image_path = 'analytics.png'
                    image = cv2.imread(image_path)
                    resized_image = cv2.resize(image, (400, 500))
                    concat = np.concatenate((cafe, resized_image), axis=1)
                    #communicating w/ script running yolo to get updated values for regions, not tested
                    # server.listen(0)
                    # client, _ = server.accept() #this stalls the program
                    # counts = None
                    # while True:
                    #     data = client.recv(1024)
                    #     data = data.decode("utf-8")
                    #     if data.lower() == 'close':
                    #         client.send("closed".encode("utf-8"))
                    #         break
                    #     counts = data
                    # client.close()
                    #format of data that is sent: counts = '#,#,#'
                    count = '3,0,1'
                    result = counts.split(',') 
                    text1 = result[0]
                    text2 = result[1]
                    text3 = result[2]

                    font = cv2.FONT_HERSHEY_DUPLEX
                    font_size = 0.75
                    font_color = (0, 0, 0) #black
                    font_thickness = 2
                    cv2.putText(concat, text1, (width_total-100, 175), font,
                                font_size, font_color, font_thickness)
                    cv2.putText(concat, text2, (width_total-100, 300), font,
                                font_size, font_color, font_thickness)
                    cv2.putText(concat, text3, (width_total-100, 425), font,
                                font_size, font_color, font_thickness)
        
        #if drawing and clicking in image of cafe/shop                          
        if selecting and x <= cols:
            curr_shape_index.append((x, y))
            #draw a line from previous point to clicked point
            if len(curr_shape_index) > 1:
                cv2.line(cafe, curr_shape_index[-2], curr_shape_index[-1], color, thickness) #update base img
                cv2.line(concat, curr_shape_index[-2], curr_shape_index[-1], color, thickness) #update img in window
    if event == cv2.EVENT_RBUTTONDOWN and x <= cols:
        curr_shape_index.append((x, y))
        cv2.line(concat, curr_shape_index[-2], curr_shape_index[-1], color, thickness) # to update window
        cv2.line(concat, curr_shape_index[0], curr_shape_index[-1], color, thickness) #close the polygon
        cv2.line(cafe, curr_shape_index[-2], curr_shape_index[-1], color, thickness) #update base img
        cv2.line(cafe, curr_shape_index[0], curr_shape_index[-1], color, thickness)
        pts = np.array(curr_shape_index, np.int32)

        cv2.fillPoly(mask, [pts], colors[color_i]) #fill in where areas are on mask
        n = input('enter area name: ') #get user input on name of area
        shapes[n] = colors[color_i] #add it dict
        curr_shape_index = [] #reset current indices list
        color_i = (1 + color_i) % len(colors) #update color index to next color
cv2.namedWindow("SmartCrowd")
add_param = 'first_sidebar'
cv2.setMouseCallback('SmartCrowd', on_mouse_click, param=add_param)
called = False
    
# Set the callback function for mouse events
while True:
    cv2.imshow('SmartCrowd', concat)
    if slide is True and add_param == 'first_sidebar' and called is False:
        add_param = 'instructions'
        called = True
        cv2.setMouseCallback('SmartCrowd', on_mouse_click, param=add_param)
    
    if cv2.waitKey(20) & 0xFF == 27: #hit esc to exit
        cv2.imwrite('concat.png', concat)
        cv2.imwrite('mask.png', mask)
        with open('areas.json', 'w') as f:
            json.dump(shapes, f)
        break

# server.close()
cv2.destroyAllWindows()
