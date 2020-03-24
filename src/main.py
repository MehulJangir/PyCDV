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
    'token':token0,
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



from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
plt.figure()
plt.imshow(WordCloud(max_font_size=50, max_words=80, background_color="white").generate(' '.join([val for val in df['source'][0: 20]])), interpolation="bilinear")
plt.axis("off")
plt.show()
plt.figure()
plt.imshow(WordCloud(max_font_size=50, max_words=80, background_color="white").generate(' '.join([val for val in df['source'][0: 20]])), interpolation="bilinear")
plt.axis("off")
plt.show()


#################################################
#                   Step 4 Code below           #
#################################################


action = 'API_getObservationsFromDataset'
        
parameters = {
 'token':token0,
 'id_dataset':'5d4c14cd9516290b01c7d673',
 'aggregate_in_time_interval':{"output":"avg","empty_intervals":"impute","time_interval_size":86400},
 'blends':[
        #Yen vs USD              
{"id_blend":"5d2495169516290b5fd2cee3","restriction":"None","blend_type":"ts","drop_features":[]},
        # Euro Vs USD
{"id_blend":"5d4b3af1951629707cc1116b","restriction":"None","blend_type":"ts","drop_features":[]},
        # Pound Vs USD              
{"id_blend":"5d4b3be1951629707cc11341","restriction":"None","blend_type":"ts","drop_features":[]},
        # Corn Price    
{"id_blend":"5d4c23b39516290b01c7feea","restriction":"None","blend_type":"ts","drop_features":[]},
        # CocaCola Price     
{"id_blend":"5d4c72399516290b02fe7359","restriction":"None","blend_type":"ts","drop_features":[]},
        # Platinum price             
{"id_blend":"5d4ca1049516290b02fee837","restriction":"None","blend_type":"ts","drop_features":[]},
        # Tin Price
{"id_blend":"5d4caa429516290b01c9dff0","restriction":"None","blend_type":"ts","drop_features":[]},
        # Crude Oil Price
{"id_blend":"5d4c80bf9516290b01c8f6f9","restriction":"None","blend_type":"ts","drop_features":[]}],
'date_filter':{"start_date":"2020-01-01T06:00:00.000Z","end_date":"2020-03-10T06:00:00.000Z"},
'consumption_confirmation':'on' 
}
df = pd.read_json(json.dumps(OpenBlender.call(action, parameters)['sample']), convert_dates=False, convert_axes=False).sort_values('timestamp', ascending=False)
df.reset_index(drop=True, inplace=True)
print(df.shape)
df.head()


# Lets compress all into the (0, 1) domain
df_compress = df.dropna(0).select_dtypes(include=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']).apply(lambda x: (x - x.min()) / (x.max() - x.min()))
df_compress['timestamp'] = df['timestamp']
# Now we select the columns that interest us
cols_of_interest = ['timestamp', 'PLATINUM_PRICE_price', 'CRUDE_OIL_PRICE_price', 'COCACOLA_PRICE_price', 'open', 'CORN_PRICE_price', 'TIN_PRICE_price', 'PLATINUM_PRICE_price']
df_compress = df_compress[cols_of_interest]
df_compress.rename(columns={'open':'DOW_JONES_price'}, inplace=True)
# An now let's plot them
from matplotlib import pyplot as plt
fig, ax = plt.subplots(figsize=(17,7))
plt = df_compress.plot(x='timestamp', y =['PLATINUM_PRICE_price', 'CRUDE_OIL_PRICE_price', 'COCACOLA_PRICE_price', 'DOW_JONES_price', 'CORN_PRICE_price', 'TIN_PRICE_price', 'PLATINUM_PRICE_price'], ax=ax)



#################################################
#                   Step 4 Code below           #
#################################################


# First the News Dataset
action = 'API_createDataset'
parameters = { 
 'token':token0,
 'name':'Coronavirus News',
 'description':'YOUR_DATASET_DESCRIPTION',
 'visibility':'private',
 'tags':[],
 'insert_observations':'on',
    'select_as_timestamp' : 'timestamp',
 'dataframe':df_news.to_json() 
}
        
print(OpenBlender.call(action, parameters))

news_token0 = input("please enter the value you see in the 'id_dataset' field from the output above: ")

# And now the Financial Indicators
action = 'API_createDataset'
parameters = { 
 'token':token0,
 'name':'Financial Indicators for COVID',
 'description':'YOUR_DATASET_DESCRIPTION',
 'visibility':'private',
 'tags':[],
 'insert_observations':'on',
 'select_as_timestamp' : 'timestamp',
 'dataframe':df_compress.to_json() 
}
        
print("\n\n", OpenBlender.call(action, parameters))

finance_token0 = input("Again, for the output above, enter the value you see in the 'id_dataset' field")

#regarding the print statements and input statements above, see the below explanation (also included in a commit message, but written here for convinience)
"""
"added input statements to (hopefully) grab the required tokens from the output of the 1st and 2nd code snippets of step 5 for the project article. TO-DO: This base-line code may be better suited for a jupyter notebook, please make one and add it to the repo"
"""

# NOTE: if the inputs don't work in the way i expect them to, then definitely make the Jupyter Notebook so that the user is aware they will need to initialise these variables manually in the next segment of code
# TO-DO: make a jupyter notebook of the article and the code within it (for convinience, it is this article: "https://towardsdatascience.com/gather-all-the-coronavirus-data-with-python-19aa22167dea") 



action = 'API_getObservationsFromDataset'
# ANCHOR: 'COVID19 Confirmed Cases'
# BLENDS: 'Coronavirus News', 'Financial Indicators for COVID'
        
parameters = { 
 'token':token0,
 'id_dataset':'5e6ac97595162921fda18076',
 'date_filter':{
               "start_date":"2020-01-01T06:00:00.000Z",
               "end_date":"2020-03-11T06:00:00.000Z"} ,
 
 },
'filter_select' : {'feature' : 'countryregion', 'categories' : ['Italy']},
'aggregate_in_time_interval':{"output":"avg","empty_intervals":"impute","time_interval_size":86400},
 'blends':[{"id_blend":news_token0,"restriction":"None","blend_type":"ts","drop_features":[]},
            {"id_blend":finance_token0,"restriction":"None","blend_type":"ts","drop_features":[]}] 
}
df = pd.read_json(json.dumps(OpenBlender.call(action, parameters)['sample']), convert_dates=False, convert_axes=False).sort_values('timestamp', ascending=False)
df.reset_index(drop=True, inplace=True)
