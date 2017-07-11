#!usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import argparse
import pandas as pd

def generate_train_data(config_file="", csv_file=None, n_samples=0, target_distance=[],  \
                        orig_cols=None, orig_prefix_cols=[], x_cols=None, x_prefix_cols=[], y_cols=None):
    """
    This function generates data sets (x, y) to use them in training and save then in disk

        Params:
        
        - config_file: File with the parameters to generate the sets. It can only contain some parameters and specify passing them by parameter.
        - csv_file: File with original data..
        - n_samples: Number of samples of the original set to add in a row of the X set.
        - target_distance: Number of samples ahead where the ground truth is. More than one value is accepted.In that case, a multioutput Y set will be generated.
        - orig_cols: Column names of the original set.
        - orig_prefix_cols: Name of the first column names in the original set that shoul be included only once per row in the X set.
        - x_cols: Column names of the X set.
        - x_prefix_cols: Name of the first column names in the X set that shoul be included only once per row in the X set.
        - y_cols: Column names of the Y set.

        Return:

        - Tuple: x_destination_path, y_destination_path
    """

    # columns is an array with column names of the destination data frame
    # it can be used to name the source set headers
    x_columns = ['codigo', 'fecha']

    for i in range(conditions['nSamples']):
        x_columns.append('hora' + str(i))
        x_columns.append('temperatura' + str(i))
        x_columns.append('humedad' + str(i))
        x_columns.append('radiacion' + str(i))

    x_columns.append('targetHour')

    y_columns = ['radiacion']

    # opening the original set
    if original_set_path is None:
        print "No source file specified"
        return

    data_frame = pd.read_csv(original_set_path)

    if verbose:
        print 'Creating column list'

    # initializing both sets
    x_set = []
    y_set = []

    # this variable is used only for show the progress
    percentage = -1

    # MAIN loop of the function
    # loop over original data obtaining the rows of both destination sets
    i = 0
    for index in range(len(data_frame.index) \
                       - conditions['n_samples'] \
                       - conditions['relative_target_sample']):

        # print progress
        perc = i * 100 / len(data_frame.index)
        if verbose and perc != percentage:
            print 'Apending row. ' \
                   + str(i) + '/' \
                   + str(len(data_frame.index)) \
                   + '. ' \
                   + str(perc) \
                   + '%'

            percentage = perc
        # END print progress

        # new row to append in the X set
        x_row = []
        y_row = []

        # adding two firsts columns
        x_row.append(data_frame['codigo'].iloc[index])
        x_row.append(data_frame['fecha'].iloc[index])

        # add the rest of the columns (it depends on the n_samples per row)
        j = 0
        for j in range(conditions['n_samples']):
            x_row.append(data_frame['hora'].iloc[index + j])
            x_row.append(data_frame['temperatura'].iloc[index + j])
            x_row.append(data_frame['humedad'].iloc[index + j])
            x_row.append(data_frame['radiacion'].iloc[index + j])

        # appending x_row to x_set
        x_set.append(x_row)

        # appending the relative target sample radiation to y_row
        y_row.append(data_frame['radiacion'].iloc[index  \
                                             + j \
                                             + conditions['relative_target_sample']])

        # increment index before next loop
        i += 1

    # create Data Frame with result values
    x_df = pd.DataFrame(data=x_set, columns=x_columns)
    y_df = pd.DataFrame(data=y_set, columns=y_columns)

    # checking if folder exists. If not, creates it
    dir_name = os.path.dirname(destination_folder)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    # generating the file names
    x_file_name = os.path.splitext(original_set_path)[0] + '-x.csv'
    y_file_name = os.path.splitext(original_set_path)[0] + '-y.csv'

    # generating the file paths
    x_destination_path = os.path.join(destination_folder, x_file_name)
    y_destination_path = os.path.join(destination_folder, y_file_name)

    x_df.to_csv(x_destination_path)
    y_df.to_csv(y_destination_path)

    return x_destination_path, y_destination_path

def main():
    """Main function to execute this scripts from cli"""

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config-file', nargs='?', action="store", dest="config_file", default="", help="File with the parameters to generate the sets. It can only contain some parameters and specify the others by cli.")
    parser.add_argument('-f', '--file', nargs='?', action="store", dest="csv_file", help="File with original data.")
    parser.add_argument('-n', '--n-samples', nargs='?', dest="n_samples", help="Number of samples of the original set to add in a row of the X set.", type=int)
    parser.add_argument('-t','--target-distance', nargs='?', dest="target_distance", help="Number of samples ahead where the ground truth is. More than one value is accepted.In that case, a multioutput Y set will be generated.")
    parser.add_argument('--orig-cols', nargs='*', dest="orig_cols", help="Column names of the original set.")
    parser.add_argument('--orig-prefix-cols', nargs='*', dest="orig_prefix_cols", help="Name of the first column names in the original set that shoul be included only once per row in the X set.")
    parser.add_argument('--x-cols', nargs='*', dest="x_cols", help="Column names of the X set.")
    parser.add_argument('--x-prefix-cols', nargs='*', dest="x_prefix_cols", help="Name of the first column names in the X set that shoul be included only once per row in the X set.")
    parser.add_argument('--y-cols', nargs='*', dest="y_cols", help="Column names of the Y set.")

    arguments = parser.parse_args()

    config_file = arguments.config_file
    csv_file = arguments.config_file
    n_samples = arguments.n_samples
    target_distance = arguments.target_distance
    orig_cols = arguments.orig_cols
    orig_prefix_cols = arguments.orig_prefix_cols
    x_cols = arguments.x_cols
    x_prefix_cols = arguments.x_prefix_cols
    y_cols = arguments.y_cols

    generate_train_data(config_file, csv_file, n_samples, target_distance,  \
                        orig_cols, orig_prefix_cols, x_cols, x_prefix_cols, y_cols)

if __name__ == '__main__':
    main()
