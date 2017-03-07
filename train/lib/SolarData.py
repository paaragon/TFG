# -*- coding: utf-8 -*-

from csvManager import createCSVWithConditions
from generateX import generateXDF
from generateY import generateYDF
import pandas as pd
import os.path

class SolarData:

    endDate = -1
    startDate = -1
    df = None
    dfX = None
    data = None
    target = None
    dataPath = "../data"

    def __init__(self, startDate, endDate):
        self.endDate = endDate
        self.startDate = startDate
        self.df = self._getPeriod(self.startDate, self.endDate, toFile = True)
 
    '''
    Function that generate the needed data frames to predict the solar radiation
    
        nSamples - number of data records to include in each row
        relativeTargetDistance - number of records below to set as target
    '''
    def loadData(self, nSamples, relativeTargetDistance):
        self.data = self._generateData(nSamples, relativeTargetDistance)
        self.target = self._generateTarget()

    '''
    Private function that generates the data to get the predition(X features)

        nSamples - number of data records to include in each row
        relativeTargetDistance - number of records below to set as target
    '''
    def _generateData(self, nSamples, relativeTargetDistance):

        if os.path.isfile(self.dataPath \
                          + "/xy" \
                          + str(self.startDate) \
                          + str(self.endDate) \
                          + str(nSamples) \
                          + str(relativeTargetDistance)):

            print "Data found. Not generated"
            return pd.read_csv(self.dataPath \
                               + "/xy/" \
                               + str(self.startDate) \
                               + str(self.endDate) \
                               + str(nSamples) \
                               + str(relativeTargetDistance))

        cond = {
                'relativeTargetSample': relativeTargetDistance,
                'nSamples': nSamples
            }
    
        return generateXDF(df = self.df,
                           conditions = cond,
                           destinationcsvPath = self.dataPath \
                                + "/xy/"+str(self.startDate)\
                                + str(self.endDate) \
                                + str(nSamples) \
                                + str(relativeTargetDistance))
  
    '''
    Generate the target data frame of the target data (Y)
    '''
    def _generateTarget(self):
        return generateYDF(df = self.df, dfX = self.data)
       
    '''
    Generate the data frame with the data between two dates
    '''
    def _getPeriod(self, startDate, endDate, toFile = False, regenerate = False):
   
        if not regenerate \
           and os.path.isfile(str(self.dataPath) \
                              + "/csvWithCondition/" \
                              + str(self.startDate) \
                              + str(self.endDate) \
                              + ".csv"):
    
            print "Csv found. Not generated."
            return pd.read_csv(self.dataPath+"/csvWithCondition/"+str(self.startDate)+str(self.endDate)+".csv")
    
        cond = {
                'ubation': ['Nava de Arevalo'],
                'dateStart': startDate,
                'dateEnd': endDate
                }
    
        if toFile:
            destinationPath = self.dataPath+"/csvWithCondition/"+str(self.startDate)+str(self.endDate)+".csv"
        else:
            destinationPath = None
    
        return createCSVWithConditions(self.dataPath+'/csvFiles/', destinationPath = destinationPath, cond = cond)
    
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

