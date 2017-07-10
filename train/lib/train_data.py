#!usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import pandas as pd

def generate_train_data(conditions, original_set_path=None, destination_folder=None, verbose=True):
    """
    This function generates data sets (x, y) to use them in training and save then in disk

        - conditions: an object width the conditions of the sets.
        - source_path: the path of the original set.
        - destination_folder: destination path of the folder to save the sets (only the path to the
            folder, not the path to the files)

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

    conditions = dict()
    conditions['relative_target_sample'] = 2
    conditions['n_samples'] = 4

    generate_train_data(conditions, '../data/csvWithCondition/2015.csv', '../data/xy')

if __name__ == '__main__':
    main()
