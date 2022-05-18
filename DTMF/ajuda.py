import numpy as np
import peakutils

dicio = {'0': (1339, 941),'1': (1206, 697),'2': (1339, 697),'3': (1477, 697),'4': (770, 1206),'5': (770, 1339),
                            '6': (770, 1477),'7': (852, 1206),'8': (852, 1339),'9': (852, 1477),'A': (1633, 697),'B': (1633, 770),
                            'C': (1633, 852),'D': (1633, 941),'X': (1206, 941),'#': (1477, 941)}

index = peakutils.indexes(np.abs(yf), thres=0.8, min_dist=20) # encontra os indices numericos dos picos
print("index de picos {}" .format(index))
distancias = []
picos_teclas = np.unique(list(decode.dict_teclas.values())) # 6

for pico in [415 107342 109746 110425]:
    for pico_tecla in picos_teclas:
        distancias.append(np.abs(pico-pico_tecla))

freq1 = picos_teclas[distancias.index(min(distancias))]
del list(picos_teclas)[distancias.index(min(distancias))]
freq2 = picos_teclas[distancias.index(min(distancias))]

for i in dicio.keys():
    if dicio[i] == (freq1, freq2) or dicio[i] == (freq2, freq1):
        print(f'Sua tecla é: {i}')