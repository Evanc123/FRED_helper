import pandas as pd
import os
import csv
from pandas import Timestamp

#Returns String like 'M' for Monthly, 'Q' for Quarterly
def get_series_freq_type(category, fr):
	return fr.series.details(cateogory)[0]['frequency_short']

def get_series_observations(cateogry, fr):
	return fr.series.observations(category, params=params)

def pp_observations(series_data):
	for res in series_data:
		print res['date'], res['value']

def sort_list_of_categories_by_freq_type(category_list, fr):
	pass

def category_to_pd_csv(category, data_dir='data/', fr):
	values = []
	times = []
	data = get_series_observations(category, fr)
	for sample in data:
		values.append(sample['value'])
		times.append(sample['date'])
	series_type = get_series_fr_type(category, fr)
	file_name = series_type + '_%s' % category + '.csv'
	pd.DataFrame({'time':pd.Series(times), 'value':pd.Series(values)}
		).to_csv('%s%s' % (data_dir, file_name), index=False)

def load_dataframes_from_path(path, freq_type):
	dataframes = []
	for i in os.listdir(abs_path):
		if i.endswith('.csv') and i.startswith(freq_type):
			file_path = abs_path + '/%s' % i
			with open(file_path, 'rb') as csvfile:
				reader = csv.reader(csvfile)
				reader.next()
				#print i
				df = pd.DataFrame.from_csv(file_path)
				df.columns = [i.replace('.csv', '')]
				dataframes.append(df)
	return dataframes

def get_min_and_max_timestamp_of_folder(path, freq_type):
	min_date = Timestamp(0)
	max_date = Timestamp(0)
	for i in os.listdir(abs_path):
	if i.endswith('.csv') and i.startswith('M'):
		file_path = abs_path + '/%s' % i
		with open(file_path, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			reader.next()
			for row in reader:
				if (Timestamp(row[0]) < min_date):
					min_date = Timestamp(row[0])
				if (Timestamp(row[0]) > max_date):
					max_date = Timestamp(row[0])
	return [min_date, max_date]


def create_target_dict_from_csv(path):
	target_dict = {}
	with open('%s' % path, 'rb') as csvfile: 
		reader = csv.reader(csvfile)
		reader.next()
		for row in reader:
			date = str(Timestamp(row[0]).replace(day=01))
			if not date in target_dict:
				target_dict[date] = row[1]
			
	return target_dict

def get_date_ranges(min_date, max_date, freq_type):
	return pd.date_range(min_date, max_date, 
		freq=freq_type).shift(1, freq=pd.datetools.day)


def fill_new_dataframe_from_list(new_dataframe, dataframes):
	name_of_data = d.columns[0]
	new_dataframe[name_of_data] = float('NaN')
	for index, row in d.iterrows():
		index = index.replace(day=01)
		if index in ranges:
			new_dataframe[name_of_data][index] = row[0]
	return new_dataframe

def give_new_dataframe_targets(new_dataframe, target_dict):
	new_dataframe['target'] = float('NaN')

	for index, row in new_dataframe.iterrows():
		try:
			new_dataframe['target'][index] = target_dict[str(index)]
		except KeyError:
			new_dataframe['target'][index] = 0
