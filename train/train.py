from lib.SolarData import SolarData
import json
from sys import argv
#from sklearn import linear_model
#from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

def getFiles():
    ret = []
    for i in range(1, len(argv)):
        ret.append(argv[i])
    return ret

def instanceModel(module_name, class_name, model_name):
    module = __import__(module_name)
    class_ = getattr(module, class_name)
    method = getattr(class_, model_name)
    return method()

if __name__ == "__main__":

    if len(argv) == 1:
        print 'No train file specified'
        exit()
    
    files = getFiles()

    for i in range(len(files)):

        with open(files[i]) as data_file:
            conf = json.load(data_file)

        kList = conf['k']
        start = conf['start']
        end = conf['end']

        print str(start)
        print str(end)
        
        for k in kList:
            for estimator in conf['estimator']:

                module_name = estimator["module"]
                class_name = estimator["class"]
                model_name = estimator["model"]
                tuned_parameters = estimator["parameters"]

                solarData = SolarData(start, end)
                solarData.loadData(k, 2)

                X = solarData.getData()
                y = solarData.getTarget()

                print "X shape: ", X.shape
                print "Y shape: ", y.shape

                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.3, random_state=0)

                model = instanceModel(module_name, class_name, model_name)

                clf = GridSearchCV(model, tuned_parameters, cv=None, n_jobs=56)
                clf.fit(X_train, y_train.values.ravel())

                means = clf.cv_results_['mean_test_score']
                stds = clf.cv_results_['std_test_score']

                with open('results/' + conf['id'] + '.csv', 'a') as csvfile:
                    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
                        print "%f (+/-%f) for %r" % (mean, std * 2, params)
                        csvfile.write("%s;%i;%f;%f;%r;%s\n" % (
                            estimator['model'], k, mean, std * 2, params, clf.best_params_))

    print "Test finished"
