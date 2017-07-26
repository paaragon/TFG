# -*- coding: utf-8 -*-

import os
import json
import datetime
import argparse
import pandas
from solar_model import solar_model

class CsvManager(object):

    start_date = None
    end_date = None
    start_hour = None
    end_hour = None
    ubications = []
    relative_radiation = False
    orig_folder = None
    dest_folder = None
    config_file = None
    verbose = True
    columns = ['codigo', 'fecha', 'hora',
                       'temperatura', 'humedad', 'radiacion']
    orig_columns = ['Codigo', 'Fecha (AAAA-MM-DD)', 'Hora (HHMM)',
                   'Temperatura (oC)', 'Humedad relativa (%)', 'Radiacion (W/m2)']

    def __init__(self, start_date=None, end_date=None, start_hour=None, end_hour=None, ubications=None, relative_radiation=False, orig_folder=None, dest_folder=None, config_file=None, verbose=True):

        self.start_date = start_date
        self.end_date = end_date
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.ubications = ubications
        self.relative_radiation = relative_radiation
        self.orig_folder = orig_folder
        self.dest_folder = dest_folder
        self.config_file = config_file
        self.verbose = verbose

        self.parse_config_file()
        self.check_errors()

    def filter_data(self):

        file_name = self._get_file_name()
        
        if os.path.isfile(os.path.join(self.dest_folder, "original", file_name + ".csv")):
            print "Filtered CSV already exists: " + file_name
            return None

        csv_files = self._get_csv_files()

        if len(csv_files) == 0:
            print "No csv files found."
            return None

        csv_files = sorted(csv_files)

        df = pandas.DataFrame(columns=self.columns)

        df = self._merge_csv_files(df, csv_files)

        df = self._patch_csv_df(df)

        df = df.sort_values(by=['codigo', 'fecha', 'hora'], ascending=True)

        df_norm, norm_values = self._normalize_csv(df.copy())

        self._save_csv(df, df_norm, norm_values)

    def _save_csv(self, data_frame, df_norm, norm_values):
        """
        This function saves the original df, the normalized df and the necesary data to denormalize
        """

        # Name of the file in the three folders
        file_name = self._get_file_name()

        # if base folder doesn't exist create it
        print self.dest_folder
        if not os.path.isdir(self.dest_folder):
            os.makedirs(self.dest_folder)

        # destination folders for the three files
        destination_orig_df_folder = os.path.join(self.dest_folder, "original")
        destination_norm_df_folder = os.path.join(self.dest_folder, "normalized")
        destination_norm_data_folder = os.path.join(self.dest_folder, "norm_data")

        # if destination folders doesn't exists we create them
        if not os.path.isdir(destination_orig_df_folder):
            os.makedirs(destination_orig_df_folder)

        if not os.path.isdir(destination_norm_df_folder):
            os.makedirs(destination_norm_df_folder)

        if not os.path.isdir(destination_norm_data_folder):
            os.makedirs(destination_norm_data_folder)

        # saving original df
        original_path = os.path.join(destination_orig_df_folder, file_name + ".csv")
        data_frame.to_csv(original_path, index=False)

        # saving normalized df
        normalized_path = os.path.join(destination_norm_df_folder, file_name + ".csv")
        df_norm.to_csv(normalized_path, index=False)

        # saving denorm data
        norm_data_path = os.path.join(destination_norm_data_folder, file_name + ".csv")

        with open(norm_data_path, 'w') as outfile:
            json.dump(norm_values, outfile)

    def _filter_csv_df(self, df):

        return df[(df['hora'] >= self.start_hour)
                  & (df['hora'] <= self.end_hour)
                  & (df['codigo'].isin(self.ubications))]

    def _merge_csv_files(self, df, csv_files):

        i = 0
        for f in csv_files:

            i += 1
            if self.verbose:
                print 'Concatenating ' + f + '(' + str(i) + '/' + str(len(csv_files)) + ')'

            aux_path = os.path.join(self.orig_folder, f)

            df_aux = pandas.read_csv(aux_path, ';', usecols=self.orig_columns)
            df_aux.columns = self.columns

            df_aux = self._filter_csv_df(df_aux)

            df = df.append(df_aux)

        return df

    def _get_csv_files(self):

        return [f for f in os.listdir(self.orig_folder)
                if f[:8].isdigit()
                and int(f[:8]) >= self.start_date]

    def _patch_csv_df(self, df):

        print "Patching csv"

        df['fecha'] = df['fecha'].str.replace('-', '').astype(float)

        df.loc[df['fecha'] == 20120406, 'fecha'] = 20150206
        df.loc[df['fecha'] == 20120408, 'fecha'] = 20150208
        df.loc[df['fecha'] == 20120511, 'fecha'] = 20150118
        df.loc[df['fecha'] == 20120526, 'fecha'] = 20150622
        df.loc[df['fecha'] == 20120607, 'fecha'] = 20150409
        df.loc[df['fecha'] == 20130429, 'fecha'] = 20150329
        df.loc[df['fecha'] == 20120714, 'fecha'] = 20150516
        df.loc[df['fecha'] == 20130502, 'fecha'] = 20150401
        df.loc[df['fecha'] == 20130525, 'fecha'] = 20150424
        df.loc[df['fecha'] == 20130612, 'fecha'] = 20150512
        df.loc[df['fecha'] == 20140129, 'fecha'] = 20150111
        df.loc[df['fecha'] == 20140624, 'fecha'] = 20150606
        df.loc[df['fecha'] == 20140624, 'fecha'] = 20150606
        df.loc[df['fecha'] == 20140626, 'fecha'] = 20150608
        df.loc[df['fecha'] == 20140628, 'fecha'] = 20150610

        print 'patching hour'
        for i, hora in enumerate(df['hora'].unique()):
            h_aux = hora / 100
            h_aux += hora % 100 / 60.0
            df.loc[df['hora'] == hora, 'hora'] = h_aux

        print 'patching date'
        for i, fecha in enumerate(df['fecha'].unique()):
            dt = datetime.datetime.strptime(str(int(fecha)), "%Y%m%d")
            df.loc[df['fecha'] == fecha, 'fecha'] = int(datetime.datetime.strftime(dt, "%j"))

        print 'patching code'
        for i, codigo in enumerate(df['codigo'].unique()):
            # i + 1 para que al normalizar no divida entre 0
            df.loc[df['codigo'] == codigo, 'codigo'] = i + 1

        if self.relative_radiation:
            print 'patching radiation'
            for i, radiacion in enumerate(df['radiacion'].unique()):
                hora = df.loc[df['radiacion'] == radiacion, 'hora'].values[0]
                fecha = df.loc[df['radiacion'] == radiacion, 'fecha'].values[0]
                model = 'robledo'

                relative_rad = df.loc[df['radiacion'] == radiacion, 'radiacion'] / solar_model.get_ghi(fecha, hora, model)
                df.loc[df['radiacion'] == radiacion, 'radiacion'] = relative_rad

        return df

    def _get_file_name(self):

        ubication_name = ":".join(self.ubications)
        relative = "r" if self.relative_radiation else ""

        return str(self.start_date) + ":" + str(self.start_hour) + "-" \
               + str(self.end_date) + ":" + str(self.end_hour) + "-" + ubication_name \
               + relative


    def _normalize(self, col):

        if col.max() - col.min() == 0:
            return col.max(), [col.mean(), col.max(), col.min()]

        return (col - col.mean()) / (col.max() - col.min()), [col.mean(), col.max(), col.min()]

    def _normalize_csv(self, data_frame):

        norm_values = dict()
        for column in list(data_frame):
            data_frame[column], norm_values[column] = self._normalize(data_frame[column])

        return data_frame, norm_values


    def parse_config_file(self):
        """This method parse the sef.config file and assign the values to attributes"""

        if self.config_file is not None:

            if self.verbose:
                print "Parsing config file"

            with open(self.config_file) as data_file:
                config_data = json.load(data_file)

            if "start_date" in config_data:
                self.start_date = int(config_data["start_date"])

            if "end_date" in config_data:
                self.end_date = int(config_data["end_date"])

            if "start_hour" in config_data:
                self.start_hour = int(config_data["start_hour"])

            if "end_hour" in config_data:
                self.end_hour = int(config_data["end_hour"])

            if "ubications" in config_data:
                self.ubications = config_data["ubications"]

            if "relative_radiation" in config_data:
                self.relative_radiation = config_data["relative_radiation"]

            if "original_folder" in config_data:
                self.orig_folder = config_data["original_folder"]

            if "destination_folder" in config_data:
                self.dest_folder = config_data["destination_folder"]

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

        elif self.start_date > self.end_date:
            raise Exception(7, "start_date greater than end_date.")

        elif self.start_hour > self.end_hour:
            raise Exception(7, "start_hour greater than end_hour.")

        elif self.ubications is None:
            raise Exception(7, "No ubications specified.")

        elif self.dest_folder is None:
            raise Exception(7, "No destination_folder specified.")

        elif self.orig_folder is None:
            raise Exception(7, "No original_folder specified.")
def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config-file', nargs='?', action="store", dest="config_file", help="File with the parameters download the data. It can only contain some parameters and specify the others by cli.")
    parser.add_argument('--start-date', dest="start_date", action="store", help="The start date of the set. (YYYYMMDD).", type=int)
    parser.add_argument('--end-date', dest="end_date", action="store", help="The end date of the set. (YYYYMMDD).", type=int)
    parser.add_argument('--start-hour', dest="start_hour", action="store", help="The start hour of the set. (HHMM).", type=int)
    parser.add_argument('--end-hour', dest="end_hour", action="store", help="The start hour of the set. (HHMM).", type=int)
    parser.add_argument('--ubications', nargs='+', dest="ubications", action="store", help="Ubication codes.")
    parser.add_argument('--relative-radiation', dest="relative_radiation", action="store", help="Ubication codes.", type=bool)
    parser.add_argument('--original-folder', dest="orig_folder", action="store", help="The folder where the original data is.")
    parser.add_argument('--destination-folder', dest="dest_folder", action="store", help="Folder to save the data.")

    arguments = parser.parse_args()

    config_file = arguments.config_file
    start_date = arguments.start_date
    end_date = arguments.end_date
    start_hour = arguments.start_hour
    end_hour = arguments.end_hour
    ubications = arguments.ubications
    relative_radiation = arguments.relative_radiation
    orig_folder = arguments.orig_folder
    dest_folder = arguments.dest_folder

    csv_manager = CsvManager(start_date, end_date, start_hour, end_hour, ubications, relative_radiation, orig_folder, dest_folder, config_file)
    csv_manager.filter_data()

if __name__ == "__main__":
    main()

