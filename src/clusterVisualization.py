

from sklearn import preprocessing
from sklearn.cluster import KMeans
import pandas as pd
from matplotlib import pyplot as plt



df = pd.read_csv('C:\\Users\\vasil\\Downloads\\winsorizedClusteredv2.csv')

colors = ['blue', 'green', 'red']

recency_count = round(df.groupby('cluster')['Recency'].mean().reset_index(),2)
plt.figure(figsize=(8, 6))
plt.subplot(2, 2, 1)
plt.bar(recency_count['cluster'].astype(str), recency_count['Recency'], width=0.2, color=colors)
plt.ylabel('Recency score (AVG)')
plt.xlabel('Cluster')
plt.title('Average Recency score by cluster')
for i, v in enumerate(recency_count['Recency']):
    plt.text(i, v, str(v), ha='center')

plt.subplot(2, 2, 3)
frequency_count = round(df.groupby('cluster')['Frequency'].mean().reset_index(),2)
plt.bar(frequency_count['cluster'].astype(str), frequency_count['Frequency'], width=0.2, color=colors)
plt.ylabel('Frequency score (AVG)')
plt.xlabel('Cluster')
plt.title('Average Frequency score by cluster')
for i, v in enumerate(frequency_count['Frequency']):
    plt.text(i, v, str(v), ha='center')

plt.subplot(2, 2, 4)
monetary_count = round(df.groupby('cluster')['Monetary'].mean().reset_index(),2)
plt.bar(monetary_count['cluster'].astype(str), monetary_count['Monetary'], width=0.2, color=colors)
plt.ylabel('Monetary score (AVG)')
plt.xlabel('Cluster')
plt.title('Average Monetary score by cluster')
for i, v in enumerate(monetary_count['Monetary']):
    plt.text(i, v, str(v), ha='center')

plt.show()