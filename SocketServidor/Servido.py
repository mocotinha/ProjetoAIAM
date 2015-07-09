"""
Vers�o 0.1.0 - PRE-ALPHA - Projeto AIAM
Solu��o em socket, para receber informa��o do scanner e construir as telas de imagens

Autores: Allisson Alex (narokwq@gmail.com), Jozias Rolim (jozias.rolim@dce.ufpb.br)
"""

import socket
import cv2
import numpy as np

"""
Vari�veis
-----------------------------------------------------------------------------------------------------------------------------
HOST - Vari�vel constante que representa o ip do servidor, no caso o ip da maquina onde esse servidor est� rodando
PORT - Variavel constante que representa a porta do servudor, no caso a porta da maquina em que esse servidor est� rodando
tcp - nosso mecanismo de Socket para receber a conex�o, onde na fun��o passamos 2 argumentos, AF_INET que declara a fam�lia
do protocolo e  SOCKET_STREAM, indica que ser� TCP/IP.
orig - Tupla criada com IP e PORTA
con - objeto (informacao do socket em uso) recebido onde se encontra a mensagem enviada pelo cliente
cliente - Informa��es vindas do cliente pela rede, como ip e porta do cliente.
tela - vetor que representa a linha recebida
msg - mesagem recebida pelo socket, com buffer de 499
entrada - lista formada pelos elementos da msg
imagem - ndarray, array do numpy, criado a partir da lista recebida (entrada)
k - recebe a tecla digitada pelo usuario durante o processamento do video.
-----------------------------------------------------------------------------------------------------------------------------

"""

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig) #Vincular o socket ao ip e porta informado
tcp.listen(1) #Aguarda comunica��o
while True:
    con, cliente = tcp.accept() #Quando recebe um socket
    tela = []
    while True:
        msg = con.recv(499) #A mesagem � salva em msg, lida em um buffer de  499 bytes
        if not msg: break
        entrada = list(msg) #converte uma string em um vetor - EX: "ab" => ["a","b"]

        if len(tela) >= 200: #Exibe apenas quando ler 200 linhas
            tela.pop(0) #Remove a primeiro elemento do frame a ser exibido
            tela.append(entrada) #Adiciona uma linha ao frame no final
            imagem = np.array(tela,np.float32) #converte o vetor em um ndarray para ser exibido
            cv2.imshow("Imagem", imagem) #exibe a imagem com titulo da janela "Imagem", representada pelo ndarry imagem
            k = cv2.waitKey(1) & 0xff #Aguarda uma tecla ser preciosada em um tempo de 1s
            if k == 27: #Se esc for pressionada, para o processamento
                break

        else:
            tela.append(entrada) #adiciona uma linha ao vetor enquanto ele for menor que 200
    cv2.destroyAllWindows() #Destroi a tela de exibi��o do video
    con.close() # Fecha a conex�o com o socket