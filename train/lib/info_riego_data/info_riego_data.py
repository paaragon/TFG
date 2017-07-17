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
    destination_folder = None
    config_file = None
    verbose = True

    def __init__(self, start_date=None, end_date=None, start_hour=None, end_hour=None, destination_folder=None, config_file=None, verbose=True):

        self.start_date = start_date
        self.end_date = end_date
        self.start_hour = end_hour
        self.destination_folder = destination_folder
        self.config_file = config_file

        self.parse_config_file()
        self.check_errors()

    def generate_csv(self):
        """This function downoads and concatenate the data in one csv file"""

        self._download_data()
        self._filter_and_unify_data()

    def _download_data(self):

        folder = os.path.join(self.destination_folder, 'info_riego_csv')
        dm = data_manager.DataManager(self.start_date, self.end_date, folder, verbose = self.verbose)
        dm.get_data()

    def _filter_and_unify_data(self):
        
        folder = os.path.join(self.destination_folder, 'unified_csv')
        csv = csv_manager.CsvManager(self.start_date, self.end_date, self.start_hour, self.end_hour, folder, verbose=self.verbose)
        csv.filter_and_unify_data()

    def parse_config_file(self):
        """This method parse the sef.config file and assign the values to attributes"""

        if self.config_file is not None:

            if self.verbose:
                print "Parsing config file"

            with open(self.config_file) as data_file:    
                self.config_data = json.load(data_file)

            if "start_date" in self.config_data:
                self.start_date = self.config_data["start_date"]

            if "end_date" in self.config_data:
                self.end_date = self.config_data["end_date"]

            if "start_hour" in self.config_data:
                self.start_hour = self.config_data["start_hour"]

            if "end_hour" in self.config_data:
                self.end_hour = self.config_data["end_hour"]

            if "dest_folder" in self.config_data:
                self.dest_folder = self.config_data["dest_folder"]

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

        elif self.dest_folder is None:
            raise Exception(7, "No dest_folder specified.")

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
    parser.add_argument('--dest-folder', dest="dest_folder", action="store", help="Folder to save the data.")
    
    arguments = parser.parse_args()

    config_file = arguments.config_file
    start_date = arguments.start_date
    end_date = arguments.end_date
    start_hour = arguments.start_hour
    end_hour = arguments.end_hour
    dest_folder = arguments.dest_folder

    info_riego_data = InfoRiegoData(config_file, start_date, end_date, start_hour, end_hour)
    info_riego_data.generate_csv()

if __name__ == "__main__":
    main()