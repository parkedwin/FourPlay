# Test Image Subtraction

import numpy as np
from scipy.misc import imread, imsave
import pylab as plt

image_prev = imread('game5/full_snap__1.png').astype(np.float32)
image_curr = imread('game5/full_snap__2.png').astype(np.float32)
x = 150
y = 278

print "original",image_curr[y][x]
img_sub = image_prev - image_curr
print "new", image_curr[y][x] 
print "subtract", img_sub[y][x] 
for y_b in range(len(img_sub)):
	for x_b in range(len(img_sub[0])):
		if(not (np.absolute(img_sub[y_b][x_b]) == np.array([0,0,0])).all()):
			img_sub[y_b][x_b] = image_curr[y_b][x_b]
		else:
			img_sub[y_b][x_b] = np.array([0,0,0])

		if(img_sub[y_b][x_b][2] != max(img_sub[y_b][x_b])):
			img_sub[y_b][x_b] = np.array([0,0,0])

print "newval", img_sub[y][x]
img_sub /= 255
plt.imshow(img_sub)
plt.show()
