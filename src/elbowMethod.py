

from matplotlib import pyplot as plt
from sklearn import preprocessing
from sklearn.cluster import KMeans
import pandas as pd


df = pd.read_csv('C:\\Users\\vasil\\Downloads\\winsorizedMonetaryFrequencyRFM.csv')

kmeans_kwargs = {
"init": "k-means++",
"max_iter":300
}

x = df.drop('CustomerID',axis=1)
x=x.values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
scaled_df = pd.DataFrame(x_scaled,columns=['Recency','Frequency','Monetary'])

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
