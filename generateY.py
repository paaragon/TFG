# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 11:24:28 2016

@author: slide22
"""

import pandas as pd

def normalize(col):
    return (col - col.mean()) / (col.max() - col.min())

def generateDataFrame(csvFilePath, xFilePath, destinationcsvPath , verbose = True):
    
    df = pd.read_csv(csvFilePath)
    dfX = pd.read_csv(xFilePath)    
    
    '''
    df['Radiacion (W/m2)'] = normalize(df['Radiacion (W/m2)'])
    '''
    
    if verbose:
        print 'Creating column list'
    
    resultList = []
    
    for index, value in enumerate(dfX['targetHour']):
        
        if verbose:
            print 'Appending row ', index, '/', str(len(dfX))
        rad = df[(df['Hora (HHMM)'] == value) &\
                 (df['Fecha (AAAA-MM-DD)'] == dfX['fecha'].loc[index])]['Radiacion (W/m2)'].values

        resultList.append(rad)
        
    retDF = pd.DataFrame(data = resultList, columns = ['radiacion'])
    
    retDF.to_csv(destinationcsvPath, index = False)
    
    
if __name__ == '__main__':
    
    generateDataFrame('data/filteredFile.csv', 'data/x.csv', 'data/y.csv')
    