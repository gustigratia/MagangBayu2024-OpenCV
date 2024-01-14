import cv2 as cv
import numpy as np
from PIL import Image

# Tulis Kodingan kalian dibawah

# Function untuk mencari limit dari hsv color
def get_limits(color): 
    c = np.uint8([[color]]) # insert bgr value yang akan diconvert ke hsv
    hsvC = cv.cvtColor(c, cv.COLOR_BGR2HSV)
    
    lower_limit = hsvC[0][0][0] - 10, 100, 100
    upper_limit = hsvC[0][0][0] + 10, 255, 255
    
    lower_limit = np.array(lower_limit, dtype=np.uint8)
    upper_limit = np.array(upper_limit, dtype=np.uint8)
    
    return lower_limit, upper_limit


whale = [165, 181, 87] # perkiraan colorspace warna paus (BGR), didapat dengan menggunakan function pada file findColor.py 

# Read image
img = cv.imread('tugas/tugas1/tugas1.png')
hsvImg = cv.cvtColor(img, cv.COLOR_BGR2HSV)

lower_limit, upper_limit = get_limits(color=whale)

# Buat mask dari limit yang didapat
mask = cv.inRange(hsvImg, lower_limit, upper_limit)

# Membuat bounding box
mask_ = Image.fromarray(mask)
bbox = mask_.getbbox()

if bbox is not None:
    x1, y1, x2, y2 = bbox
    img = cv.rectangle(img, (x1,y1), (x2,y2), (0, 0, 255), 5)

cv.imshow('Image', img)
cv.waitKey(0)
cv.destroyAllWindows()