import cv2
import numpy as np
#global add_param, slide

slide = False
# base image
cafe = cv2.imread('cafe.jpg')
height_base, width_base, channels = cafe.shape

# loading the sidebar image
image_path = 'first_sidebar.png'
image = cv2.imread(image_path)

# resizing the image to fit with the cafe picture
resized_image = cv2.resize(image, (400, 500))
#height_sidebar, width_sidebar, channels = resized_image.shape
blurred_image = cv2.medianBlur(resized_image, 3) 

# putting the two photos together
concat = np.concatenate((cafe, resized_image), axis=1) 
height_total, width_total, channels = concat.shape

# Define the region of interest (ROI)
roi_x_min, roi_x_max = width_base+1, width_total
roi_y_min, roi_y_max = 0, height_total
concat_im = 'first_sidebar'
lastScreen = False
print(roi_x_min)
print(roi_x_max)

def on_mouse_click(event, x, y, flags, param):
    global slide, concat, lastScreen
    if event == cv2.EVENT_LBUTTONDOWN: 
        print(f"Left mouse button clicked at ({x}, {y})")
        
        if roi_x_min <= x <= roi_x_max and roi_y_min <= y <= roi_y_max:
            if param == 'first_sidebar':
                slide = True
                print('first_sidebar')
                image_path = 'instructions.png'
                image = cv2.imread(image_path)
                resized_image = cv2.resize(image, (400, 500))

                # adjust this code so that the original photo with the polygons is still there
                # or can draw polygons at the end and show that image
                concat = np.concatenate((cafe, resized_image), axis=1)
              
            elif param == 'instructions':
                if lastScreen is False:
                    print('instruction')
                    top_left = (roi_x_min, int(2/3 * height_total))
                    bottom_right = (roi_x_max, int(4/5 * height_total))
                    color = (0, 255, 0)
                    thickness = 2
                    cv2.rectangle(concat, top_left, bottom_right, color, thickness)
                    lastScreen = True
                elif lastScreen and roi_x_min <= x <= roi_x_max and int(2/3*height_total) <= y <= int(4/5*height_total):
                    print('analytics')
                    image_path = 'analytics.png'
                    image = cv2.imread(image_path)
                    resized_image = cv2.resize(image, (400, 500))
                    concat = np.concatenate((cafe, resized_image), axis=1)
                                  

cv2.namedWindow("SmartCrowd")
add_param = 'first_sidebar'
cv2.setMouseCallback('SmartCrowd', on_mouse_click, param=add_param)
called = False
    
# Set the callback function for mouse events
while True:
    cv2.imshow('SmartCrowd', concat)
    #print(slide, add_param, called)
    if slide is True and add_param == 'first_sidebar' and called is False:
        add_param = 'instructions'
        called = True
        cv2.setMouseCallback('SmartCrowd', on_mouse_click, param=add_param)
    
    if cv2.waitKey(20) & 0xFF == 27:
        break
# logic for clicking in the click to proceed
#if concat_im == 'first_sidebar' and 

cv2.destroyAllWindows()
