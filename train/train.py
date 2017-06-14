from sklearn.externals import joblib
from sklearn.svm import SVR
import numpy as np
from sklearn import linear_model
from lib.SolarData import SolarData
from sklearn.neural_network import MLPClassifier

start = 20150101
end = 20153112
k = 5
target = 2

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

    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 4), random_state=2)
    return clf.fit(X, y_Mlp(y))

def save(model, path):
    print "Saving"
    joblib.dump(model, path)
    print "Saved"

def trainAndSave():
    print "Train and save"
    model = trainSVR()
    #model = trainLinear()
    #model = trainMLP()
    save(model, 'trained/linear.pkl')

if __name__ == "__main__":
    
    trainAndSave()