#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 15:03:10 2016

@author: Abel, Maria, Pablo
"""

from infoRiegoData import csvManager as cM
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

conditionsX = dict()
conditionsX['relativeTargetSample'] = 2
conditionsX['nSamples'] = 4
#x.generateDataFrame('data/filteredFile.csv','data/x.csv', conditionsX)

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

alg = linear_model.LinearRegression()

#scores = cross_val_score(alg, solar_data[:-1], solar_target[:-1], cv=5)
#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

