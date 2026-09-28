import numpy as np
import cv2 as cv
from matplotlib.pyplot import *

def aff_vitesse_eau(name):

    cap = cv.VideoCapture(cv.samples.findFile(name))
    ret, frame1 = cap.read()
    prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255

    nbr_frame=0

    while(1):

        nbr_frame=nbr_frame+1

        ret, frame2 = cap.read()
        if not ret:
            print('No frames grabbed!')
            break

        next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang*180/np.pi/2
        hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

        cv.imshow('Vitesse surface',bgr)

        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
        elif k == ord('s'):
            cv.imwrite('opticalfb.png', frame2)
            cv.imwrite('opticalhsv.png', bgr)
        prvs = next
        
    cv.destroyAllWindows()

aff_vitesse_eau("seq_5.mp4")