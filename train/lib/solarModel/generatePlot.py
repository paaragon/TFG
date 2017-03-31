import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from python.main import getGHI

def getRealRadiation():
    df = pd.read_csv('../../data/csvWithCondition/2015010120151231NN.csv')
    radiacion = list()

    horas = df['hora'].unique()
    for hora in horas:
        radiacion.append(df[df['hora'] == hora]['radiacion'].mean())

    newHoras = list()
    for h in horas:
        hAux = h / 100
        hAux += h % 100 / 60.0
        newHoras.append(hAux)

    return plt.plot(newHoras, radiacion, label='Radiacion 2015')

def getModelRadiation(model):
    
    dias = np.arange(365)
    horas = np.arange(0, 24, 1/60.0)
    ghi = np.zeros(shape=(len(horas), len(dias)))
    
    for h in range(len(horas)):
        for doy in dias:
            print str(h)
            ghi[h][doy] =  getGHI(doy,horas[h], model)

    meanGHI = np.zeros(shape=(len(horas)))
    for h in range(len(horas)):
        meanGHI[h] = ghi[h].mean()

    return plt.plot(horas, meanGHI, label=model)

if __name__ == "__main__":
    '''
    df = pd.read_csv('../../data/csvWithCondition/2015010120151231NN.csv')
    radiacion = list()

    horas = df['hora'].unique()
    for hora in horas:
        radiacion.append(df[df['hora'] == hora]['radiacion'].mean())

    plt.plot(horas, radiacion)
    plt.show()
    '''
    plot1, = getRealRadiation()
    plot2, = getModelRadiation('robledo')
    plot3, = getModelRadiation('kast')
    plot4, = getModelRadiation('adnot')
    plot5, = getModelRadiation('dpp')
    plt.xlabel('Hora (0:24)')
    plt.ylabel('Radiacion')
    plt.legend(handles=[plot1, plot2, plot3, plot4, plot5])
    plt.savefig('foo.png')
    plt.show()


