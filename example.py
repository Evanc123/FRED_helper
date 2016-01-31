import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, f1_score, 
precision_score, recall_score, classification_report, confusion_matrix
import csv
from helpers import *

fr = Fred(api_key='', response_type='dict')

params = {
         'output_type':1
         }


"""
1. Download data to csv's in data folder
"""
#example list
categories_to_check = {'GNPCA', 'DSPIC96', 'CPILFESL', 'CPIAUCSL','GDPC1','A191RL1Q225SBEA','A191RO1Q156NBEA','DFF','MEHOINUSA672N','M2V','TEDRATE',
'PAYEMS','M2','INDPRO','CIVPART','PSAVERT','SP500','M1','PCE','HOUST','PCECC96','DPCERL1Q225SBEA','IC4WSA','DGS30','DGS20','DGS10','DGS5',
'DGS3','DGS2','DGS1','DTB3','MORTG','UMCSENT','DSPIC96','A067RO1Q156NBEA','A067RL1Q156SBEA',
'CPILFESL','PCEPI','CES0500000003','EMRATIO','A939RX0Q048SBEA','EXCSRESNS','BUSLOANS','CILACBQ158SBOG','PPIACO','TCU','PCEPILFE',
'DPCCRV1M225SBEA','M1V','U6RATE','MULT','LNS11300060','A229RX0','RHORUSQ156N','MZM','NETEXP','EXPGSC1','GPDI','NAPMNOI','IMPGSC1','CSUSHPISA',
'MZMV','GCEC96','A822RL1A225NBEA','A822RO1Q156NBEA','PI','AAA10Y'}


for category in categories_to_check:
	categoory_to_pd_csv(category, fr)


"""
2. Prepare data to be converted to numpy array (In this case, choose all data collected monthly)
"""

# Where the data is on your machine
abs_data_path = '' 
target_csv_path = ''

#Change from 'M' to 'W' if you want the weekly data
dataframes = load_dataframes_from_path(abs_data_path, 'M')

[min_date, max_date] = get_min_and_max_timestamp_of_folder(abs_path_data, 'M')

#Whether this be reccesion or GDP data, or whatever
target_dict = create_target_dict_from_csv(target_csv_path)

ranges = get_date_ranges(min_date, max_date, 'M')

new_dataframe = pd.DataFrame(index=ranges)

fill_new_dataframe_from_list(new_dataframe, dataframes)

give_new_dataframe_targets(new_dataframe, target_dict)

new_dataframe.to_csv('data.csv', na_rep='NaN')


"""
3. Convert CSV to NDARRAY, and Train RandomForestClassifier on Data
"""


df = pd.read_csv('data.csv', header=0)
df = df._get_numeric_data()
numeric_headers = list(df.columns.values)
np_data = df.as_matrix()

imp = Imputer(missing_values='NaN', strategy='median', axis=0)
imp.fit(np_data)

data = imp.transform(np_data)
X = data[:, 0:-1]
y = data[:, -1:].ravel()



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.1)

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
np.savetxt('prediction_probabilities.txt', predictions)



