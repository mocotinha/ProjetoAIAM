# -*- coding: utf-8 -*-
"""
Versão 0.1.2 - ALPHA - Projeto AIAM
Solução em socket concorrente com threads, para receber informação do scanner e construir as telas de imagens, permite multiplas conexoes.

Autores: Allisson Alex (narokwq@gmail.com), Jozias Rolim (jozias.rolim@dce.ufpb.br)
"""

import socket
import thread
import cv2
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
VETOR_PECAS - representa os dados que serão persistidos no banco de dados
QTD_PECAS - representa a quantidades de peças que passaram na esteira desde o inicio
TESTE_PASSAGEM_PECA - representa valor 0 ou 1, representando se a peça esta sendo lida na esteira ou não
AREA_TOTAL - representa a area total das peças lidas
AREA_PECA_ATUAL - representa a area da pela que passou no scanner
-----------------------------------------------------------------------------------------------------------------------------
"""


HOST = 'localhost'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta


def conectado(con, cliente, CONTAGEM_CONEXAO):

    print 'Conectado por', cliente
    tela = np.zeros((350,499), np.float32)
    telaNumero = "Conexao %s - IP: %s"%(CONTAGEM_CONEXAO,cliente[0])
    CONTAGEM_CONEXAO += 1
    VETOR_PECAS = []
    QTD_PECAS = 0
    TESTE_PASSAGEM_PECA = 0
    AREA_TOTAL = 0
    AREA_PECA_ATUAL = 0


    while True:
        msg = con.recv(499) #A mesagem é salva em msg, lida em um buffer de  499 bytes
        if not msg: break
        entrada = list(msg) #converte uma string em um vetor - EX: "ab" => ["a","b"]
        area = sum(map(int,entrada))

        if TESTE_PASSAGEM_PECA == 0 and area > 0:#Verifica se existe a leitura de pelo menos um pixel 1 e se anteriormente não passava peça

            TESTE_PASSAGEM_PECA = 1
        elif TESTE_PASSAGEM_PECA == 1 and area == 0:#Verifica se a peça acabou de passar
            VETOR_PECAS.append(["Peça de numero: ",QTD_PECAS, "Com area total de (em pixel):",AREA_PECA_ATUAL])
            TESTE_PASSAGEM_PECA = 0
            QTD_PECAS+=1
            AREA_TOTAL += AREA_PECA_ATUAL
            AREA_PECA_ATUAL = 0

        if TESTE_PASSAGEM_PECA == 1:#Somatoria das leituras da peça
            AREA_PECA_ATUAL += area


        tela = np.insert(tela, 100, entrada, 0) #Adiciona uma linha ao frame no final
        tela[:100,:] = np.zeros((100,499))
        cv2.putText(tela,"Quantidade de Pecas : %d"%QTD_PECAS,(3,30),cv2.FONT_HERSHEY_SIMPLEX,1,(220,0,0),2,5)#Adiciona o texto ao frame
        cv2.putText(tela,"Area Total: %d"%AREA_TOTAL,(3,60),cv2.FONT_HERSHEY_SIMPLEX,1,(220,0,0),2,5)#Adiciona o texto ao frame
        cv2.imshow(telaNumero, tela)#exibe a imagem com titulo da janela telaNumero, representada pelo ndarry imagem
        
        k = cv2.waitKey(1) & 0xff#Aguarda uma tecla ser preciosada em um tempo de 1s
        if k == 27:#Se esc for pressionada, para o processamento
            break
        
        tela = np.delete(tela,349,0)#Remove a primeiro elemento do frame a ser exibido

    print VETOR_PECAS
    print 'Finalizando conexao do cliente', cliente
    cv2.destroyAllWindows()#Destroi a tela de exibição do video
    con.close()# Fecha a conexão com o socket
    thread.exit()# Finaliza a Thread

if __name__ == "__main__":
    CONTAGEM_CONEXAO = 0
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    orig = (HOST, PORT)

    tcp.bind(orig) #Vincular o socket ao ip e porta informado
    tcp.listen(1) #Aguarda comunicação

    while True:
        con, cliente = tcp.accept() #Quando recebe um socket
        CONTAGEM_CONEXAO += 1
        thread.start_new_thread(conectado, tuple([con, cliente, CONTAGEM_CONEXAO])) #Incia uma thread para conversação com o cliente especifico


    tcp.close() #Finaliza o socket
