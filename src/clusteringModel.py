from matplotlib import pyplot as plt
from sklearn import preprocessing
from sklearn.cluster import KMeans
import pandas as pd


df = pd.read_csv('C:\\Users\\vasil\\Downloads\\winsorizedMonetaryFrequencyRFM.csv')
x = df.drop('CustomerID',axis=1)
x=x.values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
scaled_df = pd.DataFrame(x_scaled,columns=['Recency','Frequency','Monetary'])

kmeans = KMeans(n_clusters=3, init='k-means++', max_iter=300)
kmeans.fit(scaled_df)
labels=kmeans.labels_
df['cluster'] = labels

print(df)
