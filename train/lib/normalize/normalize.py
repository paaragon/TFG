# -*- coding: utf-8 -*-

import pandas

class Normalization(object):

    @staticmethod
    def normalize(col):
        
        if col.max() - col.min() == 0:
            return col.max(), [col.mean(), col.max(), col.min()]

        return (col - col.mean()) / (col.max() - col.min()), [col.mean(), col.max(), col.min()]

    @staticmethod
    def normalize_csv(data_frame):

        norm_values = dict()
        for column in list(data_frame):
            data_frame[column], norm_values[column] = Normalization.normalize(data_frame[column])

        return data_frame, norm_values

    @staticmethod
    def denormalize(col_name, col, mean, mx, mn):

        i = 0
        for val in col:
            print 'Denormalizing ' + col_name + '-' + str(i) + '/' + str(len(col))
            val = val * (mx - mn) + mean
            i += 1

        return col

    @staticmethod
    def denormalize_csv(data_frame, reverse_norm_path):

        reverse_norm = pandas.read_json(reverse_norm_path)

        for col in list(data_frame):
            mean = reverse_norm[col][0]
            mx = reverse_norm[col][1]
            mn = reverse_norm[col][2]
            data_frame[col] = Normalization.denormalize(col, data_frame[col], mean, mx, mn)

        return data_frame
