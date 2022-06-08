
#importe as bibliotecas
from base64 import encode
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
from funcoes_LPF import *
import soundfile as sf

def main():
    encode = signalMeu()    
    fs = 44100
    
    sd.default.samplerate = fs
    sd.default.channels = 2  
    duration = 3

    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    print('A captação começará em 5 segundos')
    #use um time.sleep para a espera
    time.sleep(5)
    #faca um print informando que a gravacao foi inicializada
    print('começou')
    
    numAmostras = duration*fs
    audio = sd.rec(int(numAmostras), fs, channels=1)
    sd.wait()
    print("...     FIM")
    
    # filtrando o audio
    t, sinal = encode.generateSin(13000, 1, duration, fs)
    y = audio[:,0]
    audioFiltrado = LPF(y,2500,fs)

    #emitindo som áudio filtrado
    print("Áudio filtrado no passa baixa")
    sd.play(audioFiltrado, fs)
    sd.wait()

    #modulando áudio com transmissora de 13.000Hz
    audioModulado = sinal*audioFiltrado
    
    #normalizando áudio (dividir pela amplitude)
    audioNormalizado = audioModulado/(np.max(np.abs(audioModulado)))
    
    #criando arquivo de áudio
    sf.write('arquivo.wav', audioNormalizado, fs)

    ##### GRÁFICOS #######

    # Áudio filtrado no domínio da frequência
    x,y = encode.calcFFT(audioFiltrado, fs)
    plt.figure(figsize=(25,10))
    plt.plot(x, y)
    plt.title(f'Sinal de áudio filtrado - domínio da frequência')
    plt.xlabel('Frequencies')
    plt.ylabel('Amplitude')
    plt.show()
    # Áudio filtrado no domínio do tempo
    plt.figure(figsize=(25,10))
    plt.plot(t, audioFiltrado)
    plt.title(f'Sinal de áudio - domínio do tempo')
    plt.xlabel('Tempo')
    plt.ylabel('Amplitude')
    plt.show()
    # Áudio modulado no domínio da frequencia
    x,y = encode.calcFFT(audioModulado, fs)
    plt.figure(figsize=(25,10))
    plt.plot(x, y)
    plt.title(f'Sinal de áudio modulado - domínio da frequência')
    plt.xlabel('Frequencies')
    plt.ylabel('Amplitude')
    plt.show()
    # Áudio modulado no domínio do tempo
    plt.figure(figsize=(25,10))
    plt.plot(t, audioModulado)
    plt.title(f'Sinal de áudio modulado - domínio do tempo')
    plt.xlabel('Tempo')
    plt.ylabel('Amplitude')
    plt.show()
    # Áudio normalizado no domínio da frequência
    x,y = encode.calcFFT(audioNormalizado, fs)
    plt.figure(figsize=(25,10))
    plt.plot(x, y)
    plt.title(f'Sinal de áudio normalizado - domínio da frequência')
    plt.xlabel('Frequencies')
    plt.ylabel('Amplitude')
    plt.show()



if __name__ == "__main__":
    main()
    
