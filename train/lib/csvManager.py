# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 15:14:50 2016

@author: slide22
"""

import pandas
import os
import json
import sys
import dataManager as dm

"""
Read all CSV in a specific folder and create a new one based on the condition
dictionary

Args:
    sourceFolder (str): csv source folder. It have to ends in /
    destinationFolder (str): new csv filename
    cond (dict): dictionary with the filter conditios
                 - startDate (int): the date on which begins csv. Format: YYYYMMDD
                 - endDate (int): the date on which ends csv. Format: YYYYMMDD
                 - startHour (int): the hour on which begins csv. Format: HHMM
                 - endHour (int): the hout on which ends csv. Format: HHMM
                 - ubicationsId (list): list with the ubications ids of the csv
"""
def createCSVWithConditions(sourceFolder, destinationFolder=None, cond = dict(), verbose = True):

    # dictionary with the default conditions
    conditions = {'dateStart': 0,
                  'dateEnd': None,
                  'hourStart': 100,
                  'hourEnd': 2400,
                  'ubicationsId': list()
                  }
    
    # merge the conditions dict with the parameters cond
    conditions.update(cond)
    
    #filter data by date
    csvFiles = []
    i = 0
    while(i < 2 and len(csvFiles) == 0):
        if os.path.isdir(sourceFolder):
            if conditions['dateEnd'] != None:
                csvFiles = [f for f in os.listdir(sourceFolder) \
                            if f[:8].isdigit() \
                            and int(f[:8]) >= conditions['dateStart'] \
                            and int(f[:8]) <= conditions['dateEnd']]
            else:
                csvFiles = [f for f in os.listdir(sourceFolder) \
                            if f[:8].isdigit() \
                            and int(f[:8]) >= conditions['dateStart']]
        
        if len(csvFiles) == 0:
            i += 1
            print '\nNo csv Files found. Downloading.\n'
            dm.generateCsv(conditions['dateStart'], conditions['dateEnd'], '../data/zipFiles', sourceFolder)

    if len(csvFiles) == 0:
        print 'No csv Files found. Downloading FAILED.'
        return None

    csvFiles = sorted(csvFiles)
    
    origColumns = ['Codigo', 'Fecha (AAAA-MM-DD)', 'Hora (HHMM)','Temperatura (oC)', 'Humedad relativa (%)', 'Radiacion (W/m2)']

    columns = ['codigo', 'fecha', 'hora', 'temperatura', 'humedad', 'radiacion']

    df = pandas.DataFrame(columns = columns)

    # loading the files
    i = 0
    for f in csvFiles:
        
        i += 1
        if verbose:
            print 'Reading '+ f + '('+ str(i) +'/'+ str(len(csvFiles)) +')'
            
        auxPath = os.path.join(sourceFolder, f)
        dfAux = pandas.read_csv(auxPath, ';', usecols=origColumns)

        dfAux.columns = columns

        df = df.append(dfAux)
   
    #sort values
    df = df.sort_values(by=['codigo', 'fecha', 'hora'], ascending=True)

    #patching the 2015-06-06 csv
    df['fecha'] = df['fecha'].str.replace('-', '').astype(float)

    df.loc[df['fecha'] == 20120406, 'fecha'] = 20150206
    df.loc[df['fecha'] == 20120408, 'fecha'] = 20150208
    df.loc[df['fecha'] == 20120511, 'fecha'] = 20150118
    df.loc[df['fecha'] == 20120526, 'fecha'] = 20150622
    df.loc[df['fecha'] == 20120607, 'fecha'] = 20150409
    df.loc[df['fecha'] == 20130429, 'fecha'] = 20150329
    df.loc[df['fecha'] == 20120714, 'fecha'] = 20150516
    df.loc[df['fecha'] == 20130502, 'fecha'] = 20150401
    df.loc[df['fecha'] == 20130525, 'fecha'] = 20150424
    df.loc[df['fecha'] == 20130612, 'fecha'] = 20150512
    df.loc[df['fecha'] == 20140129, 'fecha'] = 20150111
    df.loc[df['fecha'] == 20140624, 'fecha'] = 20150606
    df.loc[df['fecha'] == 20140624, 'fecha'] = 20150606
    df.loc[df['fecha'] == 20140626, 'fecha'] = 20150608
    df.loc[df['fecha'] == 20140628, 'fecha'] = 20150610
   
    #filter the data by hour and ubication
    if len(conditions['ubicationsId']) > 0:
        df = pandas.DataFrame(df[(df['hora'] >= conditions['hourStart']) \
                               & (df['hora'] <= conditions['hourEnd']) \
                               & (df['codigo'].isin(conditions['ubicationsId']))])
    else:
        df = pandas.DataFrame(df[(df['hora'] >= conditions['hourStart']) \
                               & (df['hora'] <= conditions['hourEnd'])])
  
    for i, codigo in enumerate(df['codigo'].unique()):
        # i + 1 para que al normalizar no divida entre 0
        df.loc[df['codigo'] == codigo, 'codigo'] = i + 1

    fileName = str(conditions['dateStart']) + str(conditions['dateEnd'])+'.csv'

    destinationPath = os.path.join(destinationFolder, fileName)

    if(not os.path.isdir(destinationFolder)):
        os.makedirs(destinationFolder)

    df.to_csv(destinationPath+'.orig', index = False)
    df, normValues = normalizeCSV(df)

    reverseFolder = os.path.join(destinationFolder, 'reverseNorm')
    if not os.path.isdir(reverseFolder):
        os.makedirs(reverseFolder)

    normpath = os.path.join(reverseFolder, str(conditions['dateStart']) + str(conditions['dateEnd']) + '.json')
    with open(normpath, 'w') as outfile:
        json.dump(normValues, outfile)

    if destinationPath != None:
        df.to_csv(destinationPath, index = False)
        
    return df, destinationPath
        
#
#Normalize a pandas column
#
def normalize(col):

    if(col.max() - col.min() == 0):
        return col.max(), [col.mean(), col.max(), col.min()]
        
    return (col - col.mean()) / (col.max() - col.min()), [col.mean(), col.max(), col.min()]

def denormalize(colName, col, mean, mx, mn):
    
    i = 0
    for val in col:
        print 'Denormalizing ' + colName + '-' + str(i) + '/' + str(len(col))
        val = val * (mx - mn) + mean
        i += 1

    return col

#
#normalize dataframe values and get the control values to restore the data
#
def normalizeCSV(df):
    
    normValues = dict()
    
    for column in list(df):
        df[column], normValues[column] = normalize(df[column])
    
    return df, normValues

def denormalizeCSV(df, reverseNormPath):
    
    reverseNorm = pandas.read_json(reverseNormPath)

    for col in list(df):
        mean = reverseNorm[col][0]
        mx = reverseNorm[col][1]
        mn = reverseNorm[col][2]
        df[col] = denormalize(col, df[col], mean, mx, mn)
    
    return df
    
if __name__ == "__main__":

    conditions = dict()
    
    conditions['dateStart'] = 20150101
    conditions['dateEnd'] = 20150131
    
    if len(sys.argv) > 1:
        conditions['dateStart'] = int(sys.argv[1])
    if len(sys.argv) > 2:
        conditions['dateEnd'] = int(sys.argv[2])

    #conditions['hourStart'] = 100
    #conditions['hourEnd'] = 200
    conditions['ubication'] = ['Nava de Arevalo']
    
    createCSVWithConditions('../data/csvFiles', '../data/csvWithCondition', conditions)
