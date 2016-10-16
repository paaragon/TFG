# -*- coding: utf-8 -*-

import pandas
import numpy

titanic =pandas.read_csv('train.csv')

titanic["Age"] = titanic["Age"].fillna(titanic["Age"].median())

titanic.loc[titanic["Sex"]=="male", "Sex"] = 1
titanic.loc[titanic["Sex"]=="female", "Sex"] = 0

titanic["Cabin"] = titanic["Cabin"].fillna(0)
titanic.loc[titanic["Cabin"] != 0, "Cabin"] = 1

train = titanic[0:len(titanic)/2]

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from sklearn.cross_validation import ShuffleSplit

estimator = SVC(kernel='linear')
cv = ShuffleSplit(X_train.shape[0], n_iter=10, test_size=0.2, random_state=0)

predictors = ["Pclass", "Sex", "Age", "Cabin"]

alg = LinearRegression()
alg.fit(train[predictors], train["Survived"])

test = titanic[len(titanic)/2:]

predictions = alg.predict(test[predictors])

predictions[predictions >= 0.3] = 1
predictions[predictions < 0.3] = 0

print len(predictions)
print len(test["Survived"])

error = numpy.mean( predictions != test["Survived"] )

print 1 - error
    
print "Done."
    