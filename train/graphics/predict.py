
import pandas as pd
import json
import os
from sklearn.externals import joblib
import numpy as np

k = 3
step = 1 # registros hacia atras para cada k
timeStep = 100 # cuanto tiempo hacia delante (una hora, HHMM)
modelPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'train/mlp.pkl')
normPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'train/reversenorm.json')

def mapRad(rad):
    return int(((rad + 1) / 2) * 100)

def getPrediction(df, row, index):

    if index < (k - 1) * step:
        print "No records enough."
        return 0

    with open(normPath) as openfile:
        normData = json.load(openfile)

    date2015 = 20151015
    dateNorm = normalize(date2015, normData['fecha'][0], normData['fecha'][1], normData['fecha'][2])
    predictData = [row['codigo'], dateNorm]
    
    now = row['hora']
    for i in range(k - 1):

        horaNorm = normalize(df.get_value(index, 'hora'), normData['hora'][0], normData['hora'][1], normData['hora'][2])
        predictData.append(horaNorm)

        tempNorm = normalize(df.get_value(index, 'temperatura'), normData['temperatura'][0], normData['temperatura'][1], normData['temperatura'][2])
        predictData.append(tempNorm)

        humNorm = normalize(df.get_value(index, 'humedad'), normData['humedad'][0], normData['humedad'][1], normData['humedad'][2])
        predictData.append(humNorm)

        #radNorm = normalize(df.get_value(index, 'radiacion'), normData['radiacion'][0], normData['radiacion'][1], normData['radiacion'][2])
        rMapped = mapRad(df.get_value(index, 'radiacion')) 
        #predictData.append(radNorm)
        predictData.append(rMapped)

        index -= step
    
    predictData.append(normalize(row['hora'], normData['hora'][0], normData['hora'][1], normData['hora'][2]))
    predictData.append(normalize(row['temperatura'], normData['temperatura'][0], normData['temperatura'][1], normData['temperatura'][2]))
    predictData.append(normalize(row['humedad'], normData['humedad'][0], normData['humedad'][1], normData['humedad'][2]))
    #predictData.append(normalize(row['radiacion'], normData['radiacion'][0], normData['radiacion'][1], normData['radiacion'][2]))
    
    radMapped = mapRad(row['radiacion'])
    print radMapped
    predictData.append(radMapped)
    predictData.append(normalize(row['hora'] + timeStep, normData['hora'][0], normData['hora'][1], normData['hora'][2]))

    model = joblib.load(modelPath)

    prediction = model.predict(np.array(predictData).reshape(1, -1))
    #predDenorm = denormalize(prediction, normData['radiacion'][0], normData['radiacion'][1], normData['radiacion'][2])

    print '----prediccion: ', prediction

    #return predDenorm[0]
    return prediction

def normalize(data, mean, mx, mn):

    if mx - mn == 0:
        return mx

    return (data - mean) / (mx - mn)


def denormalize(data, mean, mx, mn):

    return data * (mx - mn) + mean