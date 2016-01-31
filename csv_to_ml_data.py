import pandas as pd
import os
import csv
from pandas import Timestamp
min_date = Timestamp(0)
max_date = Timestamp(0)
abs_path = '/home/evan/Desktop/economy/data'
dataframes = []
for i in os.listdir(abs_path):
	if i.endswith('.csv') and i.startswith('M'):
		
		file_path = abs_path + '/%s' % i
		with open(file_path, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			reader.next()
			#print i
			df = pd.DataFrame.from_csv(file_path)
			df.columns = [i.replace('.csv', '')]
			dataframes.append(df)
			for row in reader:
				if (Timestamp(row[0]) < min_date):
					min_date = Timestamp(row[0])
				if (Timestamp(row[0]) > max_date):
					max_date = Timestamp(row[0])


#print min_date, max_date
target_dict = {}
with open('target.csv', 'rb') as csvfile: 
	reader = csv.reader(csvfile)
	reader.next()
	for row in reader:
		date = str(Timestamp(row[0]).replace(day=01))
		if not date in target_dict:
			target_dict[date] = row[1]

		#target_dict[row[0].replace(day=01)] = row


ranges = pd.date_range(min_date, max_date, freq='M').shift(1, freq=pd.datetools.day)
new_dataframe = pd.DataFrame(index=ranges)

#print index
#print ranges

for d in dataframes:
	name_of_data = d.columns[0]
	new_dataframe[name_of_data] = float('NaN')
	for index, row in d.iterrows():
		index = index.replace(day=01)
		if index in ranges:
			new_dataframe[name_of_data][index] = row[0]
	print name_of_data
			#print index 
print new_dataframe

new_dataframe['target'] = float('NaN')

for index, row in new_dataframe.iterrows():
	try:
		new_dataframe['target'][index] = target_dict[str(index)]
	except KeyError:
		new_dataframe['target'][index] = 0

new_dataframe.to_csv('data.csv', na_rep = 'NaN')
 #print index, row[0]

