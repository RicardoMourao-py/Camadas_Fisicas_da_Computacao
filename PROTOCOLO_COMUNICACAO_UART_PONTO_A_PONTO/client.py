#####################################################
# Camada Física da Computação
#Carareto
####################################################

from enlace import *
import time
import math
from datetime import datetime

#   python -m serial.tools.list_ports

com1 = enlace('COM3')

class Client:

    def __init__(self, file, serialName):
        self.head = 0
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
        self.payloads = 0
        self.eop = 0x00000000.to_bytes(4, byteorder="big")
        self.serialName = serialName
        self.file = file
        self.logs = ''            
            
serialName = "COM3"     
path = "img/nubank.png"  
file = open(path, 'rb').read()          

def main():
    try:
        # INICIANDO CLIENT
        cliente = Client(file, 'COM3')
        cliente.clientCom = enlace(cliente.serialName)
        cliente.clientCom.enable()
        # INICIANDO HANDSHAKE
        print("Inicia HandShake\n")
        payload = b'\x00'
        # verifica o tipo da mensagem
        tipo = 1
        cliente.h0 = (tipo).to_bytes(1, byteorder="big")
        # Mensagem do tipo Handshake
        if tipo == 1:
            cliente.h5 = b'\x00' 
        # Mensagem do tipo dados
        elif tipo == 3:
            cliente.h5 = len(cliente.payloads[int.from_bytes(cliente.h4,"big")-1])
            cliente.h5 = (cliente.h5).to_bytes(1, byteorder="big")
        cliente.h3 = b'\x00'
        cliente.h4 = b'\x00'
        cliente.h7 = b'\x00'
        # criando o head
        cliente.head = cliente.h0+cliente.h1+cliente.h2+cliente.h3+cliente.h4+cliente.h5+cliente.h6+cliente.h7+cliente.h8+cliente.h9
        pacote = cliente.head + payload + cliente.eop
        # Envia e Espera
        timeMax = time.time()
        while True: 
            cliente.clientCom.sendData(pacote)
            # criando o log
            tempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tipodaMensagem = pacote[0]
            tamanhoMensagem = len(pacote)
            pacEnviado = pacote[4]
            pacotesTotais = pacote[3]
            cliente.logs += f"{tempo} / {'envio'} / {tipodaMensagem} / {tamanhoMensagem} / {pacEnviado} / {pacotesTotais}\n"
            time.sleep(.5)
            confirmacao = cliente.clientCom.getData(15)[0]
            timeF = time.time()
            if timeF - timeMax >= 25:
                print(confirmacao)
                print("Servidor não responde. Cancelando protocolo.")
                confirmacao = None
                break
            elif type(confirmacao) == str:
                print(confirmacao)
            else:
                break
            
        if confirmacao is None:
            print("-------------------------")
            print("Comunicação encerrada")
            print("-------------------------")
            cliente.clientCom.disable()
            exit()

        print("Handshake realizado com sucesso!\n")
        # ENVIANDO PACOTES
        print("Iniciando envio dos pacotes\n")
        # criando payloads
        cliente.payloads = []
        for i in range(0, len(cliente.file), 114):
            cliente.payloads.append(cliente.file[i:i + 114])
        
        # quantidade de pacotes
        tamanhoImagem = len(cliente.file)
        h3 = math.ceil(tamanhoImagem/114)
        cliente.h3 = (h3).to_bytes(1, byteorder="big")
        h4 = 1
        # último pacote enviado com sucesso
        cont = 0
        while cont < int.from_bytes(cliente.h3, "big"):
            print(f"Enviando informações do pacote {h4}")
            # numero da mensagem 
            cliente.h4 = (h4).to_bytes(1, byteorder="big")
            cliente.h7 = (h4-1).to_bytes(1, byteorder="big")
            # tipo da mensagem 
            tipo = 3
            cliente.h0 = (tipo).to_bytes(1, byteorder="big")
            # Mensagem do tipo Handshake
            if tipo == 1:
                cliente.h5 = b'\x00' 
            # Mensagem do tipo dados
            elif tipo == 3:
                cliente.h5 = len(cliente.payloads[int.from_bytes(cliente.h4,"big")-1])
                cliente.h5 = (cliente.h5).to_bytes(1, byteorder="big")
            # criando head
            cliente.head = cliente.h0+cliente.h1+cliente.h2+cliente.h3+cliente.h4+cliente.h5+cliente.h6+cliente.h7+cliente.h8+cliente.h9
            # criando pacote
            pacote = cliente.head + cliente.payloads[int.from_bytes(cliente.h4,"big") - 1] + cliente.eop
            # envia e espera
            timeMax = time.time()
            while True: 
                cliente.clientCom.sendData(pacote)
                time.sleep(.5)
                # criando o log
                tempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                tipodaMensagem = pacote[0]
                tamanhoMensagem = len(pacote)
                pacEnviado = pacote[4]
                pacotesTotais = pacote[3]
                cliente.logs += f"{tempo} / {'envio'} / {tipodaMensagem} / {tamanhoMensagem} / {pacEnviado} / {pacotesTotais}\n"
                confirmacao = cliente.clientCom.getData(15)[0]
                timeF = time.time()
                if timeF - timeMax >= 25:
                    print(f"Servidor não responde. Cancelando protocolo.")
                    confirmacao = None
                    break
                elif type(confirmacao) == str:
                    print(confirmacao)
                else:
                    break

            if confirmacao is None:
                print("-------------------------")
                print("Comunicação encerrada")
                print("-------------------------")
                cliente.clientCom.disable()
                exit()
            
            # verificando mensagem
            if confirmacao[0] == 4:
                # criando log
                tempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                tipodaMensagem = confirmacao[0]
                tamanhoMensagem = len(confirmacao)
                pacEnviado = confirmacao[4]
                pacotesTotais = confirmacao[3]
                numPacoteCorreto = confirmacao[7]+1
                cliente.logs += f"{tempo} / {'recebimento'} / {tipodaMensagem} / {tamanhoMensagem} / {pacEnviado} / {pacotesTotais}\n"
                print('-----------------------------------')
                
                # CASO DE ERRO
                # numPacoteCorreto = None
                print("O servidor recebeu o pacote !")
                
            else:
                # criando log
                tempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                tipodaMensagem = confirmacao[0]
                tamanhoMensagem = len(confirmacao)
                pacEnviado = confirmacao[4]
                pacotesTotais = confirmacao[3]
                cliente.logs += f"{tempo} / {'recebimento'} / {tipodaMensagem} / {tamanhoMensagem} / {pacEnviado} / {pacotesTotais}\n"
                numPacoteCorreto = confirmacao[7]
                print(f" Envio não verificado,por favor, reenvie o pacote {numPacoteCorreto}")
                
            if numPacoteCorreto is None:
                if h4 == 2:
                    h4 += 2
                    cont +=1
                else:
                    h4 += 1
                    cont += 1
            else:
                
                h4 = numPacoteCorreto
                cont = numPacoteCorreto - 1

        # escreve arquivo log
        with open(f'logs/logClient.txt', 'w') as f:
            f.write(cliente.logs)
        # FINALIZANDO CLIENT
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        cliente.clientCom.disable()
        exit()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        
if __name__ == "__main__":
    main()