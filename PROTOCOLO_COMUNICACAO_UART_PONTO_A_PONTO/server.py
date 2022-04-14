#####################################################
# Camada Física da Computação
#Carareto
####################################################

from enlace import *
import time
from datetime import datetime

#   python -m serial.tools.list_ports

class Server:
    def __init__(self, serialName):
        self.serialName = serialName
        self.logs = ''
        
serialName = "COM4"     

def main():
    try:
        # INICIANDO SERVER
        server = Server('COM4')
        server.serverCom = enlace(server.serialName)
        server.serverCom.enable()

        # INICIANDO HANDSHAKE
        print("Aguardando HandShake\n")
        pacote, lenPacote = server.serverCom.getData(15)
        # cria log
        tempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tipodaMensagem = pacote[0]
        tamanhoMensagem = len(pacote)
        pacEnviado = pacote[4]
        pacotesTotais = pacote[3]
        server.logs += f"{tempo} / {'recebimento'} / {tipodaMensagem} / {tamanhoMensagem} / {pacEnviado} / {pacotesTotais}\n"

        pacote = list(pacote)
        pacote = list(map(int, pacote))
        pacote[0] = 2
        respostaHandShake = b''
        for i in pacote:
            i = (i).to_bytes(1, byteorder="big")
            respostaHandShake += i
        
        print("Handshake recebido com sucesso! Reposta de estabilidade enviada.")
        server.serverCom.sendData(respostaHandShake)
        time.sleep(.5)

        # RECBER PACOTES
        # guarda informações
        data = b''
        numPacote = 1
        saida = b''
        while True:
            print(f"Número do pacote {numPacote}")
            # Recebendo o head
            head, lenHead = server.serverCom.getDataServer(10)
            lenPayload = head[5]
            payload_EOP, lenPayload_EOP = server.serverCom.getDataServer(lenPayload + 4)

            # verifica mensagem
            pacote = head + payload_EOP
            # cria log
            tempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tipodaMensagem = pacote[0]
            tamanhoMensagem = len(pacote)
            pacEnviado = pacote[4]
            pacotesTotais = pacote[3]
            server.logs += f"{tempo} / {'recebimento'} / {tipodaMensagem} / {tamanhoMensagem} / {pacEnviado} / {pacotesTotais}\n"

            head = pacote[0:10]
            h0, h1, h2, h3, h4, h5, h6, h7, h8, h9 = head[0], head[1], head[2], head[3], head[4], head[5], head[6], head[7], head[8], head[9]
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
                server.serverCom.sendData(respostaCorretaMsg + b'\x00' + 0x00000000.to_bytes(4, byteorder="big"))
                time.sleep(.5)

                if numPacote == h4:
                    numPacote += 1
                    data += payload_EOP[0:len(payload_EOP) - 4]                
                if numPacote == h3 + 1:
                    data += payload_EOP[0:len(payload_EOP) - 4]
                    break
            
            # verificando o local do EOP
            eop = pacote[len(pacote)-4:len(pacote)+1]
            if eop != 0x00000000.to_bytes(4, byteorder="big"):
                print(f"O eop está no local errado! Por favor reenvie o pacote {numPacote}")
                if numPacote == h4:
                    numPacote += 1
                    saida +=payload_EOP[0:len(payload_EOP) - 4]  
                    data += payload_EOP[0:len(payload_EOP) - 4]                
                if numPacote == h3 + 1:
                    saida += payload_EOP[0:len(payload_EOP) - 4]
                    data += payload_EOP[0:len(payload_EOP) - 4]
                    break   
            
            print("Está tudo certo com a mensagem! Enviando uma mensagem confirmando")
            h0 = 4
            h7 = numPacote
            confirmacao = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
            respostaCorretaMsg = b''
            for i in confirmacao:
                i = (i).to_bytes(1, byteorder="big")
                respostaCorretaMsg += i
            data = respostaCorretaMsg + b'\x00' + 0x00000000.to_bytes(4, byteorder="big")
            server.serverCom.sendData(data)
            tempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tipodaMensagem = data[0]
            tamanhoMensagem = len(data)
            pacEnviado = data[4]
            pacotesTotais = data[3]
            server.logs += f"{tempo} / {'envio'} / {tipodaMensagem} / {tamanhoMensagem} / {pacEnviado} / {pacotesTotais}\n"
            time.sleep(.5)
            if numPacote == h4:
                numPacote += 1 
                saida +=payload_EOP[0:len(payload_EOP) - 4]
                data += payload_EOP[0:len(payload_EOP) - 4]                
            if numPacote == h3 + 1:
                saida +=payload_EOP[0:len(payload_EOP) - 4]
                data += payload_EOP[0:len(payload_EOP) - 4]
                break  
                
        pathImageRx = "img/nubankCopia.png"
        f = open(pathImageRx, 'wb')
        f.write(saida)
        f.close()

        with open(f'logs/logServer.txt', 'w') as f:
            f.write(server.logs)
        # FINALIZANDO CLIENT
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        server.serverCom.disable()
        exit()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        server.serverCom.disable()
        exit()
        
if __name__ == "__main__":
    main()