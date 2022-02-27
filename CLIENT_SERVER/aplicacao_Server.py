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
        inicio_total = time.time()
        com1 = enlace('COM3')
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        rxBuffer, nRx = com1.getData(2)
        rxBuffer_resposta = int.from_bytes(rxBuffer, "big")
        
        inicio_transmissao = time.time()
        com1.sendData(np.asarray(rxBuffer))
        final_transmissao = time.time()
       
        rxBuffer2, nRx2 = com1.getData(rxBuffer_resposta)
        rxLen = len(rxBuffer2)

        comandos = rxBuffer2.split(b'\xee')
        del comandos[-1]

        com1.sendData(rxBuffer2)

        time.sleep(0.05)
        txBufferLen = len(comandos).to_bytes(2, byteorder="big")
        com1.sendData(txBufferLen)

        final_total = time.time()
        
        variacao_final = final_total - inicio_total
        variacao_transmissao = final_transmissao - inicio_transmissao

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print(f'Tempo Total: {variacao_final}')
        print(f'Tempo de Transmissão: {variacao_transmissao}')
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
