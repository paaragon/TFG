#!usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import argparse
import json
import pandas as pd

class TrainData(object):
    """
    This class generates data sets (x, y) to use them in training and save then in disk.
    """

    config_file = ""
    orig_csv_file_path = None
    dest_folder = None
    n_samples = 1
    target_distances = None
    orig_cols = None
    orig_prefix_cols = []
    x_cols = None
    x_prefix_cols = []
    y_cols = None
    orig_y_col = None
    verbose = True

    def __init__(self, orig_csv_file_path=None, dest_folder=None, n_samples=1, \
                    target_distances=None, orig_prefix_cols=[], orig_cols=None, x_prefix_cols=[], \
                    x_cols=None, y_cols=None, orig_y_col=None, config_file=None, verbose=True):
        """
        This class generates data sets (x, y) to use them in training and save then in disk

            Constructor params:

            - config_file: File with the parameters to generate the sets. It can only contain some parameters and specify passing them by parameter.
            - csv_file: File with original data..
            - n_samples: Number of samples of the original set to add in a row of the X set.
            - target_distance: Number of samples ahead where the ground truth is. More than one value is accepted.In that case, a multioutput Y set will be generated.
            - orig_cols: Column names of the original set.
            - orig_prefix_cols: Name of the first column names in the original set that shoul be included only once per row in the X set.
            - x_cols: Column names of the X set.
            - x_prefix_cols: Name of the first column names in the X set that shoul be included only once per row in the X set.
            - y_cols: Column names of the Y set.
        """

        self.config_file = config_file
        self.orig_csv_file_path = orig_csv_file_path
        self.dest_folder = dest_folder
        self.n_samples = n_samples
        self.target_distances = target_distances
        self.orig_cols = orig_cols
        self.orig_prefix_cols = orig_prefix_cols
        self.x_cols = x_cols
        self.x_prefix_cols = x_prefix_cols
        self.y_cols = y_cols
        self.orig_y_col = orig_y_col
        self.verbose = verbose

        # parsing the config fle and checking errors
        self.parse_config_file()
        self.check_errors()

    def generate_train_data(self):
        """
        Main function that generates the sets

        - Tuple: x_destination_path, y_destination_path.
        """

        # if files exists, we don't regenerate them
        x_destination_path, y_destination_path = self.get_file_names()
        if os.path.isfile(x_destination_path) and \
            os.path.isfile(y_destination_path):

            return x_destination_path, y_destination_path

        # x_columns is an array that starts with the name of some prefix columns
        x_columns = self.generate_x_columns()

        # the y column names.
        y_columns = self.y_cols

        # opening the original set
        data_frame = pd.read_csv(self.orig_csv_file_path)

        # initializing both sets
        x_set = []
        y_set = []

        # this variable is used only for show the progress
        percentage = -1

        # MAIN loop of the function
        # loop over original data obtaining the rows of both destination sets
        i = 0
        for index in range(len(data_frame.index) \
                                - self.n_samples \
                                - self.target_distances[len(self.target_distances) - 1]):

            # printing the progress
            if self.verbose:
                percentage = self.print_progress(len(data_frame.index), i, percentage)

            # new row to append in the X set
            x_row = []
            y_row = []

            # adding two firsts columns
            for col in self.orig_prefix_cols:
                x_row.append(data_frame[col].iloc[index])

            # add the rest of the columns (it depends on the n_samples per row)
            j = 0
            for j in range(self.n_samples):
                for col in self.orig_cols:
                    x_row.append(data_frame[col].iloc[index + j])

            # appending x_row to x_set
            x_set.append(x_row)

            # appending the relative target samples to y_row
            for k in self.target_distances:
                y_row.append(data_frame[self.orig_y_col].iloc[index + j + k].values[0])

            # appending y_row to y_set
            y_set.append(y_row)

            # increment index before next loop
            i += 1

        return self.save_data_frames(x_set, x_columns, y_set, y_columns)

    def generate_x_columns(self):
        """this function generates the column names in the X set."""

        # first, the prefixes column names
        x_columns = self.x_prefix_cols

        # appending the rest of the column names 
        for i in range(self.n_samples):
            for col in self.x_cols:
                x_columns.append(col + str(i))

        return x_columns

    def save_data_frames(self, x_set, x_columns, y_set, y_columns):
        """
        This method save the dataframes in disk.

        Params:

        - x_set: the matrix with X set data.
        - x_columns: the column names of the X set.
        - y_set: the matrix with Y set data.
        - y_columns: the column names of the Y set.
        """

        # create Data Frame with result values
        x_df = pd.DataFrame(data=x_set, columns=x_columns)
        y_df = pd.DataFrame(data=y_set, columns=y_columns)

        # checking if folder exists. If not, creates it
        if not os.path.isdir(self.dest_folder):
            os.makedirs(self.dest_folder)

        # generating the file paths
        x_destination_path, y_destination_path = self.get_file_names()

        # saving sets in disk
        x_df.to_csv(x_destination_path, index=False)
        y_df.to_csv(y_destination_path, index=False)

        return x_destination_path, y_destination_path

    def get_file_names(self):
        """This method return the x and y file names"""

        base_file_name = os.path.splitext(os.path.basename(self.orig_csv_file_path))[0]

        target_identifier = ':'.join(str(x) for x in self.target_distances)

        file_identifier = base_file_name \
                          + "-" + str(self.n_samples) \
                          + "-" + target_identifier

        # generating the file names
        x_file_name = file_identifier +'-x.csv'
        y_file_name = file_identifier + '-y.csv'

        # generating the file paths
        x_destination_path = os.path.join(self.dest_folder, x_file_name)
        y_destination_path = os.path.join(self.dest_folder, y_file_name)

        return x_destination_path, y_destination_path

    def check_errors(self):
        """ This method check if all the variables have the correct values """

        if self.orig_csv_file_path is None:
            raise Exception(1, "No source file specified")

        elif self.dest_folder is None:
            raise Exception(2, "No destination folder specified.")

        elif self.n_samples < 1:
            raise Exception(3, "n_samples should be greater or equal than 1.")

        elif self.target_distances is None:
            raise Exception(4, "No target_distances specified.")

        elif len(self.target_distances) < 1:
            raise Exception(5, "At least one target distance must be specified.")

        elif self.orig_cols is None:
            raise Exception(6, "No orig_cols specified.")

        elif self.x_cols is None:
            raise Exception(7, "No column names specified for X set.")

        elif self.y_cols is None:
            raise Exception(7, "No column names specified for Y set.")

        elif self.orig_y_col is None:
            raise Exception(8, "No target column name specified for Y set.")

    def parse_config_file(self):
        """This method parse the sef.config file and assign the values to attributes"""

        if self.config_file is not None:

            if self.verbose:
                print "Parsing config file"

            with open(self.config_file) as data_file:    
                self.config_data = json.load(data_file)

            if "original_csv_file_path" in self.config_data:
                self.orig_csv_file_path = self.config_data["original_csv_file_path"]

            if "destination_folder" in self.config_data:
                self.dest_folder = self.config_data["destination_folder"]

            if "n_samples" in self.config_data:
                self.n_samples = self.config_data["n_samples"]

            if "target_distances" in self.config_data:
                self.target_distances = self.config_data["target_distances"]

            if "original_prefix_column_names" in self.config_data:
                self.orig_prefix_cols = self.config_data["original_prefix_column_names"]

            if "original_column_names" in self.config_data:
                self.orig_cols = self.config_data["original_column_names"]

            if "x_prefix_column_names" in self.config_data:
                self.x_prefix_cols = self.config_data["x_prefix_column_names"]

            if "x_column_names" in self.config_data:
                self.x_cols = self.config_data["x_column_names"]

            if "y_colum_names" in self.config_data:
                self.y_cols = self.config_data["y_colum_names"]

            if "original_y_column_name" in self.config_data:
                self.orig_y_col = self.config_data["original_y_column_name"]

    def print_progress(self, df_len, index, actual_percentage):
        """ This function print the generating sets progress """

        perc = index * 100 / df_len
        if perc != actual_percentage:
            print 'Apending row. ' \
                + str(index) + '/' \
                + str(df_len) \
                + '. ' \
                + str(perc) \
                + '%'

            actual_percentage = perc

        return actual_percentage

def main():
    """Main function to execute this scripts from cli"""

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config-file', nargs='?', action="store", dest="config_file", help="File with the parameters to generate the sets. It can only contain some parameters and specify the others by cli.")
    parser.add_argument('-f', '--file', nargs='?', action="store", dest="orig_csv_file_path", help="File with original data.")
    parser.add_argument('-d', '--dest-folder', nargs='?', action="store", dest="dest_folder", help="Path of the destination folder to save the sets.")
    parser.add_argument('-n', '--n-samples', nargs='?', dest="n_samples", help="Number of samples of the original set to add in a row of the X set.", type=int)
    parser.add_argument('-t','--target-distances', nargs='?', dest="target_distances", help="Number of samples ahead where the ground truth is. More than one value is accepted.In that case, a multioutput Y set will be generated.")
    parser.add_argument('--orig-prefix-cols', nargs='*', dest="orig_prefix_cols", help="Name of the first column names in the original set that shoul be included only once per row in the X set.")
    parser.add_argument('--orig-cols', nargs='*', dest="orig_cols", help="Column names of the original set.")
    parser.add_argument('--x-prefix-cols', nargs='*', dest="x_prefix_cols", help="Name of the first column names in the X set that shoul be included only once per row in the X set.")
    parser.add_argument('--x-cols', nargs='*', dest="x_cols", help="Column names of the X set.")
    parser.add_argument('--y-cols', nargs='*', dest="y_cols", help="Column names of the Y set.")
    parser.add_argument('--orig-y-col', nargs='*', dest="orig_y_cols", help="Column names of the Y set.")

    arguments = parser.parse_args()

    config_file = arguments.config_file
    orig_csv_file_path = arguments.orig_csv_file_path
    dest_folder = arguments.dest_folder
    n_samples = arguments.n_samples
    target_distances = arguments.target_distances
    orig_prefix_cols = arguments.orig_prefix_cols
    orig_cols = arguments.orig_cols
    x_prefix_cols = arguments.x_prefix_cols
    x_cols = arguments.x_cols
    y_cols = arguments.y_cols
    orig_y_col = arguments.orig_y_cols

    train_data = TrainData(orig_csv_file_path, dest_folder, n_samples, \
                            target_distances, orig_prefix_cols, orig_cols, x_prefix_cols, \
                            x_cols, y_cols, orig_y_col, config_file)

    x_file_path, y_file_path = train_data.generate_train_data()

    print "Generation of train sets finished."
    print "X file path:", x_file_path
    print "Y file path:", y_file_path

if __name__ == '__main__':
    main()
