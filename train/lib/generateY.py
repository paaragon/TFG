# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 11:24:28 2016

@author: slide22
"""

import pandas as pd

def generateYDF(csvFilePath=None, xFilePath=None, destinationcsvPath=None, df=None, dfX=None, verbose = True):
    
    if csvFilePath is not None:
        df = pd.read_csv(csvFilePath)

    if xFilePath is not None:
        dfX = pd.read_csv(xFilePath) 
    
    if df is None:
        print 'DataFrame is None'
        return -1

    if dfX is None:
        print 'X DataFrame is None'
        return -2

    if verbose:
        print 'Creating column list'
    
    resultList = []
    
    percentage = -1
    last_date = None
    current_date = None

    for index, value in enumerate(dfX['targetHour']):
        #Recorrer los targetHour de dfX y buscar su radiacion en df
        
        perc = index * 100 / len(dfX)
        
        if verbose and perc != percentage:
            print 'Appending row ', index, '/', str(len(dfX)) + '. ' + str(perc) + '%'
            percentage = perc

        #Si no encuentra targetHour: 
        # - probar si hay error de precision de floats
        # - si no hay mas horas en el dia
        if len(df[(df['hora'] == value) & \
                  (df['fecha'] == dfX['fecha'].loc[index])]['radiacion'].values) == 0:
            
            #Si probando con floats muy parecidos no se encuentra
            # - Se prueba con la fecha de la vueta anterior
            if len(df[(is_close(df['hora'], value)) &\
                 (is_close(df['fecha'], dfX['fecha'].loc[index]))]['radiacion'].values) == 0:

                rad = df[(is_close(df['hora'], value)) &\
                    (is_close(df['fecha'], last_date))]['radiacion'].values[0]
            
            #Si probando con floats muy parecidos si se encuentra
            else:
                
                rad = df[(is_close(df['hora'], value)) &\
                    (is_close(df['fecha'], dfX['fecha'].loc[index]))]['radiacion'].values[0]
        else:
            rad = df[(df['hora'] == value) &\
                 (df['fecha'] == dfX['fecha'].loc[index])]['radiacion'].values[0]

        if current_date != dfX['fecha'].loc[index]:
            last_date = current_date
            current_date = dfX['fecha'].loc[index]
        
        resultList.append(rad)
    
    retDF = pd.DataFrame(data = resultList, columns = ['radiacion'])
    
    if destinationcsvPath != None:
        retDF.to_csv(destinationcsvPath, index = False)
    else:
        return retDF

def is_close(f1, f2):

    return abs(f1 - f2) <= 0.00000000001
    
if __name__ == '__main__':
    
    generateYDF('../data/csvWithCondition/2015.csv', '../data/xy/2015X.csv', '../data/xy/2015Y.csv')
    
