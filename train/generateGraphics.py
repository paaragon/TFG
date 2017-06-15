import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lib.SolarData import SolarData
from graphics import predict
import os
import json
import sys
from sklearn.metrics import mean_absolute_error

# Graficas para el dia 15/06/2016
normPath = 'graphics/train/reversenorm.json'

def getPredict(start, end, k, modelo, real):
    solarData = SolarData(start, end)

    df = pd.read_csv('data/csvWithCondition/' +
                     str(start) + str(end) + '.csv.orig')

    radiacion = list()

    horas = df['hora'].unique()
    for hora in horas:
        row = df.loc[df['hora'] == hora]
        index = row.index[0]
        prediction = predict.getPrediction(df, row, index, start, k, modelo)

        radiacion.append(prediction)

    newHoras = list()
    for h in horas:
        hAux = h / 100
        hAux += h % 100 / 60.0
        newHoras.append(hAux)

    print radiacion
    mse = round(mean_absolute_error(radiacion, real), 2)
    return plt.plot(newHoras, radiacion, label='modelo. MSE = ' + str(mse))


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


def getRealRadiation(start, end, model):
    df = pd.read_csv('data/csvWithCondition/' +
                     str(start) + str(end) + '.csv.orig')
    radiacion = list()

    horas = df['hora'].unique()
    for hora in horas:
        if model != 'mlp':
            radiacion.append(df[df['hora'] == hora]['radiacion'].mean())
        else:
            radiacion.append(mapRad(normalize(df[df['hora'] == hora]['radiacion'].mean())))

    newHoras = list()
    for h in horas:
        hAux = h / 100
        hAux += h % 100 / 60.0
        newHoras.append(hAux)

    dia = str(start % 100)
    mes = str(int(start % 10000) / 100)
    ano = str(start / 10000)
    return plt.plot(newHoras, radiacion, label='Radiacion ' + dia + '-' + mes + '-' + ano), radiacion


def getConservador(start, end, model, real):
    df = pd.read_csv('data/csvWithCondition/' +
                     str(start) + str(end) + '.csv.orig')
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

    mse = round(mean_absolute_error(radiacion, real), 2)
    return plt.plot(newHoras, radiacion, label='Cons. MSE = ' + str(mse))


def paintPlot(start, end, k, model):
    real = getRealRadiation(start, end, model)
    plot2, = real[0]
    plot3, = getConservador(start, end, model, real[1])
    plot1, = getPredict(start, end, k, model, real[1])
    plt.xlabel('Hora (0:24)')
    plt.ylabel('Radiacion')
    plt.legend(handles=[plot1, plot2, plot3])
    plt.savefig('graphics/' + model + '_' + str(start) + str(end) +  '.png')
    plt.show()


if __name__ == "__main__":

    print len(sys.argv)
    if len(sys.argv) < 5:
        print "Es necesario especificar los parametros."
        print "> start end k model"
        exit()

    start = int(sys.argv[1])
    end = int(sys.argv[2])
    k = int(sys.argv[3])
    model = sys.argv[4]
    paintPlot(start, end, k, model)
