"""
Sourced from
Capture Video from Camera: https://docs.opencv.org/3.4/dd/d43/tutorial_py_video_display.html
Finding Dominant Colour: https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
Bounding Rectangle: https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
"""
import cv2
import numpy as np
from sklearn.cluster import KMeans

def find_dominant_color(image, k=1):

    pixels = image.reshape((image.shape[0] * image.shape[1], 3))

    # Use KMeans to find the dominant color
    clt = KMeans(n_clusters=k)
    clt.fit(pixels)

    dominant_color = clt.cluster_centers_[0].astype(int)

    return dominant_color

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    height, width = frame.shape[:2]

    # Define the size of the ROI, center of the screen
    roi_size = 200  
    roi_x1 = width // 2 - roi_size // 2
    roi_y1 = height // 2 - roi_size // 2
    roi_x2 = roi_x1 + roi_size
    roi_y2 = roi_y1 + roi_size

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Define the region of interest (ROI)
    cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 2)

    # Extract the ROI and find its dominant color
    roi = frame_rgb[roi_y1:roi_y2, roi_x1:roi_x2]
    dominant_color = find_dominant_color(roi, k=1)

    # Create an image with the dominant color in RGB format
    color_display_rgb = np.zeros((100, 100, 3), np.uint8)
    color_display_rgb[:] = dominant_color
    color_display_bgr = cv2.cvtColor(color_display_rgb, cv2.COLOR_RGB2BGR)

    # Display the original frame and the dominant color
    cv2.imshow('Frame', frame)
    cv2.imshow('Dominant Color', color_display_bgr)

    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
