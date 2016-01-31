import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
import csv
categories_of_interest = ['M_CPIAUCSL', 'M_INDPRO', 'M_NAPMNOI', 'M_PAYEMS', 'M_PPIACO']



df = pd.read_csv('data.csv', header=0)

original_headers = list(df.columns.values)

print len(original_headers)
df = df._get_numeric_data()

numeric_headers = list(df.columns.values)

print numeric_headers

np_data = df.as_matrix()

imp = Imputer(missing_values='NaN', strategy='median', axis=0)
imp.fit(np_data)

data = imp.transform(np_data)
#print data

X = data[:, 0:-1]
y = data[:, -1:].ravel()



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.1)
#print X_train, y_train

clf_rf = RandomForestClassifier(n_estimators=500, n_jobs=3)

clf_rf.fit(X_train, y_train)
score = clf_rf.predict(X_test)
print f1_score(y_test, score)
print clf_rf.score(X_test, y_test)

print clf_rf.feature_importances_

ind = np.argpartition(clf_rf.feature_importances_, -5)[-5:]

for i in ind:
	print numeric_headers[i]

predictions = clf_rf.predict_proba(X)
np.savetxt('probabilities.txt', predictions)



