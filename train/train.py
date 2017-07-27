"""This module search the best hyperparameters in a machine learning model"""

import json
import os
import time
import argparse
import copy
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
import train_data

class Train(object):
    """this class explore the hyperparameters of a machine learning model"""

    normalized_csv_path = None
    model_destination_folder = None
    model_file_name = None
    training_set_config = None
    estimator_config = None
    verbose = True

    def __init__(self, normalized_csv_path, model_destination_folder, model_file_name, training_set_config, estimator_config, verbose=True):

        self.normalized_csv_path = normalized_csv_path
        self.model_destination_folder = model_destination_folder
        self.model_file_name = model_file_name
        self.training_set_config = training_set_config
        self.estimator_config = estimator_config
        self.verbose = verbose

    def fit(self):
        """This method read files and iterate through described parameters"""

        if self.verbose:
            print "Starting grid search"

        k = self.training_set_config["n_samples"]
        destination_folder = self.training_set_config["destination_folder"]
        target_distance = self.training_set_config["target_distance"]
        original_prefix_column_names = self.training_set_config["original_prefix_column_names"]
        original_column_names = self.training_set_config["original_column_names"]
        x_prefix_column_names = self.training_set_config["x_prefix_column_names"]
        x_column_names = self.training_set_config["x_column_names"]
        y_colum_names = self.training_set_config["y_colum_names"]
        original_y_column_name = self.training_set_config["original_y_column_name"]

        total_time = time.time()

        file_time = time.time()
        if self.verbose:
            print "Exploring " + self.normalized_csv_path


        # This is a hack. Multiout is not supported yet but TrainData is
        # prepared for this so we must pass an array to TrainData not an int
        target = [target_distance]

        print "grid_search: x_prefix - " + str(x_prefix_column_names)

        train_sets = train_data.TrainData(self.normalized_csv_path, destination_folder, \
                        k, target, original_prefix_column_names, \
                        original_column_names, copy.copy(x_prefix_column_names), \
                        x_column_names, y_colum_names, original_y_column_name)

        x_destination_path, y_destination_path = train_sets.generate_train_data()
        x_set = pd.read_csv(x_destination_path)
        y_set = pd.read_csv(y_destination_path)

        if self.verbose:
            print "Tuning hyperparameters for k=" + str(k) + \
                    " and targets=" + str(target)

        for estimator in self.estimator_config:

            module_name = estimator["module"]
            class_name = estimator["class"]
            model_name = estimator["model"]
            tuned_parameters = estimator["parameters"]

            if estimator["map"] == "classification":
                y_set = self._map_y_classifier(y_set)

            elif estimator["map"] == "regression":
                y_set = self._map_y_regression(y_set)

            model = self._instance_model(module_name, class_name, model_name)

            clf = GridSearchCV(model, tuned_parameters, cv=3, \
                                scoring=estimator["scoring"])

            fit_time = time.time()

            trained_model = clf.fit(x_set, y_set)

            if self.verbose:
                print "Tuning done in {} seconds".format(time.time() - fit_time)
                print "Saving trained model"

            if not os.path.isdir(self.model_destination_folder):
                os.makedirs(self.model_destination_folder)

            destination_path = os.path.join(self.model_destination_folder, \
                                            self.model_file_name)

            self._save_model(trained_model, destination_path)

        if self.verbose:
            print "Train finished in {} seconds".format(time.time() - total_time)

    def _instance_model(self, module_name, class_name, model_name):
        """This method instances a model from scikit learn"""

        module = __import__(module_name)
        class_ = getattr(module, class_name)
        method = getattr(class_, model_name)

        return method()

    def _map_y_regression(self, y):
        """This method map the y set for regressions"""

        return y.values.ravel()

    def _map_y_classifier(self, y):
        """This method map the y set for classifiers"""

        mapped_y = []
        for i in range(y.shape[0]):
            # map 0 - 2000 => 0 - 100
            mapped_val = int(((y.iloc[i] + 1) / 2) * 100)
            mapped_y.append(mapped_val)

        return np.array(mapped_y,)

    def _get_file_name(self):
        pass

    def _save_model(self, model, path):
        print "Saving"
        joblib.dump(model, path)
        print "Saved"


def main():
    """main function of module"""

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config-file", nargs="?", action="store", \
                        dest="config_file", help="File with the parameters \
                        to configure the train")

    arguments = parser.parse_args()

    config_file = arguments.config_file

    with open(config_file) as data_file:
        config_data = json.load(data_file)

    normalized_csv_paths = config_data["normalized_csv_paths"]
    model_destination_folder = config_data["model_destination_folder"]
    model_file_name = config_data["model_file_name"]
    training_set_config = config_data["training_set_config"]
    estimator_config = config_data["estimator_config"]

    train = Train(normalized_csv_paths, model_destination_folder, model_file_name, \
                training_set_config, estimator_config)

    train.fit()

if __name__ == "__main__":
    main()
