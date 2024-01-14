import cv2 as cv
import numpy as np


# Function untuk mencari colorspace suatu objek pada gambar dengan mouse event
def click_event(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        blue = img[y,x,0]
        green = img[y,x,1]
        red = img[y,x,2]
        font = cv.FONT_HERSHEY_SIMPLEX
        strbgr = str(blue) + ',' + str(green) + ',' + str(red)
        cv.putText(img, strbgr, (x,y), font, 0.8, (0,255,255), 2)
        cv.imshow('image', img)
        
# img = np.zeros([512,512,3], np.uint8)
img = cv.imread('tugas/tugas1/tugas1.png')
cv.imshow('image', img)

cv.setMouseCallback('image', click_event)

cv.waitKey(0)
cv.destroyAllWindows()