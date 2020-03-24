#################################################
#                   Step 2 Code below           #
#################################################

from matplotlib import pyplot as plt
import OpenBlender
import pandas as pd
import json
#%matplotlib inline
action = 'API_getObservationsFromDataset'

token0 = '5e7a020e9516296cb9efb249JGOrGBIApe2tyunHZp2BQf5VitHVys'

parameters = { 
 'token':token0,
 'id_dataset':'5e6ac97595162921fda18076',
 'date_filter':{
               "start_date":"2020-01-01T06:00:00.000Z",
               "end_date":"2020-03-11T06:00:00.000Z"},
 'consumption_confirmation':'on' 
}

df_confirmed = pd.read_json(json.dumps(OpenBlender.call(action, parameters)['sample']), convert_dates=False, convert_axes=False).sort_values('timestamp', ascending=False)
df_confirmed.reset_index(drop=True, inplace=True)
df_confirmed.head(10)


#################################################
#                   Step 3 Code below           #
#################################################


action = 'API_getOpenTextData'
parameters = {
    'token':'YOUR_TOKEN_HERE',
    'consumption_confirmation':'on',
    'date_filter':{"start_date":"2020-01-01T06:00:00.000Z", 
                   "end_date":"2020-03-10T06:00:00.000Z"},
    'sources':[
                # Wall Street Journal
               {'id_dataset' : '5e2ef74e9516294390e810a9', 
                 'features' : ['text']},
                # ABC News Headlines
               {'id_dataset':"5d8848e59516294231c59581", 
                'features' : ["headline", "title"]},
                # USA Today Twitter
               {'id_dataset' : "5e32fd289516291e346c1726", 
                'features' : ["text"]},
                # CNN News
               {'id_dataset' : "5d571b9e9516293a12ad4f5c", 
                'features' : ["headline", "title"]}
    ],
    'aggregate_in_time_interval' : {
              'time_interval_size' : 60 * 60 * 24
    },
    'text_filter_search':['covid', 'coronavirus', 'ncov']
    
}
df_news = pd.read_json(json.dumps(OpenBlender.call(action, parameters)['sample']), convert_dates=False, convert_axes=False).sort_values('timestamp', ascending=False)
df_news.reset_index(drop=True, inplace=True)


# Let's take a look
df_news.head(20)


interest_countries = ['China', 'Iran', 'Korea', 'Italy', 'France', 'Germany', 'Spain']
for country in interest_countries:
    df_news['count_news_' + country] = [len([text for text in daily_lst if country.lower() in text]) for daily_lst in df_news['source_lst']]
df_news.reindex(index=df_news.index[::-1]).plot(x = 'timestamp', y = [col for col in df_news.columns if 'count' in col], figsize=(17,7), kind='area')
