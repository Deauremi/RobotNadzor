import socket,multiprocessing
import keyboard
import sys
import select
import time



host = "192.168.61.21"
host2= "192.168.61.223"
port = 8040
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall("test".encode('utf-8'))
        buff = s.recv(512)
        print(buff.decode())


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