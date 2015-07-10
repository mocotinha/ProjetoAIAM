"""
Versão 0.1.1 - PRE-ALPHA - Projeto AIAM
Solução em socket concorrente com threads, para receber informação do scanner e construir as telas de imagens, permite multiplas conexoes.

Autores: Allisson Alex (narokwq@gmail.com), Jozias Rolim (jozias.rolim@dce.ufpb.br)
"""

import socket
import thread
import numpy as np

"""
Variáveis
-----------------------------------------------------------------------------------------------------------------------------
HOST - Variável constante que representa o ip do servidor, no caso o ip da maquina onde esse servidor está rodando
PORT - Variavel constante que representa a porta do servudor, no caso a porta da maquina em que esse servidor está rodando
CONTAGEM_CONEXAO - representa o numero da conexao com o servidor
tcp - nosso mecanismo de Socket para receber a conexão, onde na função passamos 2 argumentos, AF_INET que declara a família
do protocolo e  SOCKET_STREAM, indica que será TCP/IP.
orig - Tupla criada com IP e PORTA
con - objeto (informacao do socket em uso) recebido onde se encontra a mensagem enviada pelo cliente
cliente - Informações vindas do cliente pela rede, como ip e porta do cliente.
tela - vetor que representa a linha recebida
msg - mesagem recebida pelo socket, com buffer de 499
entrada - lista formada pelos elementos da msg
imagem - ndarray, array do numpy, criado a partir da lista recebida (entrada)
k - recebe a tecla digitada pelo usuario durante o processamento do video.
telaNumero - representa o titulo da janela a ser exibida
-----------------------------------------------------------------------------------------------------------------------------
"""


HOST = '10.0.4.35'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
CONTAGEM_CONEXAO = 0

def conectado(con, cliente):
    import cv2
    print 'Conectado por', cliente
    tela = np.zeros((200,499), np.float32)
    telaNumero = "Conexao %s - IP: %s"%(CONTAGEM_CONEXAO,cliente[0])
    CONTAGEM_CONEXAO += 1
    while True:
        msg = con.recv(499) #A mesagem é salva em msg, lida em um buffer de  499 bytes
        if not msg: break
        entrada = list(msg) #converte uma string em um vetor - EX: "ab" => ["a","b"]
        
        tela = np.insert(tela, 0, entrada, 0) #Adiciona uma linha ao frame no final
        cv2.imshow(telaNumero, tela)#exibe a imagem com titulo da janela telaNumero, representada pelo ndarry imagem
        
        k = cv2.waitKey(1) & 0xff#Aguarda uma tecla ser preciosada em um tempo de 1s
        if k == 27:#Se esc for pressionada, para o processamento
            break
        
        tela = np.delete(tela,199,0)#Remove a primeiro elemento do frame a ser exibido

    print 'Finalizando conexao do cliente', cliente
    cv2.destroyAllWindows()#Destroi a tela de exibição do video
    con.close()# Fecha a conexão com o socket
    thread.exit()# Finaliza a Thread

if __name__ == "__main__":
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    orig = (HOST, PORT)

    tcp.bind(orig) #Vincular o socket ao ip e porta informado
    tcp.listen(1) #Aguarda comunicação

    while True:
        con, cliente = tcp.accept() #Quando recebe um socket
        thread.start_new_thread(conectado, tuple([con, cliente])) #Incia uma thread para conversação com o cliente especifico


    tcp.close() #Finaliza o socket
