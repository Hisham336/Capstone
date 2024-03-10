import cv2
import numpy as np


while True:
    # Load the image
    image = cv2.imread('sample.jpg')

    # Define the circle area (center and radius)
    cx, cy, _ = image.shape
    center = (cx // 2, cy // 2) # Center of the image
    radius = 100 # Example radius

    # Create a mask of the circle area
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.circle(mask, center, radius, (255), -1)

    # Apply the mask to the image
    cropped_image = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow("data", cropped_image)

    # Reshape the image data
    data = cropped_image.reshape(-1, 3)
    
    data = np.float32(data)

    # Define criteria and apply k-means clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)

    # The dominant color is the center of the cluster
    dominant_color = centers[0].astype(np.int32)
    
    key = cv2.waitKey(1)
    
    if key == 27:
        break


print('Dominant color is: bgr({})'.format(dominant_color))