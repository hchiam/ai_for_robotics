import cv2

# edge detection method named after Canny (with thresholds for how strong to be detected)
image_edges = cv2.Canny(grayscale_image, lo_thresh, hi_thresh)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
image = mpimg.imread('image.jpg')
plt.imshow(image)
plt.show()