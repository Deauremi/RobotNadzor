# coding: utf-8

"""import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("", 1111))

print("Le nom du fichier que vous voulez récupérer:")
file_name = input("test.txt") # utilisez raw_input() pour les anciennes versions python
s.send(file_name.encode())
file_name = 'data/%s' % (file_name,)
r = s.recv(9999999)
with open(file_name,'wb') as _file:
    _file.write(r)
print("Le fichier a été correctement copié dans : %s." % file_name)"""

import socket,multiprocessing
import keyboard
import sys
import select
import time

host = "192.168.106.122"
host2= "192.168.106.21"
port = 8000
nb_workers = 1
timeout_seconds = 15
running=True

def on_key_press(event):
    global running
    if event.name == 'esc':
        if running : 
            print("Vous avez appuyé sur la touche 'Esc', le programme va s'éteindre.")
            running = False
            time.sleep(1)
            sys.exit()
    if event.name == 'u':
        envoie()

keyboard.on_press(on_key_press)

def handle_connection(conn):
    with conn:
        conn.settimeout(timeout_seconds)
        buff = conn.recv(512)
        if buff:
            message = buff.decode('utf-8')
            print(message)

def envoie():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_envoie:
        s_envoie.connect((host, port))
        s_envoie.send("test".encode('utf-8'))

if __name__ == '__main__':
    pool = multiprocessing.Pool(nb_workers)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host2, port))
        s.listen(1)
        s.setblocking(False)
        while running:
            try:
                conn, address = s.accept()
                pool.apply_async(handle_connection, (conn,))
            except socket.error:
                pass
    pool.close()
    pool.join()