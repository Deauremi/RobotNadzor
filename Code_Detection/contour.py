import cv2
import numpy as np


def main():
   cap = cv2.VideoCapture(0)


   while True:
       _, frame = cap.read()


       rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

       longueur,largeur,_=frame.shape
       
       couleur_min = np.array([0, 0, 0])
       couleur_max = np.array([50, 50, 50])


       masque = cv2.inRange(rgb, couleur_min, couleur_max)


       noyau = np.ones((5, 5), np.uint8)
       masque = cv2.erode(masque, noyau, iterations=1)
       masque = cv2.dilate(masque, noyau, iterations=1)

       contours, _ = cv2.findContours(masque, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


       detected = False
       if contours:
           largest_contour = max(contours, key=cv2.contourArea)
           x, y, w, h = cv2.boundingRect(largest_contour)
           aspect_ratio = float(w) / h
           #print(largest_contour)
           area_ratio = cv2.contourArea(largest_contour) / (w * h)
          
           if largeur/6 < w < 3*largeur/5 and longueur/5 < h < 3*longueur/4:
               cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
               detected = True
       #print(detected)


       cv2.imshow('Frame', frame)

       cle=cv2.waitKey(1) 
        
       if cle==27:
           break


   cap.release()
   cv2.destroyAllWindows()


if __name__ == '__main__':
   main()



