import cv2
import numpy as np

kernelOpen  = np.ones ((5,5))
kernelClose = np.ones ((15,15))

def nothing (x):
    pass

cv2.namedWindow ("Range HSV")
cv2.resizeWindow ("Range HSV", 500, 350)
cv2.createTrackbar ("HUE Min",   "Range HSV", 6, 179,nothing)
cv2.createTrackbar ("HUE Max",   "Range HSV", 30, 179,nothing)
cv2.createTrackbar ("SAT Min",   "Range HSV", 120,  255,nothing)
cv2.createTrackbar ("SAT Max",   "Range HSV", 255, 255,nothing)
cv2.createTrackbar ("VALUE Min", "Range HSV", 211,  255,nothing)
cv2.createTrackbar ("VALUE Max", "Range HSV", 255, 255,nothing)

vid = False # video = 1, foto = 0

if vid is True:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("cap.VideoCapture() failed")
        exit()

while True:
    if vid is False:
        img = cv2.imread("tugas/tugas1/tugas1.png")
    else:
        ret, img = cap.read()

    h, w, c = img.shape
    canvas = np.zeros((2 * img.shape[0], 2 * img.shape[1], 3), dtype=np.uint8)


    frame = cv2.GaussianBlur(img, (5,5), 0)

    # HSV Trackbar
    h_min = cv2.getTrackbarPos ("HUE Min",   "Range HSV")
    h_max = cv2.getTrackbarPos ("HUE Max",   "Range HSV")
    s_min = cv2.getTrackbarPos ("SAT Min",   "Range HSV")
    s_max = cv2.getTrackbarPos ("SAT Max",   "Range HSV")
    v_min = cv2.getTrackbarPos ("VALUE Min", "Range HSV")
    v_max = cv2.getTrackbarPos ("VALUE Max", "Range HSV")

    # Batas Max, Min HSV
    lowerBound = np.array ([h_min, s_min, v_min])
    upperBound = np.array ([h_max, s_max, v_max])

    # rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV) #COLOR_BGR2HSV lebih noise
    bgr = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Filtering
    mask = cv2.inRange (bgr, lowerBound, upperBound)
    maskOpen  = cv2.morphologyEx (mask,     cv2.MORPH_OPEN,  kernelOpen) # remove noise
    maskClose = cv2.morphologyEx (maskOpen, cv2.MORPH_CLOSE, kernelClose) # close small holes or gaps

    # Contour
    c, h  = cv2.findContours (maskClose, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours (img, c, -1, (255, 0, 0) , 2)

    # cv2.imshow("img", img)
    # cv2.imshow("frame", frame)
    # cv2.imshow ("maskClose", maskClose)
    # cv2.imshow ("maskOpen", maskOpen)

    canvas[:img.shape[0], :img.shape[1]] = img
    canvas[:img.shape[0], img.shape[1]:] = frame
    canvas[img.shape[0]:, :img.shape[1]] = cv2.cvtColor(maskClose, cv2.COLOR_GRAY2BGR)  # Convert maskClose to BGR before placing
    canvas[img.shape[0]:, img.shape[1]:] = cv2.cvtColor(maskOpen, cv2.COLOR_GRAY2BGR)  # Convert maskOpen to BGR before placing

    cv2.imshow("Combined Image", canvas)

    print("shape:",frame.shape)
    if cv2.waitKey(1) == 27:
        break


if vid is True: cap.release()
cv2.destroyAllWindows()