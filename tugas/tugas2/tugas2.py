import cv2 as cv
import numpy as np

# Tulis Kodingan kalian dibawah

# Read image
img = cv.imread('tugas/tugas2/tugas2.jpg')
# Ubah ke grayscale
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Lakukan thresholding pada gambar
_, thresh = cv.threshold(imgray, 220, 255, cv.THRESH_BINARY)

# Menemukan contours dengan findContours
contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

# Untuk setiap kontur pada array contours yang terdapat pada gambar, cari yang jumlah sisinya 12 (huruf H)
for contour in contours:
    approx = cv.approxPolyDP(contour,  0.01*cv.arcLength(contour, True), True)
    
    # Jika terdapat kontur yang jumlah sisi = 12; maka drawContours 
    if(len(approx)==12):
        cv.putText(img, str(len(approx)), (10,100), cv.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 3)
        cv.drawContours(img, [approx], 0, (0,0,0), 4)
    

cv.imshow('image', img)
cv.waitKey(0)
cv.destroyAllWindows()