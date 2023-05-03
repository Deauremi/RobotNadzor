import pip
pip.main(["install", "pyserial"])
pip.main(["install", "keyboard"])

import serial
import keyboard
import time

def envoit_avant() :
    ser.write(b"z")
    print("j'ai appuyee sur z")
    receive = ser.readline()
    print(receive.decode('ascii'))
    while keyboard.is_pressed('z') :
        continue 

def envoit_arriere() :
    ser.write(b"s")
    print("j'ai appuyee sur s")
    receive = ser.readline()
    print(receive.decode('ascii'))
    while keyboard.is_pressed('s') :
        continue

def envoit_droite() :
    ser.write(b"d")
    print("j'ai appuyee sur d")
    receive = ser.readline()
    print(receive.decode('ascii'))
    while keyboard.is_pressed('d') :
        continue
    
def envoit_gauche() :
    ser.write(b"q")
    print("j'ai appuyee sur q")
    receive = ser.readline()
    print(receive.decode('ascii'))
    while keyboard.is_pressed('q') :
        continue

    
ser = serial.Serial(port="COM8", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

while True:
    #ser.write(b"A")
    #receive = ser.readline()
    #print(receive.decode('ascii'))
    #time.sleep(1)
    
    if keyboard.is_pressed('z'):
        envoit_avant()
        
    if keyboard.is_pressed('s'):
        envoit_arriere()

    if keyboard.is_pressed('q'):
        envoit_gauche()

    if keyboard.is_pressed('d'):
        envoit_droite()

        
ser.close()



    
