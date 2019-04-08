import numpy as np
import cv2
import objekti

video = str('video2.mp4')
cap = cv2.VideoCapture(video)


#for p in range(1, 11):
    #cap = cv2.VideoCapture('video' + str(p) + '.mp4')
bgsub = cv2.createBackgroundSubtractorMOG2(detectShadows=True)  # background subtractor


w = cap.get(3)  # width
h = cap.get(4)  # height
mx = int(w / 8)
my = int(h / 8)

# all variables
font = cv2.FONT_HERSHEY_SIMPLEX

objectss = []
ukupno = []
vreme = 0
kraj = 0
objectId = 1
areaMin = 25
areaMax = 300
wid3 = 25
hei3 = 35
expected = 0
accur = 0
gornja_granica = int(h * 0.9)
donja_granica = int(h * 0.25)
leva_granica = int(5 * (w / 16))
desna_granica = int(11 * (w / 16))

#racunanje centroida
def calculateCentroid(contour):
    moments = cv2.moments(contour)
    x = int(moments['m10']/moments['m00'])
    y = int(moments['m01']/moments['m00'])
    return x, y

def UkloniSum(frame):
    openKernel = np.ones((3, 3), np.uint8)
    closeKernel = np.ones((11, 11), np.uint8)
    # Otvaranje (erode->dilate)
    frameMask = cv2.morphologyEx(frame, cv2.MORPH_OPEN, openKernel)
    # Zatvaranje (dilate -> erode)
    frameMask = cv2.morphologyEx(frameMask, cv2.MORPH_CLOSE, closeKernel)
    return frameMask

while (cap.isOpened()):
    #citanje frejma
    ret, frame = cap.read()

    fgmask = bgsub.apply(frame)
    #otklanjane suma
    try:

        ret, imBin = cv2.threshold(fgmask, 210, 255, cv2.THRESH_BINARY)
        mask = UkloniSum(imBin)
    except:
        print('EOF')
        break

    #pravi konture
    _, contours0, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours0:

        area = cv2.contourArea(cnt)
        if (area > areaMin and area < areaMax):  # contours treshold check

            x, y, w, h = cv2.boundingRect(cnt)
            calculateCentroid(cnt)
            new = True
            for i in objectss:
                if abs(x - i.getX()) <= wid3 and abs(y - i.getY()) <= hei3:

                    i.setVreme()
                    new = False
                    i.updateCoords(x, y)
                    break
                else:
                    i.setKraj()
            if new == True:
                o = objekti.TrackableObject(objectId, x, y, vreme, kraj)
                objectss.append(o)
                objectId += 1

            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)


    # checking if object is a person to count
    for objekat in objectss:
        if objekat.getVreme() > 15:
            if objekat not in ukupno:
                if (objekat.getY()) >= donja_granica and (objekat.getY()) <= gornja_granica:
                    ukupno.append(objekat)



    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break
 # show video and numbeer
    num = len(ukupno)
    strin = str(num)
    cv2.putText(frame, strin, (mx, my), font, 1, (255, 200, 200), 1, cv2.LINE_AA)
    cv2.imshow('Counter', frame)


cap.release()  # realease video
#upisa rezultata
f = open('result.txt', 'a+')
f.write(str(num))
f.write("\n")
cv2.destroyAllWindows()  # close all openCV windows

