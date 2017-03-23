#-*- coding: utf-8 -*-

from csvManager import createCSVWithConditions
from csvManager import normalizeCSV
from generateX import generateXDF
from generateY import generateYDF
import pandas as pd
import os.path
import json

class SolarData:

    endDate = -1
    startDate = -1
    nSamples = 0
    relativeTargetDistance = 0
    csvWithConditionsPath = ""
    csvDataPath = ""
    csvTargetPath = ""
    dataPath = os.path.join(os.path.dirname(__file__), "../data")

    def __init__(self, startDate, endDate):
        self.endDate = endDate
        self.startDate = startDate
        self.csvWithConditionsPath = self._generatePeriodCsv()
 
    '''
    Function that generate the needed data frames to predict the solar radiation
    
        nSamples - number of data records to include in each row
        relativeTargetDistance - number of records below to set as target
    '''
    def loadData(self, nSamples, relativeTargetDistance):
        self.csvDataPath = self._generateData(nSamples, relativeTargetDistance)
        self.csvTargetPath = self._generateTarget()

    '''
    Private function that generates the data to get the predition(X features)

        nSamples - number of data records to include in each row
        relativeTargetDistance - number of records below to set as target
    '''
    def _generateData(self, nSamples, relativeTargetDistance):
        
        self.nSamples = nSamples
        self.relativeTargetDistance = relativeTargetDistance

        # path where data csv file will be stored
        dataPath = self.dataPath + "/xy/" + str(self.startDate) + str(self.endDate) + str(nSamples) + str(relativeTargetDistance) + "-X" + ".csv"

        # check if csv file already exists
        if os.path.isfile(dataPath):

            print "Data found. Not generated"

        else:
            cond = {
                    'relativeTargetSample': relativeTargetDistance,
                    'nSamples': nSamples
                }
            
            # generate the csv file with the conditions
            df = generateXDF(csvFilePath = self.csvWithConditionsPath,
                        conditions = cond, destinationcsvPath = dataPath)
       
        # It's better create a file and return the path instead of
        # return the data frame as a variable because it's an innescesary
        # huge amount of data in memory
        return dataPath

    '''
    Generate the target data frame of the target data (Y)
    '''
    def _generateTarget(self):

        targetPath = self.dataPath + "/xy/" + str(self.startDate) + str(self.endDate) + str(self.nSamples) + str(self.relativeTargetDistance) + "-Y" + ".csv"

        if os.path.isfile(targetPath):

            print "Target found. Not generated"

        else:

            df = generateYDF(csvFilePath = self.csvWithConditionsPath, xFilePath = self.csvDataPath, destinationcsvPath = targetPath)
      
        return targetPath
       
    '''
    Generate the data frame with the data between two dates
    '''
    def _generatePeriodCsv(self):
   
        if os.path.isfile(str(self.dataPath) \
                              + "/csvWithCondition/" \
                              + str(self.startDate) \
                              + str(self.endDate) \
                              + ".csv"):
    
            print "Csv found. Not generated."
            return self.dataPath+"/csvWithCondition/"+str(self.startDate)+str(self.endDate)+".csv"
    
        cond = {
                'ubation': ['Nava de Arevalo'],
                'dateStart': self.startDate,
                'dateEnd': self.endDate
                }
    
        destinationPath = self.dataPath+"/csvWithCondition/"+str(self.startDate)+str(self.endDate)+".csv"
        createCSVWithConditions(self.dataPath+'/csvFiles/', destinationPath = destinationPath, cond = cond)

        return destinationPath
   
    def getData(self):
        
        destinationpath = self.dataPath + '/reverseNorm/' + str(self.startDate) + str(self.endDate) + str(self.nSamples) + str(self.relativeTargetDistance) + "data.json"

        df, normValues = self.normalizeCSV(pd.read_csv(self.csvDataPath))

        with open(destinationpath, 'w') as outfile:
                json.dump(normValues, outfile)

        return df

    def getTarget(self):

        return pd.read_csv(self.csvTargetPath)

    def normalizeCSV(self, df):

        return normalizeCSV(df)

if __name__ == "__main__":
        
    solarData = SolarData(20150101, 20151231)
    solarData.loadData(3, 2)

    data = solarData.data
    target = solarData.target

    #dfX = getX(df, 3, 2)
    #dfY = getY(df, dfX)
    
    #if df is not None and dfX is not None and dfY is not None:
    #    dfX.to_csv('tmp/x.csv')
    #    dfY.to_csv('tmp/y.csv')

