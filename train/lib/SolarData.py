#-*- coding: utf-8 -*-

import os.path
import pandas as pd
from csvManager import createCSVWithConditions
from csvManager import normalizeCSV
from train_data import TrainData

class SolarData(object):
    """This class generate data sets for train"""

    end_date = -1
    start_date = -1
    start_hout = 100
    end_hour = 2400
    n_samples = 0
    target_distances = 0
    csv_with_conditions_path = ""
    x_path = ""
    y_path = ""
    data_path = os.path.join(os.path.dirname(__file__), "../data")

    def __init__(self, startDate, endDate, startHour = 100, endHour = 2400):
        self.end_date = endDate
        self.start_date = startDate
        self.start_hout = startHour
        self.end_hour = endHour

        self.csv_with_conditions_path = self._generate_period_csv()


    def load_data(self, n_samples, target_distances):
        """
        Function that generate the needed data frames to predict the solar radiation

            nSamples - number of data records to include in each row
            relativeTargetDistance - number of records below to set as target
        """

        orig_csv_file = str(self.data_path) \
                          + "/csvWithCondition/" \
                          + str(self.start_date) \
                          + str(self.end_date) \
                          + ".csv"

        dest_folder = str(self.data_path) + "xy"

        train_data = TrainData(orig_csv_file_path=orig_csv_file,
                               dest_folder=dest_folder,
                               n_samples=n_samples,
                               target_distances=target_distances,
                               orig_prefix_cols=["codigo", "fecha"],
                               orig_cols=["hora", "temperatura", "humedad", "radiacion"],
                               x_prefix_cols=["codigo", "fecha"],
                               x_cols=["hora", "temperatura", "humedad", "radiacion"],
                               y_cols=["radiacion"],
                               orig_y_col=["radiacion"])

        self.x_path, self.y_path = train_data.generate_train_data()

    def _generate_period_csv(self):
        '''
        Generate the data frame with the data between two dates
        '''

        if os.path.isfile(str(self.data_path)
                          + "/csvWithCondition/"
                          + str(self.start_date)
                          + str(self.end_date)
                          + ".csv"):

            print "Csv found. Not generated."
            return self.data_path \
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

        destination_folder = os.path.join(self.data_path, "csvWithCondition")
        source_folder = os.path.join(self.data_path, 'csvFiles')

        destination_path = createCSVWithConditions(source_folder,
                                                   destinationFolder=destination_folder,
                                                   cond=cond)

        return destination_path

    def get_x(self):

        return pd.read_csv(self.x_path)

    def get_y(self):

        return pd.read_csv(self.y_path)

    def normalize_csv(self, df):

        return normalizeCSV(df)

def main():
    """main function of the module (for use it on cli)"""

    k = 3
    target_distances = [2]

    solar_data = SolarData(20150101, 20150131)
    solar_data.load_data(k, target_distances)

    data = solar_data.get_x()
    target = solar_data.get_y()

    print data.shape
    print target.shape

if __name__ == "__main__":
    main()
