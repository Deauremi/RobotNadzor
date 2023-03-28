import cv2
from time import *


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,500)

while True :
    _, frame = cap.read()
    hsv_frame=cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    height, width, _=frame.shape
   
    x=int(width/2)
    y=int(height/2)

    x_mv=x
    y_mv=y 
    #print(x_mv)
    detecteur=[frame[y,x]]
    v_h=[detecteur[0][0]]
    v_s=[detecteur[0][1]]
    v_v=[detecteur[0][2]]

    
    for k in range(10):       #calcul de la moyenne des pixels autour du centre 
        for i in range(1,11):
            y_mv+=1
            detecteur.append(frame[y_mv,x_mv])
            v_h.append(detecteur[i][0])
            v_s.append(detecteur[i][1])
            v_v.append(detecteur[i][2])
        x_mv+=1

    valeur_h=0
    valeur_s=0
    valeur_v=0
 

    for j in range(len(v_h)):
        valeur_h+=v_h[j]
        valeur_s+=v_s[j]
        valeur_v+=v_v[j]

    valeur_h=valeur_h/len(v_h)
    valeur_s=valeur_s/len(v_s)
    valeur_v=valeur_v/len(v_v)


    moyenne=[valeur_h,valeur_s,valeur_v]
    #print(moyenne)

    if valeur_v>200 and valeur_h<80 and valeur_s<80:
        cv2.imwrite('Intrus_detecte.png',frame)

        
        

       
    cv2.rectangle(frame, [x-15,y-15], [x+15,y+15] , [0,0,0],5)
    cv2.imshow("Frame", frame)

    key=cv2.waitKey(1) 
        
    if key==27:
        break


cap.release()
cv2.destroyAllWindows()