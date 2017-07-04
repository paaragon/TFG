import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lib.SolarData import SolarData
from graphics import predict
import os
import json
import sys
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import accuracy_score

import gtk

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

# Graficas para el dia 15/06/2016
normPath = 'graphics/train/reversenorm.json'


def getPredict(start_date, end_date, start_hour, end_hour, k, modelo, real):

    solarData = SolarData(start_date, end_date, start_hour, end_hour)

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

    if modelo != 'mlp':
        mae = round(mean_absolute_error(radiacion, real), 2)
        return plt.plot(newHoras, radiacion, label='modelo. MAE = ' + str(mae))
    else:
        mae = round(accuracy_score(real, radiacion, normalize=False), 2)
        return plt.plot(newHoras, radiacion, label='modelo. ACC = ' + str(mae))


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
    df = pd.read_csv('data/csvWithCondition/' + str(start) + str(end) + '.csv.orig')
    radiacion = list()

    horas = df['hora']
    x_axis = list()

    for index, hora in enumerate(horas):
        record = df[(df['hora'] == hora) & (df['fecha'] == df['fecha'].loc[index])]
        if model != 'mlp':
            radiacion.append(record['radiacion'].mean())
        else:
            radiacion.append(mapRad(normalize(record['radiacion']).mean()))

        hAux = hora / 100
        hAux += hora % 100 / 60.0

        date = df['fecha'].loc[index]
        x = date + hAux
        print x, record['radiacion'].values[0]
        x_axis.append(x)


    return plt.plot(x_axis, radiacion, label='Radiacion ' + str(start) + '-' + str(end)), radiacion


def getConservador(start, end, model, real):
    df = pd.read_csv('data/csvWithCondition/' +
                     str(start) + str(end) + '.csv.orig')
    radiacion = list()

    horas = df['hora']
    for index, hora in enumerate(horas):
        #if hora >= 200:
        if model != 'mlp':
            radiacion.append(df[df['hora'] == hora - 100]['radiacion'])
        else:
            radiacion.append(
                mapRad(normalize(df[df['hora'] == hora - 100]['radiacion'])))
        #else:
        #    radiacion.append(0)

    newHoras = list()
    for h in horas:
        hAux = h / 100
        hAux += h % 100 / 60.0
        newHoras.append(hAux)

    if model != 'mlp':
        mse = round(mean_absolute_error(real, radiacion), 2)
        return plt.plot(newHoras, radiacion, label='Cons. MAE = ' + str(mse))
    else:
        mse = round(accuracy_score(real, radiacion, normalize=False), 2)
        return plt.plot(newHoras, radiacion, label='Cons. ACC = ' + str(mse))


def paintPlot(start, end, k, model):
    real = getRealRadiation(start, end, model)
    plot2, = real[0]
    #plot3, = getConservador(start, end, model, real[1])
    #plot1, = getPredict(start, end, k, model, real[1])
    plt.xlabel('Fecha y Hora')
    plt.ylabel('Radiacion')
    #plt.legend(handles=[plot1, plot2, plot3])
    plt.legend(handles=[plot2])
    plt.savefig('graphics/' + model + '_' + str(start) + str(end) + '.png')
    plt.show()


if __name__ == "__main__":

    if len(sys.argv) < 5:
        print "Es necesario especificar los parametros."
        print "> start_date end_date start_hour end_hour k model"
        exit()

    start = int(sys.argv[1])
    end = int(sys.argv[2])
    k = int(sys.argv[3])
    model = sys.argv[4]
    print model
    paintPlot(start, end, k, model)
