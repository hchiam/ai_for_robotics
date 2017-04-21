# From lesson 2 of free preview of Self-Driving Car Engineer Nanodegree from Udacity.
# I basically put things in my own words for clearer reading.

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# get image, print stats
img = mpimg.imread('image.jpg')
print('this image is ', type(img), ' with dimensions ', img.shape)

# get dimensions
xsize = img.shape[1]
ysize = img.shape[0]

# get copy of img, make into array (why copy? (habit: b/c py is pass-by-ref))
colour_select = np.copy(img)

# set colour selection criteria
r_thresh = 200
b_thresh = 200
g_thresh = 200
rgb_thresh = [r_thresh, g_thresh, b_thresh]

# get pixels that are below rgb threshold
pixels_to_change = (img[:,:,0] < rgb_thresh[0]) \
                 | (img[:,:,1] < rgb_thresh[1]) \
                 | (img[:,:,2] < rgb_thresh[2])

# set those pixels to black in the corresponding copied array
colour_select[pixels_to_change] = [0,0,0]

# show filtered image
plt.imshow(colour_select)
plt.show()