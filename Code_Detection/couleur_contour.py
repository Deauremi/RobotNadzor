import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,500)

couleur=False

while couleur==False :
    _, frame = cap.read()
    rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _=frame.shape


    x=int(width/2)
    y=int(height/2)

    x_mv=x
    y_mv=y 

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
    print(moyenne)

    if valeur_v>210 and valeur_h<90 and valeur_s<90:
        cv2.imwrite('Intrus_detecte.png',frame)
        couleur=True
        cap.release()
        cv2.destroyAllWindows()
        


    cv2.rectangle(frame, [x-15,y-15], [x+15,y+15] , [0,0,0],5)
    cv2.imshow("Frame", frame)

    key=cv2.waitKey(1) 
        
    if key==27:
        break

def main():
   
   cap = cv2.VideoCapture(0)

   while couleur==True:
       _, frame = cap.read()


       rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

       longueur,largeur,_=frame.shape
       
       couleur_min = np.array([100, 0, 0])
       couleur_max = np.array([255, 80, 80])


       masque = cv2.inRange(rgb, couleur_min, couleur_max)


       noyau = np.ones((7, 7), np.uint8)
       masque = cv2.erode(masque, noyau, iterations=3)
       masque = cv2.dilate(masque, noyau, iterations=4)

       contours, _ = cv2.findContours(masque, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


       detected = False
       if contours:
           largest_contour = max(contours, key=cv2.contourArea)
           x, y, w, h = cv2.boundingRect(largest_contour)
           aspect_ratio = float(w) / h
           area_ratio = cv2.contourArea(largest_contour) / (w * h)
          
           if largeur/6 < w < 3*largeur/5 and longueur/5 < h < 3*longueur/4 and aspect_ratio<1:
               cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
               detected = True

       cv2.imshow('Frame', frame)

       cle=cv2.waitKey(1) 
        
       if cle==27:
           break
       
cap.release()
cv2.destroyAllWindows()

if __name__ == '__main__':
   main()