import pandas as pd
import json
import os
from sklearn.externals import joblib
import numpy as np

k = 4
step = 15 # registros hacia atras para cada k
timeStep = 100 # cuanto tiempo hacia delante (una hora, HHMM)
modelPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../train/model.pkl')
normPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../train/reversenorm.json')

def getPrediction(recordsPath, ubication, date, hour, temperature, humidity, radiation):
    
    if not os.path.isfile(recordsPath):
        print "No records."
        return [0]

    columns = ['codigo', 'fecha', 'hora',
               'temperatura', 'humedad', 'radiacion']

    try:
        records = pd.read_csv(recordsPath, usecols=columns)

        if records.shape[0] < (k - 1) * step:
            print "No records enough."
            return [0]

        with open(normPath) as openfile:
            normData = json.load(openfile)

        dateNorm = normalize(date, normData['fecha'][0], normData['fecha'][1], normData['fecha'][2])
        predictData = [ubication, dateNorm]

        index = records.shape[0] - 1
        for i in range(k - 1):

            horaNorm = normalize(records.get_value(index, 'hora'), normData['hora'][0], normData['hora'][1], normData['hora'][2])
            predictData.append(horaNorm)

            tempNorm = normalize(records.get_value(index, 'temperatura'), normData['temperatura'][0], normData['temperatura'][1], normData['temperatura'][2])
            predictData.append(tempNorm)

            humNorm = normalize(records.get_value(index, 'humedad'), normData['humedad'][0], normData['humedad'][1], normData['humedad'][2])
            predictData.append(humNorm)

            radNorm = normalize(records.get_value(index, 'radiacion'), normData['radiacion'][0], normData['radiacion'][1], normData['radiacion'][2])
            predictData.append(radNorm)

            index -= step

        predictData.append(normalize(hour, normData['hora'][0], normData['hora'][1], normData['hora'][2]))
        predictData.append(normalize(temperature, normData['temperatura'][0], normData['temperatura'][1], normData['temperatura'][2]))
        predictData.append(normalize(humidity, normData['humedad'][0], normData['humedad'][1], normData['humedad'][2]))
        predictData.append(normalize(radiation, normData['radiacion'][0], normData['radiacion'][1], normData['radiacion'][2]))
        predictData.append(normalize(hour + timeStep, normData['hora'][0], normData['hora'][1], normData['hora'][2]))

        model = joblib.load(modelPath)

        prediction = model.predict(np.array(predictData).reshape(1, -1))
        predDenorm = denormalize(prediction, normData['radiacion'][0], normData['radiacion'][1], normData['radiacion'][2])

        return predDenorm
    except pd.io.EmptyDataError as err:
        print "No columns to parse from file"
        return [0]

def normalize(data, mean, mx, mn):

    if mx - mn == 0:
        return mx

    return (data - mean) / (mx - mn)


def denormalize(data, mean, mx, mn):

    return data * (mx - mn) + mean