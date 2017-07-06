# Random forest regression for real-time prediction on key statistics
from sklearn.ensemble import RandomForestClassifier
import math
def RF_predict(X, Y, X_test):
    # X is an array of observed attributes - dummy values for now
    X = [[0, 0], [1, 1]]
    # Y is an array of observed values - dummy values for now
    Y = [0, 1]
    numIterations = math.sqrt(len(Y))
    clf = RandomForestClassifier(numIterations)
    clf = clf.fit(X, Y)

    # test array - or arrays to classify - dummy values for now
    X_test = [[1, 2], [0, 1], [0.5, 0.2]]
    return clf.predict(X_test)

# done