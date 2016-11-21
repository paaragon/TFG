#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pandas as pd

def generateDataFrame(csvFilePath, destinationcsvPath, conditions, verbose = True):
    
    df = pd.read_csv(csvFilePath)
    
    #Replace code for number
    if len(df['Codigo'].unique()) > 1:
        for i, codigo in enumerate(df['Codigo'].unique()):
            df.loc[df["Codigo"] == codigo, "Codigo"] = i
    else:
        df.loc["Codigo"] = 1
    
    columns = ['codigo', 'fecha']
    
    if verbose:
        print 'Creating column list'
        
    for i in range(conditions['nSamples']):
        columns.append('hora' + str(i))
        columns.append('precipitacion' + str(i))
        columns.append('temperatura' + str(i))
        columns.append('humedad' + str(i))
        columns.append('radiacion' + str(i))
        columns.append('velviento' + str(i))
        columns.append('dirviento' + str(i))
        
    columns.append('targetHour')
    
    resultList = []
    
    i = 0
    for index in range(len(df.index) - conditions['nSamples'] - conditions['relativeTargetSample']):
        
        if verbose:
            print 'Apending row. ' + str(i) + '/' + str(len(df.index))
            
        r = []
        r.append(df['Codigo'].loc[index])
        r.append(df['Fecha (AAAA-MM-DD)'].loc[index])

        for j in range(conditions['nSamples']):
            r.append(df['Hora (HHMM)'].loc[index + j])
            r.append(df['Precipitacion (mm)'].loc[index + j])
            r.append(df['Temperatura (oC)'].loc[index + j])
            r.append(df['Humedad relativa (%)'].loc[index + j])
            r.append(df['Radiacion (W/m2)'].loc[index + j])
            r.append(df['Vel. viento (m/s)'].loc[index + j])
            r.append(df['Dir. viento (o)'].loc[index + j])
            
        i += 1
            
        r.append(df['Hora (HHMM)'].loc[index + j + conditions['relativeTargetSample']])
        resultList.append(r) 
    
    retDF = pd.DataFrame(data = resultList, columns = columns) 
    
    retDF.to_csv(destinationcsvPath, index = False)
    
if __name__ == '__main__':
    
    conditions = dict()
    conditions['relativeTargetSample'] = 2
    conditions['nSamples'] = 4
    
    generateDataFrame('data/filteredFile.csv', 'data/x.csv' ,conditions)
    