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
serialName = "COM4" 
'''             
O client deve sortear um número N entre 10 e 30, que irá determinar a quantidades de comandos a serem
enviados. Em seguida deve construir uma lista contendo os N comandos. Esta lista deve conter os comandos de 1 a 6
em uma sequência também aleatória, desconhecida pelo server e elaborada aleatoriamente pelo client. 
'''

def main():
    try:
        com1 = enlace('COM4')
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1) 
        # lista de comandos existentes
        lista = [b'\xF0', b'\xFF', b'\x00\xFF', b'\xFF\x00', b'\x00', b'\x0F']
        # A sequência deve ter entre 10 e 30 comandos, a ser determinada pelo client (aleatoriamente)
        quant_comandos = random.randint(10,30)
        lista_comandos = []
        for i in range(quant_comandos):
            indice_aleatorio_lista = random.randint(0,5)
            lista_comandos.append(lista[indice_aleatorio_lista])
        # lista de msg com os items separados por byte xee'
        msg_txBuffer = []
        for i in lista_comandos:
            msg_txBuffer.append(i+b'\xee')
        txBuffer = (b''.join(msg_txBuffer))
        txLen = len(txBuffer)
        txBuffer_bytes = txLen.to_bytes(2, byteorder = 'big')
        # Envia lista de bytes
        com1.sendData(txBuffer_bytes)
        # recebe em binário
        rxBuffer, nRx = com1.getData(2)

        if txBuffer_bytes == rxBuffer:
            print('Comunicação iniciada!')
            
            com1.sendData((txBuffer)) 

            rxBuffer, nRx = com1.getData(txLen)

            if rxBuffer == txBuffer:
                print('Informação Enviada = Informação recebida!')
            else:
                print('Informações enviadas e recebidas diferentes')

            n_comandos = len(lista_comandos).to_bytes(2, byteorder="big")
            n_comandos_recebidos, nRx = com1.getData(2)
            len_n_comandos_recebidos = int.from_bytes(n_comandos_recebidos, "big")
            print('Número de Comandos Enviados: {} comandos'.format(len(lista_comandos)))
            print('Número de Comandos Recebidos: {} comandos'.format(len_n_comandos_recebidos)) 
            
            if n_comandos == n_comandos_recebidos:
                print('Número de comandos Enviados = Número de comandos Recebidos')
            else:
                print('Número de comandos Enviados != Número de comandos Recebidos')

            print("-------------------------------")
            print("Comunicação encerrada")
            print("-------------------------------")
            
        else:
            print('Sem comunicação!')

        com1.disable()

        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
