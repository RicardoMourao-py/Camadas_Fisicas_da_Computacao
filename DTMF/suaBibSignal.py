
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window



class signalMeu:
    def __init__(self):
        self.dict_teclas = {'0': (1339, 941),'1': (1206, 697),'2': (1339, 697),'3': (1477, 697),'4': (770, 1206),'5': (770, 1339),
                            '6': (770, 1477),'7': (852, 1206),'8': (852, 1339),'9': (852, 1477),'A': (1633, 697),'B': (1633, 770),
                            'C': (1633, 852),'D': (1633, 941),'X': (1206, 941),'#': (1477, 941)}

    def generateSin(self, freq, amplitude, time, fs):
        n = time*fs
        x = np.linspace(0.0, time, n)
        s = amplitude*np.sin(freq*x*2*np.pi)
        return (x, s)

    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs):
        x,y = self.calcFFT(signal, fs)
        plt.figure()
        plt.plot(x, np.abs(y))
        plt.title('Fourier')
