# -*- coding: utf-8 -*-

from csvManager import createCSVWithConditions
from generateX import generateXDF
from generateY import generateYDF

# get all the data from specific year
def getYear(year, destinationPath = None):

    cond = {
            'ubication': ['Nava de Arevalo'],
            'dateStart': int(str(year)+'0101'),
            'dateEnd': int(str(year)+'1231')
            }
    return createCSVWithConditions('../data/csvFiles/', destinationPath = destinationPath, cond = cond)

#get data from a period
def getPeriod(startDate, endDate, destinationPath = None):
    cond = {
            'ubation': ['Nava de Arevalo'],
            'dateStart': startDate,
            'dateEnd': endDate
            }
    return createCSVWithConditions('../data/csvFiles/', destinationPath = destinationPath, cond = cond)

#get x data from DataFrame (features)
def getX(df, nSamples, relativeTargetDistance):
    cond = {
            'relativeTargetSample': relativeTargetDistance,
            'nSamples': nSamples
        }

    return generateXDF(df = df, conditions = cond)

#get y data from DataFrame (target)
def getY(df, dfX):
    return generateYDF(df = df, dfX = dfX)


if __name__ == "__main__":
    
    import pandas as pd
    df = getYear(2015, '../data/csvWithCondition/2015.csv')
    #dfX = getX(df, 3, 2)
    #dfY = getY(df, dfX)

    #if df is not None and dfX is not None and dfY is not None:
    #    dfX.to_csv('tmp/x.csv')
    #    dfY.to_csv('tmp/y.csv')

