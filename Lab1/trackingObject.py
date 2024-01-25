"""
Sourced from
Obecjt Tracking: https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
Counter Features: https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
"""
import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Our operations on the frame come here
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # define range of dark blue color in HSV
    lower_blue = np.array([100, 100, 0])   
    upper_blue = np.array([140, 255, 255]) 


    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)

    contours,hierarchy = cv.findContours(mask, 1, 2)
    contours, hierarchy = cv.findContours(mask, 1, 2)

    if contours:
        largest = max(contours, key=cv.contourArea)
        x, y, w, h = cv.boundingRect(largest)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()