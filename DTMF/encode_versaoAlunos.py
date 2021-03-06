
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)




def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # se voce quiser, pode usar a funcao de construção de senoides existente na biblioteca de apoio cedida. Para isso, você terá que entender como ela funciona e o que são os argumentos.
    # essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # o tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Seja razoável.
    # some as senoides. A soma será o sinal a ser emitido.
    # utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print("Inicializando encoder")
    print("Aguardando usuário")
    fs = 44100
    encode = signalMeu()
    tecla = input("Digite um número de entre 0 e 9, ou A, B, C, D, X, #: ")
    freq1, freq2 = encode.dict_teclas[str(tecla)][0], encode.dict_teclas[str(tecla)][1] 
    senoide1, senoide2 = encode.generateSin(freq1, 1, 5, fs)[1], encode.generateSin(freq2, 1, 5, fs)[1]
    t1, t2 = encode.generateSin(freq1, 1, 5, fs)[0], encode.generateSin(freq2, 1, 5, fs)[0]
    sinal = senoide1+senoide2
    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    #print("Gerando Tom referente ao símbolo : {}".format(NUM))
    sd.play(sinal, fs)
    
    
    # Exibe gráficos
    #plt.show()
    # aguarda fim do audio
    sd.wait()
    #plotFFT(self, signal, fs)
    
    # Exibe gráficos
    plt.figure(figsize=(25,10))
    plt.plot(t1, senoide1, label=f"Senoide 1")
    plt.plot(t2, senoide2, label=f"Senoide 2")
    plt.plot(t2, sinal, label="Soma das senoides")
    plt.title(f"Tecla {tecla}")
    plt.xlabel("Tempo (s)", fontsize = 18)
    plt.ylabel("Função Senoidal", fontsize = 18)
    plt.legend(loc='upper right', fontsize=18)
    plt.axis([1, 1.01, -2, 2])
    plt.show()
if __name__ == "__main__":
    main()
