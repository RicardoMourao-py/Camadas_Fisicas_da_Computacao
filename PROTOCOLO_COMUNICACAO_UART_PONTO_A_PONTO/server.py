#####################################################
# Camada Física da Computação
#Carareto
####################################################

from tracemalloc import stop
from urllib import response
from xmlrpc import server

from pandas import array
from enlace import *
import time
import numpy as np
import time
from datetime import datetime


#   python -m serial.tools.list_ports

class Server:
    def __init__(self, serialName):
        self.serialName = serialName
        self.logs = ''
        
    def iniciaServidor(self):
        self.serverCom = enlace(self.serialName)
        self.serverCom.enable()

    def recebeDados(self,n):
        return self.serverCom.getDataServer(n)

    def sendData(self, data):
        self.serverCom.sendData(data)

    def recebeHandShake(self,n):
        pacote, lenPacote = self.serverCom.getData(n)
        self.criaLog(pacote, 'recebimento')
        pacote = list(pacote)
        pacote = list(map(int, pacote))
        pacote[0] = 2
        respostaHandShake = b''
        for i in pacote:
            i = (i).to_bytes(1, byteorder="big")
            respostaHandShake += i
        return respostaHandShake, lenPacote


    # fraciona o head para identificar cada componente presente
    def fracionaHead(self, pacote):
        head = pacote[0:10]
        h0 = head[0] # tipo de mensagem
        h1 = head[1] # livre
        h2 = head[2] # livre
        h3 = head[3] # número total de pacotes do arquivo
        h4 = head[4] # número do pacote sendo enviado
        h5 = head[5] # se tipo for handshake:id do arquivo; se tipo for dados: tamanho do payload
        h6 = head[6] # pacote solicitado para recomeço quando a erro no envio.
        h7 = head[7] # último pacote recebido com sucesso.
        h8 = head[8] # CRC
        h9 = head[9] # CRC
        return h0, h1, h2, h3, h4, h5, h6, h7, h8, h9

    def verificaMensagem(self, pacote, numPacote):
        self.criaLog(pacote, 'recebimento')
        h0, h1, h2, h3, h4, h5, h6, h7, h8, h9 = self.fracionaHead(pacote)
        # Checando se o número do pacote enviado está correto
        if h4 != numPacote:
            print(f"O número do pacote está errado! Por favor reenvie o pacote {numPacote}")
            h0 = 6
            h7 = numPacote
            confirmacao = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
            respostaCorretaMsg = b''
            for i in confirmacao:
                i = (i).to_bytes(1, byteorder="big")
                respostaCorretaMsg += i
            self.serverCom.sendData(respostaCorretaMsg + b'\x00' + 0x00000000.to_bytes(4, byteorder="big"))
            time.sleep(.5)
            return h4, h3

        # Checando se o EOP está no local correto
        eop = pacote[len(pacote)-4:len(pacote)+1]
        if eop != 0x00000000.to_bytes(4, byteorder="big"):
            print(f"O eop está no local errado! Por favor reenvie o pacote {numPacote}")
            return h4, h3
        
        print("Está tudo certo com a mensagem! Vamos enviar uma mensagem de confirmação.")
        h0 = 4
        h7 = numPacote
        confirmacao = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
        respostaCorretaMsg = b''
        for i in confirmacao:
            i = (i).to_bytes(1, byteorder="big")
            respostaCorretaMsg += i
        self.serverCom.sendData(respostaCorretaMsg + b'\x00' + 0x00000000.to_bytes(4, byteorder="big"))
        self.criaLog(respostaCorretaMsg + b'\x00' + 0x00000000.to_bytes(4, byteorder="big"), 'envio')
        time.sleep(.5)
        return h4, h3

    # Escreve os logs
    def criaLog(self, data, tipo):
        tempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tipoMsg = data[0]
        tamMsg = len(data)
        pacoteEnviado = data[4]
        totalPacotes = data[3]
        self.logs += f"{tempo} / {tipo} / {tipoMsg} / {tamMsg} / {pacoteEnviado} / {totalPacotes}\n"
        
    def escreveLog(self):
        with open(f'logs/logServer.txt', 'w') as f:
            f.write(self.logs)

    def finalizaServidor(self):
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        self.serverCom.disable()
        exit()
        
serialName = "COM4"     

def main():
    try:
        
        # * INICIALIZANDO SERVER
        server = Server('COM4')
        server.iniciaServidor()

        # * HANDSHAKE
        print("Esperando HandShake\n")
        pacote, lenPacote = server.recebeHandShake(15)
        print("Handshake recebido com sucesso! Enviando reposta de estabilidade.")
        server.sendData(pacote)
        time.sleep(.5)

        # * RECEBIMENTO DOS PACOTES
        # Variável para armazenar as informações recolhidas
        data = b''
        numPacote = 1
        while True:
            print(f"Recebendo informações do pacote {numPacote}")
            # Recebendo o head
            head, lenHead = server.recebeDados(10)
            lenPayload = head[5]
            payload_EOP, lenPayload_EOP = server.recebeDados(lenPayload + 4)
            numPacoteRecebido, h3 = server.verificaMensagem(head + payload_EOP, numPacote)
            if numPacote == numPacoteRecebido:
                numPacote += 1
                data += payload_EOP[0:len(payload_EOP) - 4]                
            if numPacote == h3 + 1:
                data += payload_EOP[0:len(payload_EOP) - 4]
                break     

        pathImageRx = "img/nubankCopia.png"
        f = open(pathImageRx, 'wb')
        f.write(data)
        f.close()

        server.escreveLog()
        # * FECHANDO CLIENT
        server.finalizaServidor()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        server.finalizaServidor()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()