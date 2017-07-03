#-*- coding: utf-8 -*-

import os.path
import pandas as pd
from csvManager import createCSVWithConditions
from csvManager import normalizeCSV
from generateX import generateXDF
from generateY import generateYDF

class SolarData(object):
    """This class generate data sets for train"""

    end_date = -1
    start_date = -1
    start_hout = 100
    end_hour = 2400
    nSamples = 0
    relativeTargetDistance = 0
    csv_with_conditions_path = ""
    csvDataPath = ""
    csvTargetPath = ""
    dataPath = os.path.join(os.path.dirname(__file__), "../data")

    def __init__(self, startDate, endDate, startHour = 100, endHour = 2400):
        self.end_date = endDate
        self.start_date = startDate
        self.start_hout = startHour
        self.end_hour = endHour

        self.csv_with_conditions_path = self._generatePeriodCsv()


    def loadData(self, nSamples, relativeTargetDistance):
        """
        Function that generate the needed data frames to predict the solar radiation
        
            nSamples - number of data records to include in each row
            relativeTargetDistance - number of records below to set as target
        """

        self.csvDataPath = self._generateData(nSamples, relativeTargetDistance)
        self.csvTargetPath = self._generateTarget()


    def _generateData(self, nSamples, relativeTargetDistance):
        '''
        Private function that generates the data to get the predition(X features)

            nSamples - number of data records to include in each row
            relativeTargetDistance - number of records below to set as target
        '''

        self.nSamples = nSamples
        self.relativeTargetDistance = relativeTargetDistance

        # path where data csv file will be stored
        dataPath = os.path.join(self.dataPath, 'xy', str(self.start_date) + str(
            self.end_date) + str(nSamples) + str(relativeTargetDistance) + "-X" + ".csv")

        # check if csv file already exists
        if os.path.isfile(dataPath):

            print "Data found. Not generated"

        else:

            cond = {
                'relativeTargetSample': relativeTargetDistance,
                'nSamples': nSamples
            }

            # generate the csv file with the conditions

            generateXDF(cond, self.csv_with_conditions_path, dataPath)

        # It's better create a file and return the path instead of
        # return the data frame as a variable because it's an innescesary
        # huge amount of data in memory
        return dataPath

    def _generateTarget(self):
        '''
        Generate the target data frame of the target data (Y)
        '''

        targetPath = self.dataPath + "/xy/" + str(self.start_date) + str(self.end_date) + str(
            self.nSamples) + str(self.relativeTargetDistance) + "-Y" + ".csv"

        if os.path.isfile(targetPath):

            print "Target found. Not generated"

        else:

            generateYDF(csvFilePath=self.csv_with_conditions_path,
                        xFilePath=self.csvDataPath, destinationcsvPath=targetPath)

        return targetPath

    def _generatePeriodCsv(self):
        '''
        Generate the data frame with the data between two dates
        '''

        if os.path.isfile(str(self.dataPath)
                          + "/csvWithCondition/"
                          + str(self.start_date)
                          + str(self.end_date)
                          + ".csv"):

            print "Csv found. Not generated."
            return self.dataPath \
                + "/csvWithCondition/" \
                + str(self.start_date) \
                + str(self.end_date) + ".csv"

        cond = {
            'ubicationsId': ['AV01'],
            'dateStart': self.start_date,
            'dateEnd': self.end_date,
            'hourStart': self.start_hout,
            'hourEnd': self.end_hour
        }

        destinationFolder = os.path.join(self.dataPath, "csvWithCondition")
        sourceFolder = os.path.join(self.dataPath, 'csvFiles')

        destinationPath = createCSVWithConditions(
            sourceFolder, destinationFolder=destinationFolder, cond=cond)

        return destinationPath

    def getData(self):

        return pd.read_csv(self.csvDataPath)

    def getTarget(self):

        return pd.read_csv(self.csvTargetPath)

    def normalizeCSV(self, df):

        return normalizeCSV(df)


if __name__ == "__main__":

    k = 3
    sDistance = 2

    solarData = SolarData(20150101, 20150131)
    solarData.loadData(k, sDistance)

    data = solarData.getData()
    target = solarData.getTarget()

    print data.shape
    print target.shape
