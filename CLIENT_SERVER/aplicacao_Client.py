#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################

from distutils import command
from email import message
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
        inicio_total = time.time()
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
        
        inicio_transmissao = time.time()
        com1.sendData(np.asarray(txBuffer))
        final_transmissao = time.time()
        
        txLen = len(txBuffer)
        inicio_recebimento = time.time()
        rxBuffer, nRx = com1.getData(txLen)
        final_recebimento = time.time()
        print("recebeu {}" .format(rxBuffer))
        
        # f = open(imageW, 'wb')
        # f.write(rxBuffer) 
        # f.close()
    
        final_total = time.time()
        
        variacao_final = final_total - inicio_total
        variacao_transmissao = final_transmissao - inicio_transmissao
        variacao_recebimento = final_recebimento - inicio_recebimento

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print(f'Tempo Total: {variacao_final}')
        print(f'Tempo de Transmissão: {variacao_transmissao}')
        print(f'Tempo de Recebimento: {variacao_recebimento}')
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
