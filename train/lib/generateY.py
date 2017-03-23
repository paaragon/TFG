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
    for index, value in enumerate(dfX['targetHour']):
        
        perc = index * 100 / len(dfX)
        
        if verbose and perc != percentage:
            print 'Appending row ', index, '/', str(len(dfX)) + '. ' + str(perc) + '%'
            percentage = perc

        rad = df[(df['hora'] == value) &\
                 (df['fecha'] == dfX['fecha'].loc[index])]['radiacion'].values[0]
            
        resultList.append(rad)
    
    retDF = pd.DataFrame(data = resultList, columns = ['radiacion'])
    
    if destinationcsvPath != None:
        retDF.to_csv(destinationcsvPath, index = False)
    else:
        return retDF
    
if __name__ == '__main__':
    
    generateYDF('../data/csvWithCondition/2015.csv', '../data/xy/2015X.csv', '../data/xy/2015Y.csv')
    
