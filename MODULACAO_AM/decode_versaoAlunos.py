#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas

from email.mime import audio
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import peakutils
import soundfile as sf
from funcoes_LPF import *

def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)
    decode = signalMeu()    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs = 44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = fs
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = 3#tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    #lendo arquivo de áudio gerado pelo encode
    audio, samplerate = sf.read('arquivo.wav')

    #emitindo som áudio gerado pelo encode
    print("áudio modulado")
    sd.play(audio, fs)
    sd.wait()

    #demodulando áudio com transmissora de 13.000Hz
    print("Demodulando áudio\n")
    sinal = decode.generateSin(13000, 1, duration, fs)[1]
    audioDemodulado = sinal*audio    

    
    #filtrando frequências superiores a 2.500Hz
    print("Filtrando passa baixa\n")
    audioFiltrado = LPF(audioDemodulado, 2500, fs)

    print("Reproduz áudio demodulado e filtrado")
    sd.play(audioFiltrado, fs)
    sd.wait()

    ##### GRÁFICOS #######
    x,y = decode.calcFFT(audioDemodulado, fs)
    plt.figure(figsize=(25,10))
    plt.plot(x, y)
    plt.title(f'Sinal de áudio demodulado - domínio da frequência')
    plt.xlabel('Frequencies')
    plt.ylabel('Amplitude')
    plt.show()

    x,y = decode.calcFFT(audioFiltrado, fs)
    plt.figure(figsize=(25,10))
    plt.plot(x, y)
    plt.title(f'Sinal de áudio filtrado - domínio da frequência')
    plt.xlabel('Frequencies')
    plt.ylabel('Amplitude')
    plt.show()
    
if __name__ == "__main__":
    main()
