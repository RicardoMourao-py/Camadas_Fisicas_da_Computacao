#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


from pickle import TRUE
from enlace import *
import time
import os 
from tqdm import tqdm

#   python -m serial.tools.list_ports

'''             
O client deve sortear um número N entre 10 e 30, que irá determinar a quantidades de comandos a serem
enviados. Em seguida deve construir uma lista contendo os N comandos. Esta lista deve conter os comandos de 1 a 6
em uma sequência também aleatória, desconhecida pelo server e elaborada aleatoriamente pelo client. 
'''
class Client:
    def __init__(self, nome_arquivo, porta= 'COM4', baudRate= 115200):
        self.idServer = 12
        self.idClient = 14
        self.nome_arquivo = nome_arquivo
        self.baudRate = baudRate
        self.porta = porta
        # Sequência de bytes conhecida para ser possível a identificação
        self.eopEncoded = b'\x02\x05\x00\x07'
        self.txBuffer = self.txBufferLen = 0
        self.pacotes = []
        self.n_pacotes = 0
    
    def header(self,tipoDeMensagem:int,numeroDoPacote:int,tamanhoPacote:int=1):
        '''
        h0 – tipo de mensagem
        h1 – id do cliente
        h2 – id do servidor
        h3 – número total de pacotes do arquivo
        h4 – número do pacote sendo enviado
        h5 – se tipo for handshake:id do arquivo||se tipo for dados: tamanho do payload
        h6 – pacote solicitado para recomeço quando a erro no envio.
        h7 – último pacote recebido com sucesso.
        h8 – h9 – CRC
        '''
        h0 = (tipoDeMensagem).to_bytes(1,byteorder="big")
        h1 = (self.idClient).to_bytes(1,byteorder="big")
        h2 = (self.idServer).to_bytes(1,byteorder="big")
        h3 = (self.n_pacotes).to_bytes(1,byteorder="big")
        h4 = (numeroDoPacote).to_bytes(1,byteorder="big")
        h5 = (tamanhoPacote).to_bytes(1,byteorder="big")
        h6 = (0).to_bytes(1,byteorder="big")
        h7 = (0).to_bytes(1,byteorder="big")
        h8 = (0).to_bytes(1,byteorder="big")
        h9 = (0).to_bytes(1,byteorder="big")

        return h0+h1+h2+h3+h4+h5+h6+h7+h8+h9
        
    def codificaBuffer(self):
        # quociente da divisão dividido por 114 por conta do payload
        n_pacotes = self.txBufferLen//114
        # numero total de pacotes na transmissão não se altera
        if self.txBufferLen%114==0:
            self.n_pacotes = n_pacotes  
        # se resto é diferente de 0, significa que vai para o próximo pacote
        else: 
            self.n_pacotes = n_pacotes+1
        
        id_arquivo=int(self.nome_arquivo.split('.')[0])
        header = self.header(1,0,id_arquivo)+self.eopEncoded
        self.pacotes.append(header)            
            
        pacotes_arquivo = []
        for i in range(0,self.txBufferLen,114):
            pacotes_arquivo.append(self.txBuffer[i:i+114])

        def pacote_codificado(i:int):
            body = pacotes_arquivo[i]
            header = self.header(3,i+1,len(body))
            
            if len(body)!=114:
                body=body+ (0).to_bytes(114-len(body), byteorder="big")

            return header+body+self.eopEncoded

        pacotes_arquivoEncoded = [] 
        for i in range(0,len(pacotes_arquivo)):
            pacotes_arquivoEncoded.append(pacote_codificado(i))
            
        self.pacotes = self.pacotes+pacotes_arquivoEncoded
    
    def mandaHandshake(self, i):
        transmissaoHeader= True
        while transmissaoHeader:
            self.clientCom.sendData(i)
            
            print('Aguardando Handshake...')
            rxBuffer, nRx = self.clientCom.getData(14,5)
            if not rxBuffer[0]:
                tente_novamente = input("\n\nServidor inativo. Tentar novamente? s/n: ")
                if tente_novamente == 's':
                    transmissaoHeader = True
                elif tente_novamente == 'n':
                    transmissaoHeader = False
                    return False
            else:
                transmissaoHeader = False
                if rxBuffer[0] == 2 and rxBuffer[1:] == i[1:]:
                    print('Handshake concluído com sucesso! Server ID: {}'.format(rxBuffer[2]))
                    return True
                else:
                    print('Handshake mal sucedido...')
                    return False

    def mudaHeader(self,header,posicao, valor):
        novo_valor = (valor).to_bytes(1, byteorder='big')
        novoHeader = header[:posicao]+novo_valor+header[posicao+1:]
        return novoHeader
    
    def bufferDecodificado(self, buffer):
        h0 = buffer[0]
        h1 = buffer[1]
        h2 = buffer[2]
        h3 = buffer[3]
        h4 = buffer[4]
        h5 = buffer[5]
        h6 = buffer[6]
        h7 = buffer[7]
        h8 = buffer[8]
        h9 = buffer[9]
        
        return [h0,h1,h2,h3,h4,h5,h6,h7,h8,h9]

    def mandaPacote(self, package, id):
        # print('\nEnviando pacote: {}/{}'.format(index,len(self.packages)))
        self.clientCom.fisica.flush()
        pacote_nao_enviado=True
        while pacote_nao_enviado:
            self.clientCom.sendData(package)
            rxBuffer, nRx = self.clientCom.getData(len(package),5)

            if not rxBuffer[0]:
                intervalo_pacote = self.mudaHeader(package,0,5)
                self.clientCom.sendData(intervalo_pacote)
                tente_novamente = input("Servidor inativo. Tentar novamente? s/n: ")
                if tente_novamente == 's':
                    return False
                elif tente_novamente == 'n':
                    self.mataProcesso()

            header = self.bufferDecodificado(rxBuffer)
            if rxBuffer[1:] == package[1:] and header[0]==4:
                # print('RECEBIDO OK')
                pacote_nao_enviado=False
                return package

    def mataProcesso(self):
        print('Client Finalizado.')
        self.clientCom.fisica.flush()
        self.clientCom.disable()

    def iniciaTransmissao(self):
        atualPacote = permanecePacote = []
        handshake_verifica = False
        pbar = tqdm(total=self.n_pacotes,unit='packages',desc='Pacotes Enviados:')
        for i, pacote in enumerate(self.pacotes):
            atualPacote = pacote
            if pacote == self.pacotes[0]:  
                print('\nEnviando início do protocolo...')
                handshakeResposta = self.mandaHandshake(pacote)
                if handshakeResposta:
                    permanecePacote = pacote
                    handshake_verifica=True
                else:
                    self.mataProcesso()

            if handshake_verifica and pacote != self.pacotes[0]:
                response = self.mandaPacote(pacote,i)
                permanecePacote = response
                pbar.update(1)
        pbar.close()


    def finalizaConexao(self):
        print('\nAguardando confirmação de recebimento...')
        rxBuffer, nRx = self.clientCom.getData(len(self.pacotes[-1]))
        if rxBuffer==self.pacotes[-1]:
            print('Todos os pacotes foram recebidos com sucesso.')
        else:
            print('Erro ao enviar todos os arquivos...')
        self.mataProcesso() 

    def iniciaClient(self):
        try:
            self.clientCom = enlace(self.porta,self.baudRate)
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
    arquivo = os.listdir('img')
    client = Client(arquivo[0], 'COM4')
    client.iniciaClient()
    
if __name__ == "__main__":
    main()
