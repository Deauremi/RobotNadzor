# coding: utf-8 

import socket, multiprocessing
import keyboard
import sys
import select
import time

host = '192.168.243.122'
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

keyboard.on_press(on_key_press)

def handle_connection(conn):
    with conn:
        buff = conn.recv(512)
        message = buff.decode('utf-8')
        conn.sendall(f"echo : {message}".encode('utf-8'))


if __name__ == '__main__':
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
            pool.apply_async(handle_connection, (conn,))
    pool.close()
    pool.join()