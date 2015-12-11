from PIL import ImageGrab
import os
import sys
import time
import mouseClick
from random import randint

xgap = 6
ygap = 124
window_len = 619
window_height = 420

def screenShot(iteration):
	box = (xgap, ygap, xgap + window_len, ygap + window_height)
	im = ImageGrab.grab(box)
	im.save(os.getcwd() + '/callibrate' + '/full_snap__' + str(iteration) + '.png', 'PNG')

screenShot(sys.argv[1])