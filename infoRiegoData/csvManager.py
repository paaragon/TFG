# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 15:14:50 2016

@author: slide22
"""

'''
csvFolder - Folder in wich the csv are in
conditions:
    - dateStart: YYYYMMDD
    - dateEnd: YYYYMMDD
    - hourStart HHMM
    - hourEnd: HHMM
    - ubication
    
'''
def createCSVWithConditions(sourceFolder, destinationPath, cond = dict()):
    
    import pandas
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
    
    # get the files between the condition date
    if conditions['dateEnd'] != None:
        csvFiles = [f for f in listdir(sourceFolder) \
                      if f[:8].isdigit() \
                      and int(f[:8]) >= conditions['dateStart'] \
                      and int(f[:8]) <= conditions['dateEnd']]
    else:
        csvFiles = [f for f in listdir(sourceFolder) \
                      if f[:8].isdigit() \
                      and int(f[:8]) >= conditions['dateStart']]
    
    # loading the files
    
    for f in csvFiles:
        if 'df' not in locals():
            df = pandas.read_csv(sourceFolder + f, ';')
        else:
            df.append(pandas.read_csv(sourceFolder + f, ';'))
    
    df = pandas.DataFrame(df[(df['Hora (HHMM)'] >= conditions['hourStart']) \
                           & (df['Hora (HHMM)'] <= conditions['hourEnd']) \
                           & (df['Ubicacion'].isin(conditions['ubication']))])
                           
    df.to_csv(destinationPath, index = False)
    
if __name__ == "__main__":

    conditions = dict()
    conditions['dateStart'] = 20010101
    conditions['dateEnd'] = 20010101
    conditions['hourStart'] = 100
    conditions['hourEnd'] = 200
    conditions['ubication'] = ['Nava de Arevalo', 'Miranda de Ebro']
    
    createCSVWithConditions('../csvFiles/', 'file.csv', conditions)