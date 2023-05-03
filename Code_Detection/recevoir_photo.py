import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('192.168.135.223', 8888))

def recevoirImage():
    while True:
        sock.listen(5)
        client, address = sock.accept()
        print("connexion reçue")
        # we open a fichier (if it already exists, it is rewritten) to store all the bytes of the image in it
        # the first 8 bytes indicate the taille of the image
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

recevoirImage()
sock.close()