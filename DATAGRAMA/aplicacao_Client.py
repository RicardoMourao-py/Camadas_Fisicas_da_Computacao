#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


from enlace import *
import time
import os 

#   python -m serial.tools.list_ports
serialName = "COM4" 
'''             
O client deve sortear um número N entre 10 e 30, que irá determinar a quantidades de comandos a serem
enviados. Em seguida deve construir uma lista contendo os N comandos. Esta lista deve conter os comandos de 1 a 6
em uma sequência também aleatória, desconhecida pelo server e elaborada aleatoriamente pelo client. 
'''
class Client:
    def __init__(self, nome_arquivo, porta= 'COM4'):
        self.idServidor = 13
        self.idClient = 9
        self.nome_arquivo = nome_arquivo
        self.porta = porta
        # Sequência de bytes conhecida para ser possível a identificação
        self.eopEncoded = b'\x02\x05\x00\x07'
        self.txBuffer = self.txBufferLen = 0
        self.packages = []
        self.n_pacotes = 0
    
    def codificaBuffer():
    
    def iniciaTransmissao():

    def finalizaConexao():

    def iniciaClient(self):
        try:
            self.clientCom = enlace(self.serialName,self.baudRate)
            self.clientCom.enable()

            print("Comunicação Iniciada na porta: {}".format(self.porta))

            self.initialTime = time.time()

            arquivo = open("img/{}".format(self.nome_arquivo),"rb")
            self.txBuffer=arquivo.read()
            self.txBufferLen=len(self.txBuffer)
            arquivo.close()

            print("""- Arquivo a ser enviado: {}. Tamanho: {} bytes.
            """.format(self.nome_arquivo,self.txBufferLen))

            print('Criando buffer para envio...')

            self.codificaBuffer()

            self.iniciaTransmissao()

            self.finalizaConexao()
            
            self.clientCom.disable()

        except Exception as erro:
            print("Ops! Erro no Client! :-\\\n",erro)
            self.clientCom.disable()

        except KeyboardInterrupt:
            self.clientCom.disable()
            print('Client Finalizado na força!')
        
def main():        
    # arquivos = os.listdir('NOME_DA PASTA/SEND_PASTA')
    # for i,value in enumerate(arquivos):
    #     print('{} - {}'.format(i, value))
    # seleciona_arquivo = int(input('Qual Arquivo? '))
    # seleciona_porta = input('Qual a porta? ')
    # client = Client(arquivos[seleciona_arquivo], seleciona_porta)
    
if __name__ == "__main__":
    main()
