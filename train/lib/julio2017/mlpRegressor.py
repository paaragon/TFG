"""
This module does training with MLPRegressor
"""

import argparse
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
from ..lib.SolarData import SolarData

class MlpRegressor(object):
    """this class train a MLPRegressor"""

    solar_data = None
    y_set = None
    x_set = None
    activation = "relu"

    def __init__(self, start, end, k, target, activation):
        self.solar_data = SolarData(start, end)
        self.solar_data.loadData(k, target)

        self.x_set = self.solar_data.getData()
        self.y_set = self.solar_data.getTarget()

        self.activation = activation

    def train(self):
        """Method for train MlpRegressor"""

        model = MLPRegressor(hidden_layer_sizes=(10,), activation=self.activation)
        model.fit(self.x_set, self.y_set)
        model.score(self.x_set, self.y_set)

        self.__save(model, "../trained/mlp_regressor.pkl")

    def __save(self, model, path):
        print "Saving"

        joblib.dump(model, path)
        print "Saved"

def main():
    """main function of the module"""

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', action="store", dest="start", help="Start date for data set")
    parser.add_argument('-e', action="store", dest="end", help="End date for data set")
    parser.add_argument('-k', action="store", dest="knumber", help="K previous instances")
    parser.add_argument('-t', action="store", dest="horiz", help="Prediction horizon (target)")
    parser.add_argument('-a', action="store", dest="activation", help="Activation function")

    arguments = parser.parse_args()

    start = arguments.start
    end = arguments.end
    knumber = arguments.knumber
    horiz = arguments.horiz
    activation = arguments.activation

    mlp = MlpRegressor(start, end, knumber, horiz, activation)
    mlp.train()


if __name__ == "__main__":
    main()
