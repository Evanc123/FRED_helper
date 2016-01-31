from fred import Fred
import pandas as pd


fr = Fred(api_key='adc13f2abb54e82daf273340f536b8d5', response_type='dict')

params = {
         'output_type':1
         }

urls_to_check = {'GNPCA', 'DSPIC96', 'CPILFESL', 'CPIAUCSL','GDPC1','A191RL1Q225SBEA','A191RO1Q156NBEA','DFF','MEHOINUSA672N','M2V','TEDRATE',
'PAYEMS','M2','INDPRO','CIVPART','PSAVERT','SP500','M1','PCE','HOUST','PCECC96','DPCERL1Q225SBEA','IC4WSA','DGS30','DGS20','DGS10','DGS5',
'DGS3','DGS2','DGS1','DTB3','MORTG','UMCSENT','DSPIC96','A067RO1Q156NBEA','A067RL1Q156SBEA',
'CPILFESL','PCEPI','CES0500000003','EMRATIO','A939RX0Q048SBEA','EXCSRESNS','BUSLOANS','CILACBQ158SBOG','PPIACO','TCU','PCEPILFE',
'DPCCRV1M225SBEA','M1V','U6RATE','MULT','LNS11300060','A229RX0','RHORUSQ156N','MZM','NETEXP','EXPGSC1','GPDI','NAPMNOI','IMPGSC1','CSUSHPISA',
'MZMV','GCEC96','A822RL1A225NBEA','A822RO1Q156NBEA','PI','AAA10Y'}

urls_to_check_testing = {'GNPCA', 'MULT', 'PI', 'AAA10Y'}


def get_series_fr_type(series_url):
	return fr.series.details(series_url)[0]['frequency_short']

def get_series_observations(series_url):
	return fr.series.observations(series_url, params=params)

def pp_observations(series_data):
	for res in series_data:
		print res['date'], res['value']

q_count = 0
m_count = 0
total = 0
for url in urls_to_check:
	values = []
	times = []
	data = get_series_observations(url)
	for sample in data:
		values.append(sample['value'])
		times.append(sample['date'])

	series_type = get_series_fr_type(url)
	file_name = series_type + '_%s' % url + '.csv'

	pd.DataFrame({'time':pd.Series(times), 'value':pd.Series(values)}).to_csv('data/%s' % file_name, index=False)
	#series_data = get_series_observations(url)
	#print pp_observations(series_data), series_type
	print url



