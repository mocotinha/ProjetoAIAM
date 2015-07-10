
import socket
import cv2
import numpy as np
import time
from matplotlib import pyplot as plt

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)
while True:
    con, cliente = tcp.accept()
    tela = np.zeros((200,499), np.float32)
    while True:
        start = time.clock()
        msg = con.recv(499)
        if not msg: break
        entrada = list(msg)
        tela = np.insert(tela, 0, entrada, 0)
        cv2.imshow("Imagem", tela)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
        tela = np.delete(tela,199,0)
        end = time.clock()
        print "%f\n"%(end-start,)
    cv2.destroyAllWindows()
    con.close()