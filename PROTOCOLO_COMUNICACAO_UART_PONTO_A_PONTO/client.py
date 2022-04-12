#####################################################
# Camada Física da Computação
#Carareto
####################################################

#from tracemalloc import stop
from enlace import *
import time
import numpy as np
import sys
import math
from datetime import datetime

#   python -m serial.tools.list_ports

com1 = enlace('COM3')

class Client:

    def __init__(self, file, serialName):
        #self.clientCom = None
        self.serialName = serialName
        self.head = 0
        self.file = file
        self.eop = 0x00000000.to_bytes(4, byteorder="big")
        self.payloads = 0
        self.h0 = 0 # tipo de mensagem
        self.h1 = b'\x00' # livre
        self.h2 = b'\x00' # livre
        self.h3 = 0 # número total de pacotes do arquivo
        self.h4 = 0 # número do pacote sendo enviado
        self.h5 = 0 # se tipo for handshake:id do arquivo; se tipo for dados: tamanho do payload
        self.h6 = b'\x00' # pacote solicitado para recomeço quando há erro no envio.
        self.h7 = 0 # último pacote recebido com sucesso.
        self.h8 = b'\x00' # CRC
        self.h9 = b'\x00' # CRC
        self.logs = ''


    def iniciaCliente(self):
        self.clientCom = enlace(self.serialName)
        self.clientCom.enable()

    # Quebra a imagem nos payloads
    def criaPayloads(self):
        self.payloads = []
        for i in range(0, len(self.file), 114):
            self.payloads.append(self.file[i:i + 114])
        return self.payloads

    # Define o tipo da mensagem
    def tipoMensagem(self, n):
        self.h0 = (n).to_bytes(1, byteorder="big")
        # Mensagem do tipo Handshake
        if n == 1:
            self.h5 = b'\x00' # ? o que é o id do arquivo
        # Mensagem do tipo dados
        elif n == 3:
            self.h5 = len(self.payloads[int.from_bytes(self.h4,"big")-1])
            self.h5 = (self.h5).to_bytes(1, byteorder="big")

    def numeroMensagem(self,n):
        self.h4 = (n).to_bytes(1, byteorder="big")
        self.h7 = (n-1).to_bytes(1, byteorder="big")

    # Define a quantidade de pacotes que serão enviados
    def quantidaePacotes(self):
        tamanhoImagem = len(self.file)
        h3 = math.ceil(tamanhoImagem/114)
        self.h3 = (h3).to_bytes(1, byteorder="big")

    # Cria a composição do head
    def criaHead(self):
        self.head = self.h0+self.h1+self.h2+self.h3+self.h4+self.h5+self.h6+self.h7+self.h8+self.h9

    # Cria pacote  
    def criaPacote(self):
        return self.head + self.payloads[int.from_bytes(self.h4,"big") - 1] + self.eop

    # Checa o tempo máximo para a resposta do servidor
    def enviaEspera(self, pacote):
        timeMax = time.time()
        while True: 
            self.clientCom.sendData(pacote)
            self.criaLog(pacote, 'envio')
            time.sleep(.5)
            confirmacao = self.clientCom.getData(15)[0]
            timeF = time.time()
            if timeF - timeMax >= 25:
                print("Servidor não está respondendo. Cancelando comunicação.")
                break
            elif type(confirmacao) == str:
                print(confirmacao)
            else:
                return confirmacao

    # Realiza o handshake
    def handshake(self):
        payload = b'\x00'
        self.tipoMensagem(1)
        self.h3 = b'\x00'
        self.h4 = b'\x00'
        self.h7 = b'\x00'
        self.criaHead()
        pacote = self.head + payload + self.eop
        return self.enviaEspera(pacote)

    # Escreve os logs
    def criaLog(self, data, tipo):
        tempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tipoMsg = data[0]
        tamMsg = len(data)
        pacoteEnviado = data[4]
        totalPacotes = data[3]
        self.logs += f"{tempo} / {tipo} / {tipoMsg} / {tamMsg} / {pacoteEnviado} / {totalPacotes}\n"

    # Checa o tipo de mensagem na confirmação enviada pelo servidor
    def verificaMensagem(self, confirmacao):
        #typeMsg = int.from_bytes(confirmacao[0], "big")
        if confirmacao[0] == 4:
            self.criaLog(confirmacao, 'recebimento')
            print(confirmacao[7])
            print("O servidor recebeu o pacote !")
        else:
            self.criaLog(confirmacao, 'recebimento')
            numPacoteCorreto = confirmacao[7]
            print(f" Algo deu errado no envio, reenviar o pacote {numPacoteCorreto}")
            return numPacoteCorreto
        
    def escreveLog(self):
        with open(f'logs/logClient.txt', 'w') as f:
            f.write(self.logs)
    
    def finalizaClient(self):
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        self.clientCom.disable()
        exit()
                
            
serialName = "COM3"     
path = "img/nubank.png"  
file = open(path, 'rb').read()           

def main():
    try:
        # * INICIALIZANDO CLIENT
        cliente = Client(file, 'COM3')
        cliente.iniciaCliente()
        # * HANDSHAKE
        print("Iniciando HandShake\n")
        if cliente.handshake() is None:
            cliente.finalizaClient()
        print("Handshake realizado com sucesso! Servidor está pronto para o recebimento da mensagem.\n")
        # * ENVIO DOS PACOTES
        print("Início do envio dos pacotes\n")
        payloads = cliente.criaPayloads()
        # h3 = quantidade total de pacotes
        cliente.quantidaePacotes()
        # h4 = número do pacote sendo enviado
        h4 = 1
        # último pacote enviado com sucesso
        cont = 0
        while cont < int.from_bytes(cliente.h3, "big"):
            print(f"Enviando informações do pacote {h4}")
            cliente.numeroMensagem(h4)
            cliente.tipoMensagem(3)
            cliente.criaHead()
            pacote = cliente.criaPacote()
            confirmacao = cliente.enviaEspera(pacote)

            if confirmacao is None:
                cliente.finalizaClient()

            numPacote = cliente.verificaMensagem(confirmacao)
            if numPacote is None:
                if h4 == 2:
                    h4 += 2
                    cont +=1
                else:
                    h4 += 1
                    cont += 1
            else:
                h4 = numPacote
                cont = numPacote - 1

        cliente.escreveLog()
        # * FECHANDO CLIENT
        cliente.finalizaClient()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()