import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector


# Tulis Kodingan kalian dibawah

# =============== VIRTUAL CALCULATOR ===============
# Untuk menekan tombol, bentuk 2 jari (telunjuk dan tengah) dan rapatkan seperti menggunting
# Pastikan bahwa sudah terinstall package "cvzone" dan "mediapipe" untuk handtracking

# Membuat class tombol kalkulator dengan OOP
class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
        
    def draw(self, frame):
        cv.rectangle(frame, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (225,225,225), -1)
        cv.rectangle(frame, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (20,20,20), 3)
        cv.putText(frame, self.value, (self.pos[0]+40, self.pos[1]+60), cv.FONT_HERSHEY_PLAIN, 2, (50,50,50), 2)
    
    # Method untuk cek apakah jari kita terletak di button
    def clickCheck(self, x, y):
        if self.pos[0]<x<self.pos[0]+self.width and self.pos[1]<y<self.pos[1]+self.height:
            cv.rectangle(frame, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (255,255,255), -1)
            cv.rectangle(frame, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (20,20,20), 3)
            cv.putText(frame, self.value, (self.pos[0]+35, self.pos[1]+65), cv.FONT_HERSHEY_PLAIN, 3, (0,0,0), 4)
            return True
        else:
            return False
        
# Webcam
cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Generate object button
buttonListValues = [['7','8','9','*'],
                    ['4','5','6','-'],
                    ['1','2','3','+'],
                    ['=','0','/','.']]

button_list = []
for x in range(4):
    for y in range(4):   
        xpos = x*100 + 800
        ypos = y*100 + 150
        button_list.append(Button((xpos,ypos),100,100,buttonListValues[y][x]))

# Variables
equation = ''
delayCounter =0

# Main loop
while(True):
    # Mengambil frame dari webcam
    success, frame = cap.read()
    frame = cv.flip(frame, 1)
    
    if success == True:
        # Deteksi tangan
        hands, frame = detector.findHands(frame, flipType=False)
        
        # Membuat tombol
        cv.rectangle(frame, (800,50), (800 + 400, 70 + 100), (225,225,225), -1)
        cv.rectangle(frame, (800,50), (800 + 400, 70 + 100), (50,50,50), 3)
        for button in button_list:
            button.draw(frame)
        
        # Cek tangan
        if hands:
            lmList = hands[0]['lmList']
            
            # Index untuk jari telunjuk dan jari tengah pada lmList adalah 8 dan 12
            length, _, frame = detector.findDistance(lmList[8][:2], lmList[12][:2], frame)        
            x,y = lmList[8][:2]
            
            # Processing
            if length<50:
                for i, button in enumerate(button_list):
                    if button.clickCheck(x,y) and delayCounter == 0:
                        value = buttonListValues[int(i%4)][int(i/4)]
                        if value == '=':
                            equation = str(eval(equation))
                        else:
                            equation += value   
                        delayCounter = 1
                        
        # Menghapus duplikat dari value
        if delayCounter != 0:
            delayCounter += 1
            if delayCounter >10:
                delayCounter = 0
        
        # Menampilkan Hasil
        cv.putText(frame, equation, (810, 115), cv.FONT_HERSHEY_PLAIN, 3, (50,50,50), 3)
        
        cv.imshow("window", frame)
    
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break
        
        # Membuat clear button dengan menekan 'c' pada keyboard
        elif k == ord('c'):
            equation = ''
    else:
        break
    
cap.release()
cv.destroyAllWindows()
    