import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lib.SolarData import SolarData
from graphics import predict
import os
import json

# Graficas para el dia 15/06/2016
normPath = 'graphics/train/reversenorm.json'
def getPredict():
    solarData = SolarData(20161015, 20161015)

    df = pd.read_csv('data/csvWithCondition/2016101520161015.csv.orig')

    radiacion = list()

    horas = df['hora'].unique()
    for hora in horas:
        row = df.loc[df['hora'] == hora]
        index = row.index[0]
        prediction = predict.getPrediction(df, row, index)

        radiacion.append(prediction)
        print prediction

    newHoras = list()
    for h in horas:
        hAux = h / 100
        hAux += h % 100 / 60.0
        newHoras.append(hAux)

    return plt.plot(newHoras, radiacion, label='MLP')

def mapRad(rad):
    return int(((rad + 1) / 2) * 100)

def normalize(rad):
    with open(normPath) as openfile:
        normData = json.load(openfile)

    mean = normData['hora'][0]
    mx = normData['hora'][1]
    mn = normData['hora'][2]

    if mx - mn == 0:
        return mx

    return (rad - mean) / (mx - mn)

def getRealRadiation():
    df = pd.read_csv('data/csvWithCondition/2016101520161015.csv.orig')
    radiacion = list()

    horas = df['hora'].unique()
    for hora in horas:
        radiacion.append(df[df['hora'] == hora]['radiacion'].mean())
        #radiacion.append(mapRad(normalize(df[df['hora'] == hora]['radiacion'].mean())))

    newHoras = list()
    for h in horas:
        hAux = h / 100
        hAux += h % 100 / 60.0
        newHoras.append(hAux)

    return plt.plot(newHoras, radiacion, label='15-01-206')

def getConservador():
    df = pd.read_csv('data/csvWithCondition/2016101520161015.csv.orig')
    radiacion = list()

    horas = df['hora'].unique()
    for hora in horas:
        if hora <= 2300:
            radiacion.append(df[df['hora'] == hora + 100]['radiacion'].mean())
        else:
            radiacion.append(0)

    newHoras = list()
    for h in horas:
        hAux = h / 100
        hAux += h % 100 / 60.0
        newHoras.append(hAux)

    return plt.plot(newHoras, radiacion, label='Modelo conservador')

def paintPlot():
    plot1, = getConservador()
    plot2, = getRealRadiation()
    plt.xlabel('Hora (0:24)')
    plt.ylabel('Radiacion')
    #plt.legend(handles=[plot1, plot2, plot3, plot4, plot5])
    plt.legend(handles=[plot1, plot2])
    plt.savefig('graphics/20161015_conservador.png')
    plt.show()

if __name__ == "__main__":
    paintPlot()