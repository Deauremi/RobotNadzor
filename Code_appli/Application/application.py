from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
import sys
import socket,multiproccesing
import keyboard
import sys
import select
import time
from enum import Enum
import multiprocessing as mp
import cv2

host="192.168.135.122"
host2 = '192.168.135.21'
port = 8040
nb_workers = 1
timeout_seconds = 15
running=True

class Ui_Application(object):
    def setupUi(self, Application,queue):
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
        self.video.move(280, 120)
        self.video.resize(640, 480)
        """th = Thread(self.video)
        th.changePixmap.connect(self.setImage)
        th.start()
        """
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
        self.joystick = Joystick(queue,self.groupBox_2)
        self.joystick.setGeometry(QtCore.QRect(20, 330, 191, 51))
       
        Application.setCentralWidget(self.ApplicationRobot)
        self.statusbar = QStatusBar(Application)
        self.statusbar.setObjectName("statusbar")
        Application.setStatusBar(self.statusbar)

        self.retranslateUi(Application)
        QtCore.QMetaObject.connectSlotsByName(Application)

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.video.setPixmap(QPixmap.fromImage(image))

    def retranslateUi(self, Application):
        _translate = QtCore.QCoreApplication.translate
        Application.setWindowTitle(_translate("Application", "ApplicationRobot"))
        self.groupBox.setTitle(_translate("Application", "Historique des notifications"))
        self.groupBox_3.setTitle(_translate("Application", "Vidéo"))
        self.groupBox_2.setTitle(_translate("Application", "Contrôle du robot "))
        self.checkBox.setText(_translate("Application", "Le robot continue d\'avancer"))
        self.comboBox.setItemText(0, _translate("Application", "Commande1"))
        self.comboBox.setItemText(1, _translate("Application", "Commande2"))

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


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
        if not self.grabCenter:
            return 0
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
        else :
            direction="d"
        #distance = round(min(currentDistance / self.__maxDistance, 1.0),2)
        #angleMes = "angle:"
        message = direction.encode("utf-8")
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
            print(message)

def envoyer(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_envoie:
        try :
            s_envoie.connect((host, port))
            print("envoie de : ",message)
            s_envoie.send(message)
        except socket.error:
            pass


def main_data(queue):
    pool = mp.Pool(nb_workers)
    i=0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host2, port))
        s.listen(1)
        s.setblocking(False)
        while running:
            item=queue.get()
            i+=1
            if item != None and i==20:
                i=0
                envoyer(item)
            try:
                conn, address = s.accept()
                pool.apply_async(handle_connection, (conn,))
            except socket.error:
                pass
    pool.close()
    pool.join()

def main_appli(queue):
    app = QApplication(sys.argv)
    Application = QMainWindow()
    ui = Ui_Application()
    ui.setupUi(Application,queue)
    Application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    q=mp.Queue()
    p1 = mp.Process(target=main_data, args=(q,))
    p2 = mp.Process(target=main_appli, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()