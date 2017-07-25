"""This module search the best hyperparameters in a machine learning model"""

import json
import os
import numpy as np
from sklearn.model_selection import GridSearchCV
import argparse
from train_data import info_riego_data

class GridSearch(object):
    """this class explore the hyperparameters of a machine learning model"""

    normalized_csv_path = None
    estimator_config = None

    def __init__(self, normalized_csv_path, estimator_config):
        self.normalized_csv_path = normalized_csv_path
        self.estimator_config = estimator_config

    def instance_model(self, module_name, class_name, model_name):
        module = __import__(module_name)
        class_ = getattr(module, class_name)
        method = getattr(class_, model_name)
        return method()

    def y_regression(self, y):
        return y.values.ravel()

    def y_mlp(self, y):
        mapped_y = []
        for i in range(y.shape[0]):
            # map 0 - 2000 => 0 - 100
            map = int(((y.iloc[i] + 1) / 2) * 100)
            mapped_y.append(map)

        return np.array(mapped_y,)

    def explore(self, file_path):
        """This method read files and iterate through described parameters"""

        with open(file_path) as data_file:
            conf = json.load(data_file)

        k_list = conf['k']
        start_date = conf['startDate']
        end_date = conf['endDate']
        start_hour = conf['startHour']
        end_hour = conf['endHour']

        relative_target = conf['relative_target']

        print str(start_date)
        print str(end_date)

        for k in k_list:
            for estimator in conf['estimator']:

                module_name = estimator["module"]
                class_name = estimator["class"]
                model_name = estimator["model"]
                tuned_parameters = estimator["parameters"]

                for target in relative_target:

                    x_set, y_set = self.get_data_set(start_date, end_date, start_hour, end_hour, k, target)

                    print "X shape: ", x_set.shape
                    print "Y shape: ", y_set.shape

                    if model_name == "MLPClassifier":
                        y_set = self.y_mlp(y_set)
                    else:
                        y_set = self.y_regression(y_set)

                    model = self.instance_model(module_name, class_name, model_name)

                    clf = GridSearchCV(model, tuned_parameters, cv=None)
                    clf.fit(x_set, y_set)

                    means = clf.cv_results_['mean_test_score']
                    stds = clf.cv_results_['std_test_score']

                    if not os.path.isdir('results'):
                        os.makedirs('results')

                    with open('results/' + conf['id'] + '.csv', 'w') as csvfile:
                        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
                            print "%f (+/-%f) for %r" % (mean, std * 2, params)
                            csvfile.write("%s;%i;%i;%f;%f;%r;%s\n" % (
                                estimator['model'], k, target, mean, std * 2, params, clf.best_params_))

        print "Test finished"

def main():
    """main function of module"""

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config-file', nargs='?', action="store", \
                        dest="config_file", help="File with the parameters \
                        download the data. It can only contain some parameters  \
                        and specify the others by cli.")

    arguments = parser.parse_args()

    config_file = arguments.config_file

    with open(config_file) as data_file:
        config_data = json.load(data_file)

    normalized_csv_path = config_data["normalized_csv_path"]
    estimator_config = config_data["estimator_config"]

    grid = GridSearch(normalized_csv_path, estimator_config)
    grid.explore()

if __name__ == "__main__":
    main()
