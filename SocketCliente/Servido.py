
import socket
import cv2
import numpy as np
from matplotlib import pyplot as plt

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)
while True:
    con, cliente = tcp.accept()
    tela = []
    while True:
        msg = con.recv(499)
        if not msg: break
        entrada = list(msg)
        if len(tela) >= 200:
            tela.pop(0)
            tela.append(entrada)
            imagem = np.array(tela,np.float32)
            cv2.imshow("Imagem", imagem)
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break

        else:
            tela.append(entrada)
    cv2.destroyAllWindows()
    con.close()