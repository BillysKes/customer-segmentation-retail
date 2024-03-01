

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sb
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

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
kmeans = KMeans(init="random", n_clusters=4, n_init=10, random_state=1)

#fit k-means algorithm to data
kmeans.fit(scaled_df)

#view cluster assignments for each observation
#df['cluster'] = kmeans.labels_
scaled_df['cluster'] = kmeans.labels_
#print("\n\n", df.nunique())  # statistics information
#df.to_csv('C:\\Users\\vasil\\Downloads\\normalizedRFMclustering3.csv')
silhouette_coefficient = silhouette_score(scaled_df, kmeans.labels_)
print("Silhouette Coefficient:", silhouette_coefficient)

#print(df)
''''# Creating figure
z = scaled_df['Monetary']
x = scaled_df['Frequency']
y = scaled_df['Recency']
c = scaled_df['cluster']
fig = plt.figure(figsize=(16, 9))
ax = plt.axes(projection="3d")

# Add x, y gridlines
ax.grid(b=True, color='grey',
        linestyle='-.', linewidth=0.3,
        alpha=0.2)

# Creating color map
#my_cmap = plt.get_cmap('hsv')
# Creating plot
sctt = ax.scatter3D(x, y, z,
                    alpha=0.8,
                    c=c,

                    marker='^')
plt.title("simple 3D scatter plot")
ax.set_xlabel('Frequency', fontweight='bold')
ax.set_ylabel('Recency', fontweight='bold')
ax.set_zlabel('Monetary', fontweight='bold')
fig.colorbar(sctt, ax=ax, shrink=0.5, aspect=5)
# show plot
plt.show()'''
#df.to_csv('C:\\Users\\vasil\\Downloads\\normalizedRFM.csv')


