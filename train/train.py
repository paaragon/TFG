from sklearn.externals import joblib
from sklearn.svm import SVR
import numpy as np
from sklearn import linear_model
from lib.SolarData import SolarData
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor

start = 20150101
end = 20153112
start_hour = 100
end_hour = 2000
k = 4
target = 2


def trainMLPRegressor():
    print "training"

    start_date = 20150101
    end_date = 20153112
    start_hour = 800
    end_hour = 2000

    k = 4
    target = 2

    solar_data = SolarData(start_date, end_date, start_hour, end_hour)
    solar_data.loadData(k, target)

    x = solar_data.getData()
    y = solar_data.getTarget()

    mlp = MLPRegressor(hidden_layer_sizes=(100,100), activation='logistic', solver='lbfgs', random_state=2)
    return mlp.fit(x, y.values.ravel())


def trainSVR():
    print "Training"

    solarData = SolarData(start, end)
    solarData.loadData(k, target)

    X = solarData.getData()
    y = solarData.getTarget()

    svr_rbf = SVR(kernel='rbf', C=1000, gamma=0.001)
    return svr_rbf.fit(X, y.values.ravel())


def trainLinear():
    print "Training Linear"

    solarData = SolarData(start, end)
    solarData.loadData(k, target)

    X = solarData.getData()
    y = solarData.getTarget()

    regr = linear_model.LinearRegression()
    return regr.fit(X, y)


def y_Mlp(y):
    mappedY = []
    for i in range(y.shape[0]):
        # map 0 - 2000 => 0 - 100
        map = int(((y.iloc[i] + 1) / 2) * 100)
        mappedY.append(map)

    return np.array(mappedY,)


def trainMLP():
    print "Training MLP"

    solarData = SolarData(start, end)
    solarData.loadData(k, target)

    X = solarData.getData()
    y = solarData.getTarget()

    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 4), random_state=2)
    return clf.fit(X, y_Mlp(y))


def save(model, path):
    print "Saving"
    joblib.dump(model, path)
    print "Saved"


def trainAndSave():
    print "Train and save"
    #model = trainSVR()
    #model = trainLinear()
    #model = trainMLP()
    model = trainMLPRegressor()
    save(model, 'trained/mlp_regressor.pkl')


if __name__ == "__main__":

    trainAndSave()
