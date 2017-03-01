# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 15:14:50 2016

@author: slide22
"""

import pandas

"""
Read all CSV in a specific folder and create a new one based on the condition
dictionary

Args:
    sourceFolder (str): csv source folder. It have to ends in /
    destinationPath (str): new csv filename
    cond (dict): dictionary with the filter conditios
                 - startDate (int): the date on which begins csv. Format: YYYYMMDD
                 - endDate (int): the date on which ends csv. Format: YYYYMMDD
                 - startHour (int): the hour on which begins csv. Format: HHMM
                 - endHour (int): the hout on which ends csv. Format: HHMM
                 - ubication (list): list with the ubications of the csv
"""
def createCSVWithConditions(sourceFolder, destinationPath=None, cond = dict(), verbose = True):
    
    from os import listdir

    # dictionary with the default conditions
    conditions = {'dateStart': 0,
                  'dateEnd': None,
                  'hourStart': 100,
                  'hourEnd': 2400,
                  'ubication': list()
                  }
    
    # merge the conditions dict with the parameters cond
    conditions.update(cond)
    
    #filter data by date
    if conditions['dateEnd'] != None:
        csvFiles = [f for f in listdir(sourceFolder) \
                      if f[:8].isdigit() \
                      and int(f[:8]) >= conditions['dateStart'] \
                      and int(f[:8]) <= conditions['dateEnd']]
    else:
        csvFiles = [f for f in listdir(sourceFolder) \
                      if f[:8].isdigit() \
                      and int(f[:8]) >= conditions['dateStart']]
    
    if len(csvFiles) == 0:
        print 'No csv Files found'
        return None

    csvFiles = sorted(csvFiles)

    # loading the files
    i = 0
    for f in csvFiles:
        
        i += 1
        if verbose:
            print 'Reading '+ f + '('+ str(i) +'/'+ str(len(csvFiles)) +')'
            
        if 'df' not in locals():
            df = pandas.read_csv(sourceFolder + f, ';')
            
        else:
            dfAux = pandas.read_csv(sourceFolder + f, ';')
            df = df.append(dfAux)
    
    #patching the 2015-06-06 csv
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2012-04-06', 'Fecha (AAAA-MM-DD)'] = '2015-02-06'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2012-04-08', 'Fecha (AAAA-MM-DD)'] = '2015-02-08'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2012-05-11', 'Fecha (AAAA-MM-DD)'] = '2015-01-18'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2012-05-26', 'Fecha (AAAA-MM-DD)'] = '2015-06-22'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2012-06-07', 'Fecha (AAAA-MM-DD)'] = '2015-04-09'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2013-04-29', 'Fecha (AAAA-MM-DD)'] = '2015-03-29'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2012-07-14', 'Fecha (AAAA-MM-DD)'] = '2015-05-16'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2013-05-02', 'Fecha (AAAA-MM-DD)'] = '2015-04-01'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2013-05-25', 'Fecha (AAAA-MM-DD)'] = '2015-04-24'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2013-06-12', 'Fecha (AAAA-MM-DD)'] = '2015-05-12'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2014-01-29', 'Fecha (AAAA-MM-DD)'] = '2015-01-11'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2014-06-24', 'Fecha (AAAA-MM-DD)'] = '2015-06-06'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2014-06-24', 'Fecha (AAAA-MM-DD)'] = '2015-06-06'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2014-06-26', 'Fecha (AAAA-MM-DD)'] = '2015-06-08'
    df.loc[df['Fecha (AAAA-MM-DD)'] == '2014-06-28', 'Fecha (AAAA-MM-DD)'] = '2015-06-10'
    
    #filter the data by hour and ubication
    if len(conditions['ubication']) > 0:
      
        df = pandas.DataFrame(df[(df['Hora (HHMM)'] >= conditions['hourStart']) \
                               & (df['Hora (HHMM)'] <= conditions['hourEnd']) \
                               & (df['Ubicacion'].isin(conditions['ubication']))])
    else:
        df = pandas.DataFrame(df[(df['Hora (HHMM)'] >= conditions['hourStart']) \
                               & (df['Hora (HHMM)'] <= conditions['hourEnd'])])
    
    #sort values
    df = df.sort_values(by=['Codigo', 'Fecha (AAAA-MM-DD)', 'Hora (HHMM)'], ascending=True)                         
     
    if destinationPath != None:
        df.to_csv(destinationPath, index = False)
        
    return df
        
#
#Normalize a pandas column
#
def normalize(col):
    return (col - col.mean()) / (col.max() - col.min()), [col.mean(), col.max(), col.min()]

#
#normalize dataframe values and get the control values to restore the data
#
def normalizeCSV(df):

    df['Fecha (AAAA-MM-DD)'] = df['Fecha (AAAA-MM-DD)'].str.replace('-', '').astype(float)

    #retrieve normalized values and control values to restore data
    normValues = dict()
    df['Fecha (AAAA-MM-DD)'], normValues['Fecha (AAAA-MM-DD)'] = normalize(df['Fecha (AAAA-MM-DD)'])
    df['Hora (HHMM)'], normValues['Hora (HHMM)'] = normalize(df['Hora (HHMM)'])
    df['Temperatura (oC)'], normValues['Temperatura (oC)'] = normalize(df['Temperatura (oC)'])
    df['Humedad relativa (%)'], normValues['Humedad relativa (%)'] = normalize(df['Humedad relativa (%)'])
    df['Radiacion (W/m2)'], normValues['Radiacion (W/m2)'] = normalize(df['Radiacion (W/m2)'])
    
    return df, normValues
    
if __name__ == "__main__":

    conditions = dict()
    conditions['dateStart'] = 20010101
    conditions['dateEnd'] = 20020101
    #conditions['hourStart'] = 100
    #conditions['hourEnd'] = 200
    conditions['ubication'] = ['Nava de Arevalo']
    
    createCSVWithConditions('../data/csvFiles/', '../data/filteredFile.csv', conditions)
