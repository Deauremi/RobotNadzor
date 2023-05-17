from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtGui import QImage, QPixmap
import sys
import socket
import keyboard
import sys
import time
from enum import Enum
import multiprocessing as mp
import cv2
import base64
import numpy as np


BUFF_SIZE = 65536
host_raspberry="192.168.1.10"
host_application = '192.168.1.18'
port = 8040
nb_workers = 1
timeout_seconds = 15
running=True

class Ui_Application(QWidget):
    @pyqtSlot(QPixmap)
    def setImage(self, pixmap):
        self.video.setPixmap(pixmap)

    def setupUi(self, Application,queue,queue2):
        super().__init__()
        self.queue=queue
        Application.setObjectName("Application")
        Application.resize(1200, 775)
        self.ApplicationRobot = QWidget(Application)
        self.ApplicationRobot.setMinimumSize(QtCore.QSize(1200, 750))
        self.ApplicationRobot.setBaseSize(QtCore.QSize(1200, 750))
        self.ApplicationRobot.setStyleSheet("")
        self.ApplicationRobot.setObjectName("ApplicationRobot")
       
        self.groupBox = QGroupBox(self.ApplicationRobot)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 241, 721))
        self.groupBox.setObjectName("groupBox")
        self.textBrowser = QTextBrowser(self.groupBox)
        self.textBrowser.setGeometry(QtCore.QRect(20, 20, 201, 681))
        self.textBrowser.setObjectName("textBrowser")
        
        self.groupBox_3 = QGroupBox(self.ApplicationRobot)
        self.groupBox_3.setGeometry(QtCore.QRect(260, 10, 681, 721))
        self.groupBox_3.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_3.setObjectName("groupBox_3")
        self.video = QLabel(self.groupBox_3)
        self.video.setGeometry(QtCore.QRect(20, 20, 640, 480))
        self.video.resize(640, 480)
        th = Thread(self,queue2)
        th.changePixmap.connect(self.setImage)
        th.start()

        self.groupBox_2 = QGroupBox(self.ApplicationRobot)
        self.groupBox_2.setGeometry(QtCore.QRect(950, 10, 231, 721))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.checkBox = QCheckBox(self.groupBox_2)
        self.checkBox.setGeometry(QtCore.QRect(20, 660, 191, 51))
        self.checkBox.setObjectName("checkBox")
        self.comboBox = QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QtCore.QRect(20, 60, 191, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton = QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(20, 100, 191, 22))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.joystick = Joystick(queue,self.groupBox_2)
        self.joystick.setGeometry(QtCore.QRect(20, 330, 191, 51))
       
        Application.setCentralWidget(self.ApplicationRobot)
        self.statusbar = QStatusBar(Application)
        self.statusbar.setObjectName("statusbar")
        Application.setStatusBar(self.statusbar)

        self.retranslateUi(Application)
        QtCore.QMetaObject.connectSlotsByName(Application)


    def retranslateUi(self, Application):
        _translate = QtCore.QCoreApplication.translate
        Application.setWindowTitle(_translate("Application", "ApplicationRobot"))
        self.groupBox.setTitle(_translate("Application", "Historique des notifications"))
        self.groupBox_3.setTitle(_translate("Application", "Vidéo"))
        self.groupBox_2.setTitle(_translate("Application", "Contrôle du robot "))
        self.checkBox.setText(_translate("Application", "Le robot continue d\'avancer"))
        self.comboBox.setItemText(0, _translate("Application", "0"))
        self.comboBox.setItemText(1, _translate("Application", "45"))
        self.comboBox.setItemText(2, _translate("Application", "90"))
        self.comboBox.setItemText(3, _translate("Application", "135"))
        self.comboBox.setItemText(4, _translate("Application", "180"))
        self.pushButton.setText(_translate("Application", "Tourner la tête du robot"))
    
    def pushButton_clicked(self):
        message=self.comboBox.currentText() 
        self.queue.put(message)


class Thread(QThread):
    changePixmap = pyqtSignal(QPixmap)

    def __init__(self, parent=None,queue=None):
        QThread.__init__(self, parent=parent)
        self.queue=queue

    def run(self):
        #cp=cv2.VideoCapture(0)
        while True:
            #ret, frame = cp.read()
            frame=self.queue.get()
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            qImg = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            scaled_pixmap = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(scaled_pixmap)


class Joystick(QWidget):
    def __init__(self,queue = None, parent=None):
        super(Joystick, self).__init__(parent)
        self.setMinimumSize(100, 100)
        self.movingOffset = QPointF(0,0)
        self.grabCenter = False
        self.__maxDistance = 50
        self.q=queue

    def paintEvent(self, event):
        painter = QPainter(self)
        bounds = QRectF(-self.__maxDistance, -self.__maxDistance, self.__maxDistance * 2, self.__maxDistance * 2).translated(self._center())
        painter.drawEllipse(bounds)
        painter.setBrush(Qt.black)
        painter.drawEllipse(self._centerEllipse())

    def _centerEllipse(self):
        if self.grabCenter:
            return QRectF(-20, -20, 40, 40).translated(self.movingOffset)
        return QRectF(-20, -20, 40, 40).translated(self._center())

    def _center(self):
        return QPointF(self.width()/2, self.height()/2)

    def _boundJoystick(self, point):
        limitLine = QLineF(self._center(), point)
        if (limitLine.length() > self.__maxDistance):
            limitLine.setLength(self.__maxDistance)
        return limitLine.p2()

    def joystickDirection(self):
        normVector = QLineF(self._center(), self.movingOffset)
        currentDistance = normVector.length()
        angle = round(normVector.angle())
        direction =""
        if 45 <= angle < 135:
            direction="z"
        elif 135 <= angle < 225:
            direction="q"
        elif 225 <= angle < 315:
            direction="s"
        elif 0<=angle<45 or 315<= angle < 360 :
            direction="d"
        else:
            direction="s"
        #distance = round(min(currentDistance / self.__maxDistance, 1.0),2)
        #angleMes = "angle:"
        message = direction
        return(message)

    def mousePressEvent(self, ev):
        self.grabCenter = self._centerEllipse().contains(ev.pos())
        return super().mousePressEvent(ev)

    def mouseReleaseEvent(self, event):
        self.grabCenter = False
        self.movingOffset = QPointF(0, 0)
        self.update()

    def mouseMoveEvent(self, event):
        if self.grabCenter:
            self.movingOffset = self._boundJoystick(event.pos())
            self.update()
        self.q.put(self.joystickDirection())

def on_key_press(event):
    global running
    if event.name == 'esc':
        if running : 
            print("Vous avez appuyé sur la touche 'Esc', le programme va s'éteindre.")
            running = False
            time.sleep(1)
            sys.exit()

keyboard.on_press(on_key_press)

def handle_connection(conn):
    with conn:
        conn.settimeout(timeout_seconds)
        buff = conn.recv(512)
        if buff:
            message = buff.decode('utf-8')

def envoyer(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_envoie:
        try :
            message = str(message).encode('utf-8')
            print(message)
            s_envoie.connect((host_raspberry, port))
            s_envoie.send(message)
        except socket.error:
            print("Erreur lors de l'envoie du message")
            pass

def recevoirImage(sock):
    while True:
        sock.listen(5)
        client, address = sock.accept()
        print("connexion reçue")
        # on ouvre un fichier (s'il existe déjà, ça l'écrase) pour y stocker tous les octets de l'image
        # les 8 premiers octets indiquent la taille de l'image
        with open("image_recue.jpg", 'wb') as img:
            taille = int.from_bytes(client.recv(8), byteorder='big')
            print("image taille : " + str(taille))
            acc = 0
            while acc < taille:
                donnee = client.recv(4096)
                img.write(donnee)
                acc += len(donnee)
        print("image received")

def main_photo(queue):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host_application, port+2))
    recevoirImage(sock)
    sock.close()

def main_data(queue):
    pool = mp.Pool(nb_workers)
    i=0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host_application, port))
        s.listen(1)
        s.setblocking(False)
        while running:
            item=queue.get()
            i+=1
            if item != None and i==20:
                i=0
                envoyer(item)
            elif item in ["0","45","90","135","180"]:
                envoyer(item)
            try:
                conn, address = s.accept()
                pool.apply_async(handle_connection, (conn,))
            except socket.error:
                pass
    pool.close()
    pool.join()

def main_appli(queue,queue2):
    app = QApplication(sys.argv)
    Application = QMainWindow()
    ui = Ui_Application()
    ui.setupUi(Application,queue,queue2)
    Application.show()
    sys.exit(app.exec_())

def main_video(queue):
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    print(host_raspberry)
    port_video = port+1
    message = b'Hello'
    client_socket.sendto(message,(host_raspberry,port_video))
    fps,st,frames_to_count,cnt = (0,0,20,0)
    while True:
        packet,_ = client_socket.recvfrom(BUFF_SIZE)

        npdata = np.frombuffer(packet, dtype=np.uint8)
        
        #frame = cv2.imdecode(npdata,1)
        frame = cv2.putText(npdata,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        #cv2.imshow("RECEIVING VIDEO",frame)
        queue.put(frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            client_socket.close()
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count/(time.time()-st))
                st=time.time()
                cnt=0
            except:
                pass
        cnt+=1

if __name__ == "__main__":
    manager=mp.Manager()
    q=mp.Queue()
    q2=manager.Queue()
    p1 = mp.Process(target=main_data, args=(q,))
    p2 = mp.Process(target=main_appli, args=(q,q2,))
    p3 = mp.Process(target=main_video, args=(q2,))
    p4 = mp.Process(target=main_photo, args=(q,))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()