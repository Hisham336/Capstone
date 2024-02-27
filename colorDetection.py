import cv2 as cv
import numpy as np

def get_limits (colorList):
    color = np.uint8([[colorList]])
    hsv = cv.cvtColor(color, cv.COLOR_BGR2HSV)
    
    lower = hsv[0][0][0] - 10, 10, 10
    upper = hsv[0][0][0] + 10, 10, 10
    
    lower = np.array(lower, dtype=np.uint8)
    upper = np.array(upper, dtype=np.uint8)
    
    return (lower, upper)

def rescale (img, scale=0.5):
    height = int(img.shape[0] * scale)
    width = int(img.shape[1] * scale)
    dimen = (width, height)
    
    return cv.resize(img,dimen,interpolation=cv.INTER_AREA)

img = cv.imread('circles.jpg')
img = rescale(img, 0.2)
# cv.imshow('Circles', img)

# cv.waitKey(0)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

lower, upper = get_limits([75, 170, 210])

mask = cv.inRange(hsv, lower, upper)

cv.imshow('Colors', mask)

cv.waitKey(0) 
cv.destroyAllWindows() 