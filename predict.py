import pandas as pd
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import time
import seaborn as sns

mdf = pd.read_csv('data.csv')
mdf['Venue_code'] = mdf['Venue'].astype('category').cat.codes
mdf['opp_code'] =  mdf['Opponent'].astype('category').cat.codes
mdf['team_code'] =  mdf['Team'].astype('category').cat.codes
mdf['formation'] =  mdf['Formation'].astype('category').cat.codes
mdf['hour'] = mdf['Time'].replace(':.+','',regex=True).astype('int')
#mdf['day_code'] = mdf['Date'].dt.dayofweek # put in order of days of week
mdf['target'] = (mdf['Result'] == 'W').astype('int')
mdf.dropna()

cmdf = mdf
cmdf.to_csv('data1.csv')
cmdf = cmdf.drop(["Unnamed: 0","Team", "Opponent", "Result", "Captain", "Referee", "Match Report", "Notes", "Venue", "Day", "Round", "Comp", "Formation"],axis =1 )
cmdf = cmdf.drop(["Time"], axis =1)
cmdf = cmdf.drop(["Date"], axis =1)
cmdf.to_csv('data1.csv')
train = cmdf[cmdf['Season'] < 2018]
test = cmdf[cmdf['Season'] > 2018]
predictors = ['Venue_code','team_code','opp_code','hour','day_code']

print(cmdf.dtypes)
