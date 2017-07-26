"""This module search the best hyperparameters in a machine learning model"""

import json
import os
import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
import train_data

class GridSearch(object):
    """this class explore the hyperparameters of a machine learning model"""

    normalized_csv_paths = None
    results_destination_folder = None
    training_sets_config = None
    estimator_configs = None
    verbose = True

    def __init__(self, normalized_csv_paths, results_destination_folder, training_sets_config, estimator_configs, verbose=True):

        self.normalized_csv_paths = normalized_csv_paths
        self.results_destination_folder = results_destination_folder
        self.training_sets_config = training_sets_config
        self.estimator_configs = estimator_configs
        self.verbose = verbose

    def explore(self):
        """This method read files and iterate through described parameters"""

        if self.verbose:
            print "Starting grid search"

        for normalized_csv_path in self.normalized_csv_paths:

            k_list = self.training_sets_config["n_samples"]
            target_distances = self.training_sets_config["target_distances"]

            for k in k_list:
                for targets in target_distances:

                    train_sets = train_data.TrainData(normalized_csv_path, \
                                    self.training_sets_config["destination_folder"], \
                                    k, \
                                    targets, \
                                    self.training_sets_config["original_prefix_column_names"], \
                                    self.training_sets_config["original_column_names"], \
                                    self.training_sets_config["x_prefix_column_names"], \
                                    self.training_sets_config["x_column_names"], \
                                    self.training_sets_config["y_colum_names"], \
                                    self.training_sets_config["original_y_column_name"], \
                                    )

                    x_destination_path, y_destination_path = train_sets.generate_train_data()
                    x_set = pd.read_csv(x_destination_path)
                    y_set = pd.read_csv(y_destination_path)

                    if self.verbose:
                        print "Tuning hyperparameters for k=" + str(k) + \
                                " and targets=" + str(targets)

                    for estimator in self.estimator_configs:

                        module_name = estimator["module"]
                        class_name = estimator["class"]
                        model_name = estimator["model"]
                        tuned_parameters = estimator["parameters"]

                        if estimator["map"] == "classifier":
                            y_set = self.map_y_classifier(y_set)

                        elif estimator["map"] == "regression":
                            y_set = self.map_y_regression(y_set)

                        model = self.instance_model(module_name, class_name, model_name)

                        clf = GridSearchCV(model, tuned_parameters, cv=3, \
                                            scoring=estimator["scoring"])

                        clf.fit(x_set, y_set)

                        if self.verbose:
                            print "Tuning done. Saving results"

                        means = clf.cv_results_["mean_test_score"]
                        stds = clf.cv_results_["std_test_score"]

                        if not os.path.isdir(self.results_destination_folder):
                            os.makedirs(self.results_destination_folder)

                        destination_path = os.path.join(self.results_destination_folder, \
                                                        estimator["model"] + ".csv")

                        with open(destination_path, "a") as csvfile:
                            for mean, std, params in zip(means, stds, clf.cv_results_["params"]):
                                print "%f (+/-%f) for %r" % (mean, std * 2, params)
                                csvfile.write("{};{};{};{};{};{};{};{}\n".format(
                                    normalized_csv_path, \
                                    model_name, \
                                    k, \
                                    targets, \
                                    mean, \
                                    std * 2, \
                                    params, \
                                    clf.best_params_))

        print "Test finished"

    def instance_model(self, module_name, class_name, model_name):
        """This method instances a model from scikit learn"""

        module = __import__(module_name)
        class_ = getattr(module, class_name)
        method = getattr(class_, model_name)

        return method()

    def map_y_regression(self, y):
        """This method map the y set for regressions"""
        return y.values.ravel()

    def map_y_classifier(self, y):
        """This method map the y set for classifiers"""

        mapped_y = []
        for i in range(y.shape[0]):
            # map 0 - 2000 => 0 - 100
            mapped_val = int(((y.iloc[i] + 1) / 2) * 100)
            mapped_y.append(mapped_val)

        return np.array(mapped_y,)


def main():
    """main function of module"""

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config-file", nargs="?", action="store", \
                        dest="config_file", help="File with the parameters \
                        download the data. It can only contain some parameters  \
                        and specify the others by cli.")

    arguments = parser.parse_args()

    config_file = arguments.config_file

    with open(config_file) as data_file:
        config_data = json.load(data_file)

    normalized_csv_paths = config_data["normalized_csv_paths"]
    results_destination_folder = config_data["results_destination_folder"]
    training_sets_config = config_data["training_sets_config"]
    estimator_configs = config_data["estimator_configs"]

    grid = GridSearch(normalized_csv_paths, results_destination_folder, \
                training_sets_config, estimator_configs)

    grid.explore()

if __name__ == "__main__":
    main()
