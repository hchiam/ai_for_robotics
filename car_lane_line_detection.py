# From lesson 2 of free preview of Self-Driving Car Engineer Nanodegree from Udacity.
# I basically put things in my own words for clearer reading.

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np



def get_pixels_to_change_COLOUR():
    # set colour selection criteria
    r_thresh = 200
    b_thresh = 200
    g_thresh = 200
    rgb_thresh = [r_thresh, g_thresh, b_thresh]
    
    # get pixels that are below rgb threshold
    pixels_to_change_COLOUR = (img[:,:,0] < rgb_thresh[0]) \
                            | (img[:,:,1] < rgb_thresh[1]) \
                            | (img[:,:,2] < rgb_thresh[2])
    return pixels_to_change_COLOUR


def get_pixels_to_change_TRIANGLE():
    # get triangle corner coordinates
    # (top left = [row=0, col=0]) ; like typical x and y but y is flipped
    left = [0, 540]
    right = [960, 540]
    top = [480, 260]
    
    # get fit lines (y=mx+b) as the sides of the triangle
    # np.polyfit() returns [m, b]
    fit_left = np.polyfit((left[0], top[0]), (left[1], top[1]), 1)
    fit_right = np.polyfit((right[0], top[0]), (right[1], top[1]), 1)
    fit_bottom = np.polyfit((left[0], right[0]), (left[1], right[1]), 1)
    
    # get rectangular meshgrid for x and y
    x,y = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))
    
    # get pixels that are within the triangle
    pixels_to_change_TRIANGLE = (y > (fit_left[0] * x + fit_left[1])) \
                              & (y > (fit_right[0] * x + fit_right[1])) \
                              & (y < (fit_bottom[0] * x + fit_bottom[1]))
    return pixels_to_change_TRIANGLE



# get image, print stats
img = mpimg.imread('image.jpg')
print('this image is ', type(img), ' with dimensions ', img.shape)

# get dimensions
xsize = img.shape[1]
ysize = img.shape[0]

# get copy of img, make into array (why copy? (habit: b/c py is pass-by-ref))
lane_lines_select = np.copy(img)

# get pixels to be changed
pixels_to_change_COLOUR = get_pixels_to_change_COLOUR()
pixels_to_change_TRIANGLE = get_pixels_to_change_TRIANGLE()

# set those pixels to red in the corresponding copied array
lane_lines_select[~pixels_to_change_COLOUR & pixels_to_change_TRIANGLE] = [255, 0, 0]

# show filtered image
plt.imshow(lane_lines_select)
plt.show()