mdf['opp_code'] =  mdf['Opponent'].astype('category').cat.codes
# mdf['team_code'] =  mdf['Team'].astype('category').cat.codes
# mdf['formation'] =  mdf['Formation'].astype('category').cat.codes
# mdf['hour'] = mdf['Time'].replace(':.+','',regex=True).astype('int')
# mdf['day_code'] = mdf['Date'].dt.dayofweek # put in order of days of week
# mdf['target'] = (mdf['Result'] == 'W').astype('int')
# mdf.dropna()