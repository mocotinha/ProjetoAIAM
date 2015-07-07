import socket
import sys

HOST = 'localhost'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

arquivo = sys.stdin.readlines()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
print 'Para sair use CTRL+X\n'

for i in arquivo:
    tcp.send (i[:-1])

tcp.close()
