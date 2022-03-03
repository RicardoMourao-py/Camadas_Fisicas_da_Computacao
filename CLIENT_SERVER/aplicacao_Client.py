#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


from enlace import *
import time
import numpy as np
import random 

#   python -m serial.tools.list_ports
serialName = "COM3" 
'''             
O client deve sortear um número N entre 10 e 30, que irá determinar a quantidades de comandos a serem
enviados. Em seguida deve construir uma lista contendo os N comandos. Esta lista deve conter os comandos de 1 a 6
em uma sequência também aleatória, desconhecida pelo server e elaborada aleatoriamente pelo client. 
'''

def main():
    try:
        com1 = enlace('COM3')
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        lista = [b'\xF0', b'\xFF', b'\x00\xFF', b'\xFF\x00', b'\x00', b'\x0F']
        quant_comandos = random.randint(10,30)
        lista_comandos = []
        for i in range(quant_comandos):
            indice_aleatorio_lista = random.randint(0,5)
            lista_comandos.append(lista[indice_aleatorio_lista])

        msg_txBuffer = []
        for i in lista_comandos:
            msg_txBuffer.append(i+b'\xee')
        txBuffer = (b''.join(msg_txBuffer))
        txLen = len(txBuffer)
        txBuffer_bytes = txLen.to_bytes(2, byteorder = 'big')

        com1.sendData(txBuffer_bytes)
        rxBuffer, nRx = com1.getData(2)

        print("recebeu {}" .format(rxBuffer))
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
