from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from python.main import getGHI

def getRealRadiation():
    df = pd.read_csv('../../data/csvWithCondition/invierno20152016.csv')
    radiacion = list()

    horas = df['hora'].unique()
    for hora in horas:
        radiacion.append(df[df['hora'] == hora]['radiacion'].mean())

    newHoras = list()
    for h in horas:
        hAux = h / 100
        hAux += h % 100 / 60.0
        newHoras.append(hAux)

    return plt.plot(newHoras, radiacion, label='Invierno 2015')

def getModelRadiation(model, startDate = None, endDate = None): 
    if startDate == None:
        dias = np.arange(365)
    else:
        start = datetime.strptime(str(startDate), "%Y%m%d").timetuple().tm_yday
        end = datetime.strptime(str(endDate), "%Y%m%d").timetuple().tm_yday
        print str(start) + '-' + str(end)
        if start > end:
            dias = np.arange(end, start)
        else:
            dias = np.arange(start, end)
    horas = np.arange(0, 24, 1/60.0)
    ghi = np.zeros(shape=(len(horas), len(dias)))
    
    for h in range(len(horas)):
        for i, doy in enumerate(dias):
            print str(h)
            ghi[h][i] =  getGHI(doy,horas[h], model)

    meanGHI = np.zeros(shape=(len(horas)))
    for h in range(len(horas)):
        meanGHI[h] = ghi[h].mean()

    return plt.plot(horas, meanGHI, label=model)

if __name__ == "__main__":
   
    plot1, = getRealRadiation()
    plot2, = getModelRadiation('robledo', 20151221, 20160320)
    plot3, = getModelRadiation('kast', 20151221, 20160320)
    plot4, = getModelRadiation('adnot', 20151221, 20160320)
    plot5, = getModelRadiation('dpp', 20151221, 20160320)
    plt.xlabel('Hora (0:24)')
    plt.ylabel('Radiacion')
    plt.legend(handles=[plot1, plot2, plot3, plot4, plot5])
    plt.savefig('invierno2015.png')
    plt.show()


