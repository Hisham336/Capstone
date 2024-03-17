import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

def rescale(img, scale=0.5):
    height = int(img.shape[0] * scale)
    width = int(img.shape[1] * scale)
    dimen = (width, height)
    return cv2.resize(img, dimen, interpolation=cv2.INTER_AREA)

def roi(frame, x:int, y:int, r=50):
    return frame[int(y-r/2):int(y+r/2), int(x-r/2):int(x+r/2)]

def findColor(frame, cx:int, cy:int, radius:int, n_colors=5):
    roi_frame = roi(frame, cx, cy, radius)
    roi_frame_float32 = roi_frame.astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(roi_frame_float32.reshape(-1, 3), n_colors, None, criteria, 10, flags)
    unique_labels, counts = np.unique(labels, return_counts=True)
    max_count_label = unique_labels[np.argmax(counts)]
    dominant_color = palette[max_count_label]
    return dominant_color[0], dominant_color[1], dominant_color[2]

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(1280, 720))

# Allow the camera to warmup
time.sleep(0.1)

beginX = 200
beginY = 200
endX = 1000
endY = 600
rows = 3
columns = 5
radius = 50
n_colors = 5

while True:
    # Capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = frame.array
        frame = cv2.flip(frame, 1)
        
        stepX = (endX - beginX)/float(columns)
        stepY = (endY - beginY)/float(rows)
        
        xList = np.arange(beginX, endX, stepX).tolist()
        yList = np.arange(beginY, endY, stepY).tolist()
        
        for cx in xList:
            for cy in yList:
                x = int(cx)
                y = int(cy)
                b, g, r = findColor(frame, x, y, radius, n_colors)
                cv2.circle(frame, (x, y), radius, (25, 25, 25), 3)
                cv2.rectangle(frame, (x-20, y-20+radius+10), (x+20, y+radius+10), (int(b), int(g), int(r)), thickness=-1)
                cv2.rectangle(frame, (x-20, y-20+radius+10), (x+20, y+radius+10), (25, 25, 25), 3)
        
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        
        # Clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        
        if key == ord("q"):
            break

cv2.destroyAllWindows()