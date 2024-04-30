

import pandas as pd

df = pd.read_csv('C:\\Users\\vasil\\Downloads\\winsorizedClustered.csv')
print(df)

for column in df.columns:
    print("Column:", column)
    print(df[column].unique())

print("\n\n", round(df.describe(), 2))  # statistics information
print(df.nunique())
'''x = df.drop('CustomerID',axis=1)
x = x.values #returns a numpy array

min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)

scaled_df = pd.DataFrame(x_scaled,columns=['Recency','Frequency','Monetary'])
kmeans = KMeans(init="random", n_clusters=3, n_init=10, random_state=30)
kmeans.fit(scaled_df)
labels=kmeans.labels_
silhouette_coefficient = silhouette_score(scaled_df, labels)
print(silhouette_coefficient)
#ch_index = calinski_harabasz_score(scaled_df.drop(columns=['CustomerID','cluster'],axis=1),  kmeans.labels_)
df['cluster'] = labels
scaled_df['cluster'] = kmeans.labels_'''

