#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 15:03:10 2016

@author: Abel, Maria, Pablo
"""

from infoRiegoData import csvManager as cM
<<<<<<< HEAD
from sklearn.model_selection import cross_val_score
from sklearn import linear_model
import pandas as pd
import os.path
import generateY as y
import generateX as x


conditions = dict()
conditions['dateStart'] = 20150601
conditions['dateEnd'] = 20150930
conditions['hourStart'] = 800
conditions['hourEnd'] = 2000
conditions['ubication'] = ['Nava de Arevalo']

#cM.createCSVWithConditions('data/csvFiles/', 'data/filteredFile.csv', conditions)
=======
import pandas
from sklearn import svm
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import linear_model
from sklearn.model_selection import KFold

conditions = dict()
conditions['dateStart'] = 20010601
conditions['dateEnd'] = 20010605
conditions['hourStart'] = 1900
conditions['hourEnd'] = 1900
conditions['ubication'] = ['Nava de Arevalo']

cM.createCSVWithConditions('data/csvFiles/',\
                           'data/filteredFile.csv',\
                           conditions)
>>>>>>> b40cf697f14f61f4bbed84f582dd6e185e21854a

conditionsX = dict()
conditionsX['relativeTargetSample'] = 2
conditionsX['nSamples'] = 4
#x.generateDataFrame('data/filteredFile.csv','data/x.csv', conditionsX)

<<<<<<< HEAD
conditionsY = dict()
#y.generateDataFrame('data/filteredFile.csv', 'data/x.csv', 'data/y.csv')

dfX = pd.read_csv('data/x.csv')
dfY = pd.read_csv('data/y.csv')

dfX['fecha'] = [item.replace('-', '') for item in dfX['fecha']]

for i, codigo in enumerate(dfX['codigo'].unique()):
    dfX.loc[dfX['codigo'] == codigo, 'codigo'] = i


alg = linear_model.LinearRegression()
cv = 3

scores = cross_val_score(alg, dfX, dfY, cv = cv)

columns = ['dateStart',\
           'dateEnd',\
           'hourStart',\
           'hourEnd',\
           'ubicacion',\
           'relativeTargetSample',\
           'nSamples',\
           'alg',\
           'cv',\
           'mean',\
           'std']

if os.path.isfile("data/results.csv") :
    resultDf = pd.read_csv('data/results.csv')
    
else:
    resultDf = pd.DataFrame(data = [], columns = columns)
        
data = [[conditions['dateStart'],\
        conditions['dateEnd'],\
        conditions['hourStart'],\
        conditions['hourEnd'],\
        conditions['ubication'],\
        conditionsX['relativeTargetSample'],\
        conditionsX['nSamples'],\
        alg,\
        cv,\
        scores.mean(),\
        scores.std()*2]]

newDf = pd.DataFrame(data = data, columns = columns)

resultDf = resultDf.append(newDf)

resultDf.to_csv('data/results.csv', index = False)
=======
#cleaning DataFrame
df = df.drop('Ubicacion', 1)

newEntry = pandas.Series(['AV01', '2001-06-06', 1900, None, None, None, None, None, None])

newDf = pandas.DataFrame([list(newEntry)],\
                         columns=['Codigo', 'Fecha (AAAA-MM-DD)',\
                                 'Hora (HHMM)', 'Humedad relativa (%)', 'Precipitacion (mm)',\
                                 'Radiacion (W/m2)', 'Temperatura (oC)', 'Vel. viento (m/s)', 'Dir. viento (o)'])
                         
df = df.append(newDf, ignore_index=True)

df['Fecha (AAAA-MM-DD)'] = [item.replace('-', '') for item in df['Fecha (AAAA-MM-DD)']]
   
for i, codigo in enumerate(df['Codigo'].unique()):
    df.loc[df["Codigo"]==codigo, "Codigo"] = i

#df['Radiacion (W/m2)'] = np.array([item*100 for item in df['Radiacion (W/m2)']]).astype(long)

predictors = ['Codigo', 'Hora (HHMM)', 'Fecha (AAAA-MM-DD)']
targetIndexes = ["Precipitacion (mm)", "Temperatura (oC)",\
                 "Humedad relativa (%)", "Radiacion (W/m2)",\
                 "Vel. viento (m/s)", "Dir. viento (o)"]

#Defining data and target
solar_data = df
solar_target = df[targetIndexes]
                  
#print solar_data
#print solar_target

#X_train, X_test, y_train, y_test = train_test_split(solar_data, solar_target,\
#                                                    test_size=0.4,\
#                                                    random_state=0)

alg = linear_model.LinearRegression()

#scores = cross_val_score(alg, solar_data[:-1], solar_target[:-1], cv=5)
#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

kf = KFold(n_splits=2)
for train, test in kf.split(solar_data[:-1]):
    alg.fit(solar_data[predictors].loc[train], solar_target.loc[train])
    
    
print alg.predict(solar_data[predictors].iloc[-1:])
>>>>>>> b40cf697f14f61f4bbed84f582dd6e185e21854a
