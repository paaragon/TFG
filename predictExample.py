#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 15:03:10 2016

@author: Abel, Maria, Pablo
"""

from infoRiegoData import csvManager as cM
from sklearn.model_selection import cross_val_score
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import pandas as pd
import generateY as y
import generateX as x
import os.path
import math

'''
conditions = dict()
conditions['dateStart'] = 20150601
conditions['dateEnd'] = 20150930
conditions['hourStart'] = 800
conditions['hourEnd'] = 2000
conditions['ubication'] = ['Nava de Arevalo']

cM.createCSVWithConditions('data/csvFiles/',\
                           'data/filteredFile.csv',\
                           conditions)
cM.normalizeCSV('data/filteredFile.csv', 'data/normalized.csv')

conditionsX = dict()
conditionsX['relativeTargetSample'] = 2
conditionsX['nSamples'] = 4
x.generateDataFrame('data/normalized.csv','data/x.csv', conditionsX)

conditionsY = dict()
y.generateDataFrame('data/normalized.csv', 'data/x.csv', 'data/y.csv')
'''

dfX = pd.read_csv('data/x.csv')
dfY = pd.read_csv('data/y.csv')

#selectionIndex = math.ceil(len(dfX) * 0.7)
selectionIndex = len(dfX) - 1

X_train = dfX[:selectionIndex]
y_train = dfY[:selectionIndex]
X_test = dfX[selectionIndex:]
y_test = dfY[selectionIndex:]

for i, codigo in enumerate(dfX['codigo'].unique()):
    dfX.loc[dfX['codigo'] == codigo, 'codigo'] = i
    
alg = linear_model.LinearRegression()
cv = 3

alg.fit(X_train, y_train)

prediction = alg.predict(X_test)

print prediction

'''
X_train, X_test, y_train, y_test = train_test_split(dfX,\
                                                    dfY,\
                                                    test_size=0.3,\
                                                    random_state=42)
                                                    
print "Train:"
print X_train.shape
print y_train.shape

print "Test:"
print X_test.shape
print y_test.shape

alg.fit(X_train, y_train)

prediction = alg.predict(X_test)
'''
'''
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

#scores = cross_val_score(alg, solar_data[:-1], solar_target[:-1], cv=5)
#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
'''