import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Importing dataset 
df = pd.read_csv('steam_games.csv') 
print(df['genre'])

# Checking columns
print(df.dtypes)

# Cleaning and checking data range of dataset
df = df.dropna(subset=['release_date'])
df['release_date'] = pd.to_datetime(df['release_date'],errors='coerce')
df['year'] = df['release_date'].dt.year
df['year'] = df['year'].sort_values()

# Tail and head of dataset
print("Oldest game in dataset.\n",df[['name','year']].tail(5)) 
print("Latest game in dataset.\n",df[['name','year']].head(5)) 

# Removing future games
df = df.drop(df[df['year'] >= 2020].index) 
df = df.drop(df[df['year'] <= 1995].index)  

# Geting number of unique years
years = pd.unique(df['year'])
years = np.sort(years)
years = np.delete(years, -1)
bins = len(years)

# Check and clean genres
df = df[df['genre'].notnull()]
genres = pd.unique(df['genre'])
categories = []
for key in genres:
    categories = categories + key.split(",")

categories = pd.unique(categories)
catDict = {}
counter = 0
for key in categories:
    catDict[counter] = key
    counter = counter + 1 


print(catDict)
categories = np.delete(categories, [4,7,8,12,13,14,15,16,17,19,18,20,21,22,23,25,23])
print(categories)

# Substracting unmatched words in dataframe
keyList = []
for index, row  in df.iterrows():
    keyList = row[13].split(',')
    keyList = [i for i in keyList if i in categories]
    keyList = ''.join(keyList)
    df.at[index,'genre'] = keyList

print(pd.unique(df['genre']))

# Making a list with less popoular categories
subCategories = df['genre'].value_counts()
subCategories = subCategories.to_dict()
for key in subCategories.copy():
    if(subCategories[key]<=1500):
        del subCategories[key]


# Subseting dataframe with previous list
for index, row  in df.iterrows():
    if row[13] not in subCategories:
        df.drop(index, inplace=True)

# Fill empty genre with name 'other'
for index, row  in df.iterrows():
    if(df['genre'].empty==True):
        df.at[index,'genre'] = 'other'


# Plot a number of games each year
ax = sns.histplot(data=df, x='year', hue='genre', multiple='stack', bins=bins, palette="Set2")
plt.xticks(years, rotation = 45)
ax.tick_params(axis='both', which='minor', labelsize=4)
plt.show()

