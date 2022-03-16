from enlace import *
import time
from tqdm import tqdm

class Server:

    def __init__(self, porta= 'COM3',baudRate= 115200):
       self.idServer = 12
       self.idClient = 0
       self.porta = porta
       self.baudRate = baudRate
       self.eopEncoded = b'\x02\x05\x00\x07'
       self.rxBuffer = self.rxBufferLen = 0
       self.idArquivo = 0
       self.n_pacotes = 0
       self.pacotes = []

    def bufferDecodificado(self, buffer):
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

        if h0 == 1:
            self.n_pacotes = h3
            self.idArquivo = h5
            self.idClient = h1
            self.pacoteAnalisado = h4
            self.pacoteAtual = h4
            self.tamanhoPacoteAtual = h5
        elif h0 == 2:
            self.pacoteAtual = h4
            self.tamanhoPacoteAtual = h5
        
        return [h0,h1,h2,h3,h4,h5,h6,h7,h8,h9]

    def mudaHeader(self,header,posicao, valor):
        novo_valor = (valor).to_bytes(1, byteorder='big')
        novoHeader = header[:posicao]+novo_valor+header[posicao+1:]
        return novoHeader


    def handshakePrometido(self):

        print('Esperando Head Protocol...')
        rxBufferHeader, nRxHeaderLen = self.serverCom.getData(14)
        print('Tamanho do Head: {} bytes.'.format(nRxHeaderLen))
        header = self.bufferDecodificado(rxBufferHeader)
        
        if header[0]==1 and header[2]==self.idServer:
            print('Head Protocol recebido! Client ID: {}.'
            .format(self.idClient))
            newHeader = self.mudaHeader(rxBufferHeader,0,2)
            print('Enviando Handshake...\n')
            self.serverCom.sendData(newHeader)


    def integridadeArquivoBuffer(self,pacote):
        header = self.bufferDecoding(pacote)
        if pacote[-4:]==self.eopEncoded and header[4]== self.pacoteAnalisado+1:
            # print('sequencial',header[4])
            self.pacoteAnalisado=header[4]
            return True
        else:
            return False


    def receberArquivoBuffer(self):
        pbar = tqdm(total=self.n_pacotes,unit='bytes',unit_scale=128,
        desc='Bytes Recebidos')
        while len(self.pacotes)<self.n_pacotes:
            # print(len(self.pacotes),self.n_pacotes)
            self.serverCom.fisica.flush()
            rxBufferHeader, nRxHeaderLen = self.serverCom.getData(128)
            integridadeArquivoBuffer=self.integridadeArquivoBuffer(rxBufferHeader)

            responseBuffer = 0
            if integridadeArquivoBuffer:                
                respostaBuffer=self.mudaHeader(rxBufferHeader,0,4)
                self.pacotes.append(rxBufferHeader)
            else:
                responseBuffer=self.mudaHeader(rxBufferHeader,0,6)
            # print('RECEBIDO:',rxBufferHeader, len(self.pacotes))
            self.serverCom.sendData(responseBuffer)
            pbar.update(1)
        pbar.close()


    def startCommunication(self):
        self.handshakePrometido()
        self.receberArquivoBuffer()

    def decodificaArquivo(self):
        print('\nIniciando decodificação do arquivo recebido...')

        def limpaPacote(package):
            tamanhoPacote=self.bufferDecoding(package)[5]
            pacoteBuffer=package[10:-4][:tamanhoPacote]
            return pacoteBuffer

        arquivoBufferLimpo=[limpaPacote(i) for i in self.pacotes]
        buffer=bytes.join(b'',arquivoBufferLimpo)
        recebe_file=open('img/{}.png'.format(self.idArquivo),'wb')
        recebe_file.write(buffer)
        recebe_file.close()
        print('Arquivo {}.png (Size: {} bytes) criado em "files".'
        .format(self.idArquivo,len(buffer)))


    def finalizaConexao(self):
        print('\nFechando conexão com o cliente...')
        time.sleep(0.05)
        self.serverCom.sendData(self.pacotes[-1])
        print('Conexão fechada com client de ID: {}.'.format(self.idClient))
        self.rxBuffer = self.rxBufferLen = 0
        self.idArquivo = 0
        self.n_pacotes = 0
        self.pacotes = []
        self.pacoteAnalisado = 0
        self.pacoteAtual = 0
        self.tamanhoPacoteAtual = 0
        self.killProcess()


    def startServer(self):
        try:
            while True:
                self.serverCom = enlace(self.porta,self.baudRate)
                self.serverCom.enable()
                self.serverCom.fisica.flush()

                print("""
                --------------------------------
                ------Comunicação Iniciada------
                --------- Porta: {} ----------
                ------ Baud Rate: {} ------
                --------------------------------
                """.format(self.porta,self.baudRate))
                self.initialTime = time.time()

                print('Servidor aberto.')

                self.startCommunication()

                self.fileDecoding()

                self.closeConnection()
            
        except Exception as erro:
            print("Ops! Erro no Server! :-\\\n",erro)
            self.serverCom.disable()

        except KeyboardInterrupt:
            self.serverCom.disable()
            print('Server Finalizado na força!')


    def killProcess(self):
        print('Server Finalizado.')
        self.serverCom.fisica.flush()
        self.serverCom.disable()


def main():
    porta = input('Escolha a porta: (COM3, COM4,...): ')
    server = Server(porta)
    server.startServer()

if __name__ == "__main__":
    main()