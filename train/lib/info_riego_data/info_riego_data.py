# -*- coding: utf-8 -*-

"""
This module download and combine InfoRiego data in one csv file
"""

import os
import argparse
import lib.data_manager as data_manager
import lib.csv_manager as csv_manager
import json

class InfoRiegoData(object):

    start_date = None
    end_date = None
    start_hour = None
    end_hour = None
    ubications = []
    destination_folder = None
    config_file = None
    verbose = True

    def __init__(self, start_date=None, end_date=None, start_hour=None, end_hour=None, ubications=None, relative_radiation=False, destination_folder=None, config_file=None, verbose=True):

        self.config_file = config_file
        self.start_date = start_date
        self.end_date = end_date
        self.start_hour = end_hour
        self.ubications = ubications
        self.relative_radiation = relative_radiation
        self.destination_folder = destination_folder
        self.config_file = config_file

        self.parse_config_file()
        self.check_errors()

    def generate_csv(self):
        """This function downoads and concatenate the data in one csv file"""

        self._download_data()
        self._filter_and_unify_data()

    def _download_data(self):

        folder = os.path.join(self.destination_folder, 'csv_files')
        dm = data_manager.DataManager(self.start_date, self.end_date, folder, verbose=self.verbose)
        dm.get_data()

    def _filter_and_unify_data(self):

        orig_folder = os.path.join(self.destination_folder, 'csv_files')
        dest_folder = os.path.join(self.destination_folder, 'filtered_csv')
        csv = csv_manager.CsvManager(self.start_date, self.end_date, self.start_hour, self.end_hour, self.ubications, self.relative_radiation, orig_folder, dest_folder, verbose=self.verbose)
        csv.filter_data()

    def parse_config_file(self):
        """This method parse the sef.config file and assign the values to attributes"""

        if self.config_file is not None:

            if self.verbose:
                print "Parsing config file"

            with open(self.config_file) as data_file:
                config_data = json.load(data_file)

            if "start_date" in config_data:
                self.start_date = config_data["start_date"]

            if "end_date" in config_data:
                self.end_date = config_data["end_date"]

            if "start_hour" in config_data:
                self.start_hour = config_data["start_hour"]

            if "end_hour" in config_data:
                self.end_hour = config_data["end_hour"]

            if "ubications" in config_data:
                self.ubications = config_data["ubications"]

            if "relative_radiation" in config_data:
                self.relative_radiation = config_data["relative_radiation"]

            if "destination_folder" in config_data:
                self.destination_folder = config_data["destination_folder"]

    def check_errors(self):
        """ This method check if all the variables have the correct values """

        if self.start_date is None:
            raise Exception(1, "No start_date specified")

        elif self.end_date is None:
            raise Exception(2, "No end_date specified.")

        elif self.start_hour is None:
            raise Exception(4, "No start_hour specified.")

        elif self.end_hour is None:
            raise Exception(6, "No end_hour specified.")

        elif self.destination_folder is None:
            raise Exception(7, "No destination_folder specified.")

        elif self.ubications is None:
            raise Exception(7, "No ubications specified.")

        elif self.relative_radiation is None:
            raise Exception(7, "No relative_radiation specified.")

        elif self.start_date > self.end_date:
            raise Exception(7, "start_date greater than end_date.")

        elif self.start_hour > self.end_hour:
            raise Exception(7, "start_hour greater than end_hour.")

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config-file', nargs='?', action="store", dest="config_file", help="File with the parameters download the data. It can only contain some parameters and specify the others by cli.")
    parser.add_argument('--start-date', dest="start_date", action="store", help="The start date of the set. (YYYYMMDD).", type=int)
    parser.add_argument('--end-date', dest="end_date", action="store", help="The end date of the set. (YYYYMMDD).", type=int)
    parser.add_argument('--start-hour', dest="start_hour", action="store", help="The start hour of the set. (HHMM).", type=int)
    parser.add_argument('--end-hour', dest="end_hour", action="store", help="The start hour of the set. (HHMM).", type=int)
    parser.add_argument('--ubications', nargs='+', dest="ubications", action="store", help="Ubication codes.")
    parser.add_argument('--relative-radiation', dest="relative_radiation", action="store", help="Ubication codes.", type=bool)
    parser.add_argument('--destination-folder', dest="dest_folder", action="store", help="Folder to save the data.")

    arguments = parser.parse_args()

    config_file = arguments.config_file
    start_date = arguments.start_date
    end_date = arguments.end_date
    start_hour = arguments.start_hour
    end_hour = arguments.end_hour
    ubications = arguments.ubications
    relative_radiation = arguments.relative_radiation
    dest_folder = arguments.dest_folder

    info_riego_data = InfoRiegoData(start_date, end_date, start_hour, end_hour, ubications, relative_radiation, dest_folder, config_file)
    info_riego_data.generate_csv()

if __name__ == "__main__":
    main()
