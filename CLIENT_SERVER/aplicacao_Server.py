#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################

from enlace import *
import time
import numpy as np

#   python -m serial.tools.list_ports
serialName = "COM3"                  

def main():
    try:
        com1 = enlace('COM3')
        # Ativa comunicacao. Inicia os threads e a comunicação serial 
        com1.enable()
        print("esperando 1 byte de sacrifício")        
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        # Dando acesso aos bytes recebidos
        rxBuffer, nRx = com1.getData(2)
        # retorna um array de bytes
        rxBuffer_array = int.from_bytes(rxBuffer, "big")
        # transmite os dados
        com1.sendData(np.asarray(rxBuffer))
        # Dando acesso aos bytes recebidos em forma de array
        rxBuffer2, nRx2 = com1.getData(rxBuffer_array)
        rxLen = len(rxBuffer2)
        # Recebe a msg crua e splita ela com os separadores
        comandos = rxBuffer2.split(b'\xee')
        # Deleta o ultimo valor que é irrelevante
        del comandos[-1]


        com1.sendData(rxBuffer2)
        # tempo para executar o envio
        time.sleep(0.05) 
        # Retorna uma matriz de bytes representando um inteiro.
        txBufferLen = len(comandos).to_bytes(2, byteorder="big")
        com1.sendData(txBufferLen)

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        
    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
