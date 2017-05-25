#!usr/bin/env python2
# -*- coding: utf-8 -*-

import pandas as pd
import os

def generateXDF(conditions, csvFilePath=None, destinationcsvPath=None, df=None, verbose = True):
    
    #if no source path espicified uses df by param
    if csvFilePath is not None:
        df = pd.read_csv(csvFilePath)
    
    if csvFilePath is None and df is None:
        print 'No DataFrame'
        return None

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
    percentage = -1
    for index in range(len(df.index) - conditions['nSamples'] - conditions['relativeTargetSample']):
        
        perc = i * 100 / len(df.index)
        if verbose and perc != percentage:
            print 'Apending row. ' + str(i) + '/' + str(len(df.index)) + '. ' + str(perc)+'%'

            percentage = perc
            
        r = []
        r.append(df['codigo'].iloc[index])
        r.append(df['fecha'].iloc[index])

        for j in range(conditions['nSamples']):
            r.append(df['hora'].iloc[index + j])
            r.append(df['temperatura'].iloc[index + j])
            r.append(df['humedad'].iloc[index + j])
            r.append(df['radiacion'].iloc[index + j])
            
        i += 1
            
        r.append(df['hora'].iloc[index + j + conditions['relativeTargetSample']])
        resultList.append(r) 
    
    #create Data Frame with result values
    retDF = pd.DataFrame(data = resultList, columns = columns) 
    
    dirName = os.path.dirname(destinationcsvPath)
    if not os.path.isdir(dirName):
        os.makedirs(dirName)

    if destinationcsvPath != None:
        retDF.to_csv(destinationcsvPath, index = False)

    return retDF
    
if __name__ == '__main__':
    
    conditions = dict()
    conditions['relativeTargetSample'] = 2
    conditions['nSamples'] = 4
    
    generateXDF(conditions, '../data/csvWithCondition/2015.csv', '../data/xy')
    
