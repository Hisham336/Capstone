import cv2 as cv

def rescale (img, scale=0.5):
    height = int(img.shape[0] * scale)
    width = int(img.shape[1] * scale)
    dimen = (width, height)
    
    return cv.resize(img,dimen,interpolation=cv.INTER_AREA)

img = cv.imread('circles.jpg')
img = rescale(img, 0.2)
# cv.imshow('Circles', img)

# cv.waitKey(0)

grayScale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

contours, _ = cv.findContours(cv.threshold(grayScale, 127, 255, cv.THRESH_BINARY)[1], cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

first = True

for contour in contours:
    if first:
        first = False
        continue
    
    if cv.arcLength(contour, True) < 100:
        continue
    
    approx = cv.approxPolyDP( 
        contour, cv.arcLength(contour, True), True) 
      
    cv.drawContours(img, [contour], 0, (0, 0, 255), 5) 
  
    M = cv.moments(contour) 
    
    x = 0
    y = 0
    if M['m00'] != 0.0: 
        x = int(M['m10']/M['m00']) 
        y = int(M['m01']/M['m00']) 
 
  
    if len(approx) == 4 and x != 0 and y != 0: 
        cv.putText(img, 'Quadrilateral', (x, y), 
                    cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
  
    elif x != 0 and y != 0: 
        cv.putText(img, 'circle', (x, y), 
                    cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
  
cv.imshow('shapes', img) 
  
cv.waitKey(0) 
cv.destroyAllWindows() 