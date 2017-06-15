
import pandas as pd
import json
import os
from sklearn.externals import joblib
import numpy as np

step = 1  # registros hacia atras para cada k
timeStep = 100  # cuanto tiempo hacia delante (una hora, HHMM)


def mapRad(rad):
    return int(((rad + 1) / 2) * 100)

def getPrediction(df, row, index, start, k, model):

    modelPath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'train/' + str(model) + '.pkl')

    normPath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'train/reversenorm.json')

    if index < (k - 1) * step:
        print "No records enough."
        return 0

    with open(normPath) as openfile:
        normData = json.load(openfile)

    date2015 = 20150000 + (start % 10000)
    dateNorm = normalize(
        date2015, normData['fecha'][0], normData['fecha'][1], normData['fecha'][2])
    predictData = [row['codigo'], dateNorm]

    now = row['hora']
    for i in range(k - 1):

        horaNorm = normalize(df.get_value(
            index, 'hora'), normData['hora'][0], normData['hora'][1], normData['hora'][2])
        predictData.append(horaNorm)

        tempNorm = normalize(df.get_value(index, 'temperatura'),
                             normData['temperatura'][0], normData['temperatura'][1], normData['temperatura'][2])
        predictData.append(tempNorm)

        humNorm = normalize(df.get_value(
            index, 'humedad'), normData['humedad'][0], normData['humedad'][1], normData['humedad'][2])
        predictData.append(humNorm)

        radNorm = normalize(df.get_value(index, 'radiacion'), normData['radiacion'][0], normData['radiacion'][1], normData['radiacion'][2])
        
        if model == 'mlp':
            radNorm = mapRad(radNorm)
        
        predictData.append(radNorm)

        index -= step

    predictData.append(normalize(
        row['hora'], normData['hora'][0], normData['hora'][1], normData['hora'][2]))

    predictData.append(normalize(row['temperatura'], normData['temperatura']
                                 [0], normData['temperatura'][1], normData['temperatura'][2]))
    predictData.append(normalize(
        row['humedad'], normData['humedad'][0], normData['humedad'][1], normData['humedad'][2]))

    radNorm = normalize(row['radiacion'], normData['radiacion'][0], normData['radiacion'][1], normData['radiacion'][2])
    if model == 'mlp':
        radNorm = mapRad(radNorm)

    predictData.append(radNorm)
    
    predictData.append(normalize(
        row['hora'] + timeStep, normData['hora'][0], normData['hora'][1], normData['hora'][2]))

    model = joblib.load(modelPath)

    prediction = model.predict(np.array(predictData).reshape(1, -1))

    if model != 'mlp':
        predDenorm = denormalize(prediction, normData['radiacion'][0], normData['radiacion'][1], normData['radiacion'][2])
        return predDenorm[0]
    else:
        return prediction


def normalize(data, mean, mx, mn):

    if mx - mn == 0:
        return mx

    return (data - mean) / (mx - mn)


def denormalize(data, mean, mx, mn):

    return data * (mx - mn) + mean
