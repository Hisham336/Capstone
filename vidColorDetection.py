import cv2
import numpy as np
def rescale (img, scale=0.5):
        height = int(img.shape[0] * scale)
        width = int(img.shape[1] * scale)
        dimen = (width, height)
        
        return cv2.resize(img,dimen,interpolation=cv2.INTER_AREA)    
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
while True:
    
    # frame = cv2.imread('sample.jpg')
    _, frame = cap.read()
    # frame = rescale(frame, 0.2)
    frame = cv2.flip(frame, 1)

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)
    
    radius = 200
    
    mask = np.zeros_like(frame, dtype=np.uint8)
    # cv2.circle(mask, frame, radius, (255, 255, 255), -1)

    # Extract the pixels within the circle
    circle_pixels = cv2.bitwise_and(frame, mask)

    # Convert the extracted pixels to np.float32
    circle_pixels_float32 = circle_pixels.astype(np.float32)
    
    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(circle_pixels_float32, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    

    pixel_center = hsv_frame[cy, cx]
    hue_value = pixel_center[0]

    color = "Undefined"
    if hue_value < 5:
        color = "RED"
    elif hue_value < 22:
        color = "ORANGE"
    elif hue_value < 33:
        color = "YELLOW"
    elif hue_value < 78:
        color = "GREEN"
    elif hue_value < 131:
        color = "BLUE"
    elif hue_value < 170:
        color = "VIOLET"
    else:
        color = "RED"

    pixel_center_bgr = frame[cy, cx]
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
    cv2.putText(frame, color, (10, 70), 0, 1.5, (b, g, r), 2)
    cv2.circle(frame, (cx, cy), radius, (25, 25, 25), 3)
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
