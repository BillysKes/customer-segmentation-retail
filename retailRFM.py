

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sb
from sklearn import preprocessing
from sklearn.cluster import KMeans


df = pd.read_csv('C:\\Users\\vasil\\Downloads\onlineretailRFMvaluesTable.csv')

print('\ndata types : \n', df.dtypes)  # verifying that data types are all correct
for column in df.columns:
    print("Column:", column)
    print(df[column].unique())

print("\n\n", round(df.describe(), 2))  # statistics information
print(df.nunique())
'''plt.figure(figsize=(8, 6))
sb.heatmap(data=df.corr(numeric_only=True), cmap="YlGnBu", annot=True)
plt.show()'''
#exit(df['Recency'].drop_duplicates())
#df['r'] = pd.qcut(df['Recency'], q=5, labels=[5, 4, 3, 2, 1])
#df['f'] = pd.qcut(df['Frequency'], q=2, labels=[1,2])
#df['m'] = pd.qcut(df['Monetary'], q=5, labels=[1, 2, 3, 4, 5])



x = df.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
scaled_df = pd.DataFrame(x_scaled,columns=df.columns)
print(df)

kmeans_kwargs = {
"init": "random",
"n_init": 10,
"random_state": 1,
}

sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(scaled_df)
    sse.append(kmeans.inertia_)

plt.plot(range(1, 11), sse,'bx-')
plt.xticks(range(1, 11))
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
plt.show()

#instantiate the k-means class, using optimal number of clusters
kmeans = KMeans(init="random", n_clusters=3, n_init=10, random_state=1)

#fit k-means algorithm to data
kmeans.fit(scaled_df)

#view cluster assignments for each observation
df['cluster'] = kmeans.labels_

print(df)
#df.to_csv('C:\\Users\\vasil\\Downloads\\normalizedRFM.csv')


