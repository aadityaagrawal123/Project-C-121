# import cv2 to capture videofeed
import cv2
import time
import numpy as np

# attach camera indexed as 0
camera = cv2.VideoCapture(0)

time.sleep(2)

# setting framewidth and frameheight as 640 X 480
camera.set(3 , 640)
camera.set(4 , 480)

# loading the mountain image
image = "./mount_everest.jpg"
mountain_img = cv2.imread(image)

# resizing the mountain image as 640 X 480
mountain = cv2.resize(mountain_img,(640, 480))

while True:

    # read a frame from the attached camera
    status , frame = camera.read()

    # if we got the frame successfully
    if status:
        # flip it
        frame = cv2.flip(frame , 1)

        # converting the image to RGB for easy processing
        frame_rgb = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)

        # creating thresholds       
        #Based on blue wall as the background
        lower_blue = np.array([120, 120, 120])
        upper_blue = np.array([205, 205, 250])

        # thresholding image
        mask = cv2.inRange(frame_rgb, lower_blue, upper_blue)
        # inverting the mask
        mask_bg = cv2.bitwise_not(mask)
        # bitwise and operation to extract foreground / person
        person = cv2.bitwise_and(frame, frame, mask=mask_bg)
        # final image
        final_output = cv2.addWeighted(mountain, 1, person, 1.25, 0)

        # show it
        cv2.imshow('Final Output' , final_output)

        output_file = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
        output_file.write(final_output)

        # wait of 1ms before displaying another frame
        code = cv2.waitKey(1)

        #To stop the output, click spacebar
        if code  ==  32:
            break

# release the camera and close all opened windows
camera.release()
cv2.destroyAllWindows()
