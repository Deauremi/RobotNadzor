import pip
pip.main(["install", "pyserial"])
pip.main(["install", "keyboard"])

import serial
import socket
import multiprocessing as mp
import keyboard
import time
import socket, multiprocessing
import sys
import select


host="192.168.1.18"
host2 = '192.168.1.10'
port = 8040
nb_workers = 1
timeout_seconds = 15
running=True

def envoit_avant(ser) :
    ser.write(b"z")
    print("j'ai appuyee sur z")
    receive = ser.readline()
    print(receive.decode('ascii'))


def envoit_arriere(ser) :
    ser.write(b"s")
    print("j'ai appuyee sur s")
    receive = ser.readline()
    print(receive.decode('ascii'))


def envoit_droite(ser) :
    ser.write(b"d")
    print("j'ai appuyee sur d")
    receive = ser.readline()
    print(receive.decode('ascii'))
    
def envoit_gauche(ser) :
    ser.write(b"q")
    print("j'ai appuyee sur q")
    receive = ser.readline()
    print(receive.decode('ascii'))

def on_key_press(event):
    global running
    if event.name == 'esc':
        if running :
            print("Vous avez appuyé sur la touche 'Esc', le programme va s'éteindre.")
            running = False
            time.sleep(1)
            sys.exit()

keyboard.on_press(on_key_press)

def handle_connection(conn,q):
    with conn:
        conn.settimeout(timeout_seconds)
        buff = conn.recv(512)
        if buff:
            message = buff.decode('utf-8')
            print(message)
            q.put(message)


def main_uart(queue):
    ser = serial.Serial(port="COM8", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    while True:
        #ser.write(b"A")
        #receive = ser.readline()
        #print(receive.decode('ascii'))
        #time.sleep(1)
        item=queue.get()
        if item=="z":
            envoit_avant(ser)
        if item=="s":
            envoit_arriere(ser)
        if item=="q":
            envoit_gauche(ser)
        if item=="d":
            envoit_droite(ser)
    ser.close()

def main_server(queue):
    pool = multiprocessing.Pool(nb_workers)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        while running:
            ready_to_read, _, _ = select.select([s], [], [])

            if not ready_to_read:
                # No connection received within timeout period, exit the loop
                print("Pas de connection reçu dutant la période de timeout")
                break
                
            conn, address = s.accept()
            pool.apply_async(handle_connection, (conn,queue,))
    pool.close()
    pool.join()

if __name__ == '__main__':
    q=mp.Queue()
    p1 = mp.Process(target=main_server, args=(q,))
    p2 = mp.Process(target=main_uart, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()