import numpy as np
import cv2 as cv
from matplotlib.pyplot import *
import csv

def enregistrement(record_duration, where_file):
    webcam = cv.VideoCapture(0)
    largeur_image = int(webcam.get(cv.CAP_PROP_FRAME_WIDTH))
    hauteur_image = int(webcam.get(cv.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv.VideoWriter_fourcc(*'MJPG')
    fichier = cv.VideoWriter(where_file, fourcc,20,(largeur_image,hauteur_image))
    start_time_record=time.time()
    while(True):
        # Capture image par image
        ret, img = webcam.read()
        if ret==True:
            fichier.write(img)
            # Preparation de l'affichage de l'image
            #cv.imshow('Ma Webcam',img)
            # affichage et saisie d'un code clavier
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            if (time.time() - start_time_record) > record_duration :
                break
        else:
            break
    # Ne pas oublier de fermer le flux et la fenetre
    webcam.release()
    fichier.release()
    cv.destroyAllWindows()

def vitesse_eau_region_ligne(name, origine, dimension):

    cap = cv.VideoCapture(cv.samples.findFile(name))
    ret, frame1 = cap.read()
    prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255
    
    #enregistrement des images à afficher sur le site internet avec une sauvegarde avec la date et l'heure dans un répertoire dédié
    cv.imwrite(f"/home/utilisateur/Desktop/flood_sentinel/SAVE/PICTURE/PICTURE_{time.asctime(time.localtime())}.png" , frame1)
    cv.imwrite("/var/www/html/PICTURE.png" , frame1)

    #définition des variables
    nbr_frame=0
    (xo,yo)=origine
    (xd,yd)=dimension
    final=[]

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

        #print(hsv.shape)

        values=hsv[xo:xo+xd, yo:yo+yd, 2]
        values_TR=values.mean(axis=0)
        final.append(values_TR*0.15*0.30)
        final_TR=np.array(final).mean(axis=1)

        #print(np.array(final).size)
        #print(np.array(final_TR).size)

        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
        elif k == ord('s'):
            cv.imwrite('opticalfb.png', frame2)
            cv.imwrite('opticalhsv.png', bgr)
        prvs = next

        cv.destroyAllWindows()

    return(final, final_TR, nbr_frame)

def vitesse_eau_point_moyenne(name, origine, dimension):

    cap = cv.VideoCapture(cv.samples.findFile(name))
    ret, frame1 = cap.read()
    prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255

    #définition des variables
    nbr_frame=0
    (xo,yo)=origine
    (xd,yd)=dimension
    final=[]

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

        #print(hsv.shape)

        values=hsv[xo-round(xd/2):xo+round(xd/2), yo-round(yd/2):yo+round(yd/2), 2]
        values_TR=values.mean(axis=0)
        final.append(values_TR*0.15*0.30)
        final_TR=np.array(final).mean(axis=0)

        final_min=[]
        final_max=[]
        values_MM=hsv[..., 2]
        values_MM=values_MM*0.15*0.30
        #print(values_MM)
        """
        for i in range(len(values_MM)):
            values_max=values_MM.max(axis=1).max(axis=0)
            values_min=values_MM.min(axis=1).min(axis=0)
            final_max.append(values_max)
            final_min.append(values_min)
        final_min=np.array(final_min)
        final_max=np.array(final_max)
        """
        #print(np.array(final).size)
        #print(np.array(final_TR).size)

        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
        elif k == ord('s'):
            cv.imwrite('opticalfb.png', frame2)
            cv.imwrite('opticalhsv.png', bgr)
        prvs = next

        cv.destroyAllWindows()

    return(final, final_TR, final_max, final_min, nbr_frame)

def enregistrement_min_max(variable):
    clf()
    plot(variable[1])
    plot(variable[2])
    plot(variable[3])
    savefig(f"/home/utilisateur/Desktop/flood_sentinel/SAVE/GRAPHIQUE/Graph_vitesse_pt{time.asctime(time.localtime())}.png")
    savefig(f"/var/www/html/Graph2.png")

def affichage(variable):
    plot(variable)
    show()

def enregistrement_graph(variable):
    clf()
    plot(variable)
    savefig(f"/home/utilisateur/Desktop/flood_sentinel/SAVE/GRAPHIQUE/Graph_vitesse_ligne{time.asctime(time.localtime())}.png")
    savefig(f"/var/www/html/Graph.png")

def return_data(values):
    data = values
    with open('/home/utilisateur/Desktop/flood_sentinel/SAVE/DATA/VITESSE/data_VITESSE.csv', 'a') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(data)

def fonction(duration, duration_record, name_file, where_file, origine, dimension):
    enregistrement(duration_record, where_file)
    time.sleep(4)
    return_data(vitesse_eau_region_ligne(name_file, origine, dimension)[1])

#enregistrement(3, "/home/utilisateur/Desktop/flood sentinel/film2.avi")

#affichage(vitesse_eau_region_ligne("film2.avi", (300,0), (20,640))[1])


start_time=time.time()
duration_time=3601
while(True):
    time.sleep(10)
    fonction(4, 2, "rec.avi", "/home/utilisateur/Desktop/flood_sentinel/PROGRAMME/rec.avi", (300,0), (20,640))
    print("Enregistrement effectué.")
    variable=vitesse_eau_region_ligne("rec.avi", (300,0), (20,640))[1]
    if (time.time() - start_time) > duration_time :
        break
    enregistrement_graph(variable)
    enregistrement_min_max(vitesse_eau_point_moyenne("rec.avi", (370,240), (20,20)))
    print("Valeurs enregistrer")
