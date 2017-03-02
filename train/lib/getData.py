# -*- coding: utf-8 -*-

from csvManager import createCSVWithConditions
from generateX import generateXDF
from generateY import generateYDF
import pandas as pd
import os.path

# get all the data from specific year
def getYear(year, toFile = True, regenerate = False):

    #if file exists and regenerate is False read the file and return DF
    if not regenerate and os.path.isfile("../data/csvWithCondition/"+str(year)+".csv"):
        print "Csv found. Not generated.abs"
        return pd.read_csv("../data/csvWithCondition/"+str(year)+".csv");
    
    print "Generating csv"
    cond = {
            'ubication': ['Nava de Arevalo'],
            'dateStart': int(str(year)+'0101'),
            'dateEnd': int(str(year)+'1231')
            }

    #if toFile is true set destination path
    if toFile:
        detinationPath = "../data/csvWithCondition/"+str(year)+".csv"
    else:
        destinationPath = None

    return createCSVWithConditions('../data/csvFiles/', destinationPath = destinationPath, cond = cond)

#get data from a period
def getPeriod(startDate, endDate, toFile = False, regenerate = False):

    if not regenerate and os.path.isFile("../data/csvWithCondition/"+str(startDate)+str(endDate)+".csv"):

        print "Csv found. Not generated."
        return pd.read_csv("../data/csvWithCondition/"+str(startDate)+str(endDate)+".csv")

    cond = {
            'ubation': ['Nava de Arevalo'],
            'dateStart': startDate,
            'dateEnd': endDate
            }

    if toFile:
        destinationPath = "../data/csvWithCondition/"+str(startDate)+str(endDate)+".csv"
    else:
        destinationPath = None

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

