# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 13:09:46 2016

@author: slide22
"""

"""
This sript tries to predict the solar radiation based on the data recopiled by
inforiego
"""

"""
Create a table with the data in the window

Args:
    startDate (int): YYYYMMDD
    endDate (int): YYYYMMDD
    startTime (int): HHMM
    endTime (int): HHMM
    ubication (list)

Returns:
    window: the dataframe with the data
"""
def getDataWindow(startDate, endDate, startTime, endTime, ubication = list()):
    
    from infoRiegoData import csvManager as cM
    import pandas as pd
    
    conditions = {'dateStart': startDate,
                  'dateEnd': endDate,
                  'hourStart': startTime,
                  'hourEnd': endTime,
                  'ubication': ubication
                  }
    cM.createCSVWithConditions('data/csvFiles/', 'data/filteredFile.csv', conditions)
    return pd.read_csv('data/filteredFile.csv')

def predict():
    pass

if __name__ == "__main__":
    print getDataWindow(20010101, 20020101, 100, 2400, ['Nava de Arevalo'])