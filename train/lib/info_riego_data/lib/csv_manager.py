import os
import json
import datetime
import pandas

class CsvManager(object):

    start_date = None
    end_date = None
    start_hour = None
    end_hour = None
    ubications = []
    orig_folder = None
    dest_folder = None
    config_file = None
    verbose = True
    columns = ['codigo', 'fecha', 'hora',
                       'temperatura', 'humedad', 'radiacion']
    orig_columns = ['Codigo', 'Fecha (AAAA-MM-DD)', 'Hora (HHMM)',
                   'Temperatura (oC)', 'Humedad relativa (%)', 'Radiacion (W/m2)']

    def __init__(self, start_date=None, end_date=None, start_hour=None, end_hour=None, ubications=None, orig_folder=None, dest_folder=None, config_file=None, verbose=True):
        
        self.start_date = start_date
        self.end_date = end_date
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.orig_folder = orig_folder
        self.dest_folder = dest_folder
        self.config_file = config_file
        self.verbose = verbose
        self.ubications = ubications

    def filter_and_unify_data(self):

        csv_files = self._get_csv_files()

        if len(csv_files):
            print "No csv files found."
            return None

        csv_files = sorted(csv_files)

        df = pandas.DataFrame(columns=self.columns)
        df = self._merge_csv_files(df, csv_files)
        df = self._patch_csv_df(df)
        df_norm, norm_values = self._normalize_csv(df)
        self._save_csv(df, df_norm, norm_values)

    def _save_csv(self, data_frame, df_norm, norm_values):
        """
        This function saves the original df, the normalized df and the necesary data to denormalize
        """

        # Name of the file in the three folders
        file_name = self.start_date + ":" + self.start_hour + "-" + self.end_date + ":" + self.end_hour

        # if base folder doesn't exist create it
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
        original_path = os.path.join(destination_orig_df_folder, file_name, ".csv")
        data_frame.to_csv(original_path, index=False)

        # saving normalized df
        normalized_path = os.path.join(destination_norm_df_folder, file_name, ".csv")
        df_norm.to_csv(normalized_path, index=False)

        # saving denorm data
        norm_data_path = os.path.join(destination_norm_data_folder, file_name, ".json")

        with open(norm_data_path, 'w') as outfile:
            json.dump(norm_values, outfile)

    def _filter_csv_df(self, df):

        df = pandas.DataFrame(df[(df['hora'] >= self.start_hour)
                                 & (df['hora'] <= self.end_hour)
                                 & (df['codigo'].isin(self.ubications))])

        return df

    def _merge_csv_files(self, df, csv_files):

        i = 0
        for f in csv_files:

            i += 1
            if self.verbose:
                print 'Reading ' + f + '(' + str(i) + '/' + str(len(csv_files)) + ')'

            aux_path = os.path.join(self.orig_folder, f)
            df_aux = pandas.read_csv(aux_path, ';', usecols=self.orig_columns)

            df_aux.columns = self.columns

            df = df.append(df_aux)

        return df.sort_values(by=['codigo', 'fecha', 'hora'], ascending=True)

    def _get_csv_files(self):

        return [f for f in os.listdir(self.orig_folder)
                    if f[:8].isdigit()
                    and int(f[:8]) >= self.start_date]

    def _patch_csv_df(self, df):

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

        for i, hora in enumerate(df['hora'].unique()):
            h_aux = hora / 100
            h_aux += hora % 100 / 60.0
            df.loc[df['hora'] == hora, 'hora'] = h_aux

        for i, fecha in enumerate(df['fecha'].unique()):
            dt = datetime.datetime.strptime(fecha, "%Y%m%d")
            df.loc[df['fecha'] == fecha, 'fecha'] = datetime.datetime.strftime("%j", dt)

        return df

    def _normalize(self, col):

        if col.max() - col.min() == 0:
            return col.max(), [col.mean(), col.max(), col.min()]

        return (col - col.mean()) / (col.max() - col.min()), [col.mean(), col.max(), col.min()]

    def _normalize_csv(self, df):

        norm_values = dict()

        for column in list(df):
            df[column], norm_values[column] = self._normalize(df[column])

        return df, norm_values

# TODO main method tu use this class from cli
