#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 15:03:10 2016

@author: Abel, Maria, Pablo
"""

from infoRiegoData import csvManager as cM
import pandas
from sklearn import linear_model
from sklearn import datasets

diabetes = datasets.load_diabetes()

conditions = dict()
conditions['dateStart'] = 20010601
conditions['dateEnd'] = 20010607
conditions['hourStart'] = 1900
conditions['hourEnd'] = 1900
conditions['ubication'] = ['Nava de Arevalo']

cM.createCSVWithConditions('data/csvFiles/', 'data/filteredFile.csv', conditions)

df = pandas.read_csv('data/filteredFile.csv')

train = df[:-1]
test = df[-1:]

predictors = ["Hora (HHMM)"]

target = ["Precipitacion (mm)", "Temperatura (oC)",\
              "Humedad relativa (%)", "Radiacion (W/m2)", "Vel. viento (m/s)",\
              "Dir. viento (o)"]

alg = linear_model.LinearRegression()

alg.fit(train[predictors], train[target])

predictions = alg.predict(test[predictors])

print predictions
           