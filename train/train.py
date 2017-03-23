from lib.SolarData import SolarData
import pandas as pd
import json
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import numpy as np

with open('./conf/linearRegression.json') as data_file:    
    conf = json.load(data_file)

kList = conf['k']
start = conf['start']
end = conf['end']
tuned_parameters = conf['parameters']

print str(start)
print str(end)

for k in kList:
    solarData = SolarData(start, end)
    solarData.loadData(k, 2)

    X = solarData.getData()
    y = solarData.getTarget()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    #y = y_train.values.ravel()
    #y_train.values = np.array(y).astype(float)

    model = linear_model.LinearRegression()

    clf = GridSearchCV(model, tuned_parameters, cv=None)
    clf.fit(X_train, y_train.values.ravel())

    print ""
    print "Best parameters set found on development set:"
    print ""

    print clf.best_params_
    print "Grid scores on development set:"
    print ""
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print "%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params)
