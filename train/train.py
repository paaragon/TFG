from sklearn.externals import joblib
from sklearn.svm import SVR
from lib.SolarData import SolarData

start = 20150101
end = 20153112
k = 4
target = 2

def trainSVR():
    print "Training"

    solarData = SolarData(start, end)
    solarData.loadData(k, target)

    X = solarData.getData()
    y = solarData.getTarget()

    svr_rbf = SVR(kernel='rbf', C=1000, gamma=0.001)
    return svr_rbf.fit(X, y.values.ravel())

def save(model, path):
    print "Saving"
    joblib.dump(model, path)
    print "Saved"

def trainAndSave():
    print "Train and save"
    model = trainSVR()
    save(model, 'trained/model.pkl')

if __name__ == "__main__":
    
    trainAndSave()