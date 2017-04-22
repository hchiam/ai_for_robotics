# edge detection method named after Canny
# (keep pixels with gradient values > hi_thresh, reject if < lo_thresh, keep those between if connected to strong edges)
# image_edges = cv2.Canny(grayscale_image, lo_thresh, hi_thresh)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2



# get image
image = mpimg.imread('image.jpg')

# get grayscale version of image
grayscale_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# smooth out noise to remove likely "false edges"
kernel_size = 3
presmoothed_image = cv2.GaussianBlur(grayscale_image, (kernel_size, kernel_size), 0)

# get edges
lo_thresh = 100
hi_thresh = 200
image_edges = cv2.Canny(presmoothed_image, lo_thresh, hi_thresh)

# show plot
plt.imshow(image_edges, cmap='Greys_r')
plt.show()