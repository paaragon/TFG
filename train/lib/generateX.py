#!usr/bin/env python2
# -*- coding: utf-8 -*-

import pandas as pd

def generateXDF(conditions, csvFilePath=None, destinationcsvPath=None, df=None, verbose = True):
    
    #if no source path espicified uses df by param
    if csvFilePath is not None:
        df = pd.read_csv(csvFilePath)
    
    if csvFilePath is None and df is None:
        print 'No DataFrame'
        return None

    #Replace code for number
    if len(df['Codigo'].unique()) > 1:
        for i, codigo in enumerate(df['Codigo'].unique()):
            df.loc[df["Codigo"] == codigo, "Codigo"] = i
    else:
        df.loc["Codigo"] = 1
    
    if verbose:
        print 'Creating column list'
   
    columns = ['codigo', 'fecha']
         
    for i in range(conditions['nSamples']):
        columns.append('hora' + str(i))
        columns.append('temperatura' + str(i))
        columns.append('humedad' + str(i))
        columns.append('radiacion' + str(i))
        
    columns.append('targetHour')
    
    resultList = []
   
    #append X data in list
    i = 0
    for index in range(len(df.index) - conditions['nSamples'] - conditions['relativeTargetSample']):
        
        if verbose:
            print 'Apending row. ' + str(i) + '/' + str(len(df.index))
            
        r = []
        r.append(df['Codigo'].iloc[index])
        r.append(df['Fecha (AAAA-MM-DD)'].iloc[index])

        for j in range(conditions['nSamples']):
            r.append(df['Hora (HHMM)'].iloc[index + j])
            r.append(df['Temperatura (oC)'].iloc[index + j])
            r.append(df['Humedad relativa (%)'].iloc[index + j])
            r.append(df['Radiacion (W/m2)'].iloc[index + j])
            
        i += 1
            
        r.append(df['Hora (HHMM)'].iloc[index + j + conditions['relativeTargetSample']])
        resultList.append(r) 
    
    #create Data Frame with result values
    retDF = pd.DataFrame(data = resultList, columns = columns) 
    
    if destinationcsvPath != None:
        retDF.to_csv(destinationcsvPath, index = False)

    return retDF
    
if __name__ == '__main__':
    
    conditions = dict()
    conditions['relativeTargetSample'] = 2
    conditions['nSamples'] = 4
    
    generateXDF(conditions, '../data/csvWithCondition/2015.csv', '../data/xy/2015X.csv')
    
