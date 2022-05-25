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

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


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


    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    print('A captação começará em 5 segundos')
    #use um time.sleep para a espera
    time.sleep(5)
    #faca um print informando que a gravacao foi inicializada
    print('começou')
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = duration*fs
    audio = sd.rec(int(numAmostras), fs, channels=1)
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    y = audio[:,0] # informações de onda

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    #t = np.linspace(inicio,fim,numPontos)

    # plot do gravico  áudio vs tempo!
   
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = decode.calcFFT(y, fs)
    #plt.figure("F(y)")
    #plt.plot(xf,yf)
    #plt.grid()
    #plt.title('Fourier audio')
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   

    index = peakutils.indexes(np.abs(yf), thres=0.2, min_dist=100) # encontra os indices numericos dos picos


    picos_teclas = np.unique(list(decode.dict_teclas.values())) # 6
    
    dic = {}
    for freq in xf[index]:
        print(freq)
        distancias = []
        for pico_tecla in picos_teclas:
            delta = np.abs(freq - pico_tecla)
            distancias.append(delta)

        x = distancias.index(min(distancias))
        dic[picos_teclas[x]] = min(distancias)



    cont = 0
    tom = []    
    for i in sorted(dic, key = dic.get):
        if cont == 2:
            break
        tom.append(i)
        cont+=1

    print(tom)
    
    
    for i in decode.dict_teclas.keys():
        if decode.dict_teclas[i] == (tom[0], tom[1]) or decode.dict_teclas[i] == (tom[1], tom[0]):
            print(f'Sua tecla é: {i}')
            tecla = i

    x = np.linspace(0.0, duration, numAmostras)
    plt.figure(figsize=(25,10))
    
    plt.plot(x, audio)
    plt.title('Áudio Gravado')
    plt.xlabel('Tempo')
    plt.ylabel('Amplitude')
    #plt.xlim(0,1500)
    plt.show()
    #printe os picos encontrados! 
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
    
    x,y = decode.calcFFT(audio[:,0], fs)
    plt.figure(figsize=(25,10))
    plt.plot(x, y)
    plt.title(f'Tecla: {tecla}')
    plt.xlabel('Frequencias')
    plt.ylabel('Transformada')
    #plt.xlim(0,1500)
    #plt.axis([0, 1500, 0, 0.0001])
    plt.show()
    ## Exibe gráficos
    #plt.show()

if __name__ == "__main__":
    main()
